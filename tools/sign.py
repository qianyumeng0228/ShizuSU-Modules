#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ShizuSU 模块仓库签名工具（进阶2）

用 Ed25519 对发布产物签名，防投毒：
  - output/modules.json        -> 对 canonical JSON 字节签名（索引防篡改）
  - private/*.zip              -> 对 zip 原始字节签名（私有模块逐文件）

用法：
  python tools/sign.py --gen-key                  # 生成密钥对（公钥入仓库，私钥给 secrets）
  python tools/sign.py                            # 默认：签 output/modules.json + private/*.zip
  python tools/sign.py --verify                   # 校验签名是否有效

私钥来源优先级：
  1. 环境变量 SHIZUSU_SIGN_PRIVATE_KEY（GitHub Actions secrets 托管）
  2. --private-key <file>（本地开发）
未提供私钥时跳过签名步骤并提示（CI 中视为失败）。
"""
import argparse
import base64
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SIGN_DIR = HERE / "signatures"
OUT_DIR = HERE / "output"
PRIVATE_DIR = HERE / "private"

CANONICAL_SEP = (",", ":")
PUBLIC_KEY_FILE = SIGN_DIR / "public.pem"


def _canonical_bytes(data) -> bytes:
    """canonical JSON（键排序、紧凑分隔符），保证跨端验签一致。"""
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=CANONICAL_SEP).encode("utf-8")


def _load_private_key(path=None):
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    pem = None
    env_key = os.environ.get("SHIZUSU_SIGN_PRIVATE_KEY")
    if env_key:
        pem = env_key.encode("utf-8")
    elif path:
        pem = Path(path).read_bytes()
    if not pem:
        return None
    return serialization.load_pem_private_key(pem, password=None)


def _load_public_key(path=None):
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

    key_file = Path(path) if path else PUBLIC_KEY_FILE
    if not key_file.exists():
        return None
    return serialization.load_pem_public_key(key_file.read_bytes())


def gen_key():
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    SIGN_DIR.mkdir(parents=True, exist_ok=True)
    key = Ed25519PrivateKey.generate()
    priv_pem = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )
    pub_pem = key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    PUBLIC_KEY_FILE.write_bytes(pub_pem)
    priv_out = HERE / "secrets" / "shizusu-sign-private.pem"
    priv_out.parent.mkdir(parents=True, exist_ok=True)
    priv_out.write_bytes(priv_pem)
    print(f"公钥已写入: {PUBLIC_KEY_FILE}")
    print(f"私钥已写入: {priv_out}（请将内容加入 GitHub Actions secrets: SHIZUSU_SIGN_PRIVATE_KEY，切勿提交入库）")


def _sign_file(key, payload_bytes):
    return base64.b64encode(key.sign(payload_bytes)).decode("ascii")


def sign(private_key_path=None):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    key = _load_private_key(private_key_path)
    if key is None:
        print("未找到私钥（env SHIZUSU_SIGN_PRIVATE_KEY 或 --private-key），跳过签名。", file=sys.stderr)
        return 1

    out_sig = OUT_DIR / "signatures"
    out_sig.mkdir(parents=True, exist_ok=True)

    # 1) 索引签名：对 modules.json 原始文件字节签名（跨端零歧义，Android 端直接验下载字节）
    catalog_path = OUT_DIR / "modules.json"
    if not catalog_path.exists():
        print(f"缺少 {catalog_path}，先运行 build.py", file=sys.stderr)
        return 1
    payload = catalog_path.read_bytes()
    meta = {
        "signedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "target": "modules.json",
        "payload": "raw file bytes（modules.json 文件原样字节，Android 端对下载字节直接验签）",
        "moduleCount": len(json.loads(payload)),
        "publicKey": (PUBLIC_KEY_FILE.read_text(encoding="utf-8") if PUBLIC_KEY_FILE.exists() else ""),
    }
    (out_sig / "modules.sig").write_text(_sign_file(key, payload), encoding="utf-8")
    (out_sig / "modules.meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 2) 私有模块 zip 逐个签名
    signed_zips = 0
    if PRIVATE_DIR.exists():
        for zf in sorted(PRIVATE_DIR.glob("*.zip")):
            sig = _sign_file(key, zf.read_bytes())
            (out_sig / f"{zf.stem}.sig").write_text(sig, encoding="utf-8")
            signed_zips += 1

    print(f"签名完成: modules.json + {signed_zips} 个私有 zip -> {out_sig}")
    return 0


def verify(public_key_path=None):
    key = _load_public_key(public_key_path)
    if key is None:
        print(f"缺少公钥 {PUBLIC_KEY_FILE}", file=sys.stderr)
        return 1

    sig_dir = OUT_DIR / "signatures"
    catalog_path = OUT_DIR / "modules.json"
    ok = True

    sig_file = sig_dir / "modules.sig"
    if sig_file.exists() and catalog_path.exists():
        catalog_bytes = catalog_path.read_bytes()
        try:
            key.verify(base64.b64decode(sig_file.read_text().strip()), catalog_bytes)
            print("modules.json 签名: 有效")
        except Exception as e:
            print(f"modules.json 签名: 无效 ({e})")
            ok = False

    if PRIVATE_DIR.exists() and sig_dir.exists():
        for zf in sorted(PRIVATE_DIR.glob("*.zip")):
            sf = sig_dir / f"{zf.stem}.sig"
            if not sf.exists():
                print(f"{zf.name}: 缺少签名文件")
                ok = False
                continue
            try:
                key.verify(base64.b64decode(sf.read_text().strip()), zf.read_bytes())
                print(f"{zf.name}: 签名有效")
            except Exception as e:
                print(f"{zf.name}: 签名无效 ({e})")
                ok = False

    return 0 if ok else 1


def main():
    parser = argparse.ArgumentParser(description="ShizuSU 模块仓库签名工具")
    parser.add_argument("--gen-key", action="store_true", help="生成 Ed25519 密钥对")
    parser.add_argument("--verify", action="store_true", help="校验已发布产物的签名")
    parser.add_argument("--private-key", metavar="FILE", help="私钥文件路径（默认用 env SHIZUSU_SIGN_PRIVATE_KEY）")
    parser.add_argument("--public-key", metavar="FILE", help="公钥文件路径（默认 signatures/public.pem）")
    args = parser.parse_args()

    if args.gen_key:
        gen_key()
        return 0
    if args.verify:
        return verify(args.public_key)

    try:
        return sign(args.private_key)
    except ImportError:
        print("缺少 cryptography 依赖，请先执行: pip install -r requirements.txt", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
