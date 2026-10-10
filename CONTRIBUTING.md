# ShizuSU 模块仓库收录规则（CONTRIBUTING）

本仓库是 ShizuSU 生态的模块收录中心，同时输出两套格式：

- **A 路线**：`modules.json` + `module/<id>.json`（ShizuSU 管理器原生源，schema 兼容）
- **B 路线**：`json/config.json` + `json/modules.json` + `modules/<id>/track.json`（MMRL 兼容，MMRL 应用可直接加载本仓库）

## 收录门槛（进阶3：开源审核，自动校验）

所有模块必须满足以下条件才会以 `verified` 状态进入索引：

1. **开源**：提供可访问的源码仓库（GitHub `repo` 字段）
2. **许可证**：仓库可检测到标准开源许可证（SPDX）
3. **可下载**：最新 release 包含可下载的 zip 资产
4. **标准结构**：仓库根目录存在 `module.prop`（或已有 release zip）

未达标模块会被标记 `unverified`（仍展示，但管理器/MMRL 端可见"待审核"状态）；无公开仓库的私有模块由管理员背书，标记 `manual`。

每日构建时 `tools/validate.py` 自动执行上述检查，结果写入 `output/audit.json`。

## 收录流程

### 方式一：人工提交（推荐）
1. 在本仓库开 Issue（使用模块提交模板），附源码仓库链接与 release 地址
2. 管理员审核后把模块信息加入 `modules.config.json`
3. 每日构建自动生成双格式产物并发布

### 方式二：自动发现 + 审批
1. `discover-modules.yml` 每天按 topic（`shizusu-module`、`kernelsu-module`、`magisk-module`、`apatch-module` 等）扫描 GitHub
2. 候选写入 `catalog/candidates.json` 并自动开审阅 Issue
3. 人工挑选后把候选的 `suggestedConfig` 片段加入 `modules.config.json` 即可

### 方式三：手机端上传 + 审批
ShizuSU 管理器「模块上传」入口 → Gist 分片上传 → 本仓库 `submission` Issue 待审队列 → 管理员在审批工具中通过后自动入库。

## 签名（进阶2）

- 发布产物由 Ed25519 签名：`signatures/modules.sig`（索引签名）+ `signatures/<moduleId>.sig`（私有 zip 签名）
- 公钥：`signatures/public.pem`（入库）
- 私钥：GitHub Actions secrets `SHIZUSU_SIGN_PRIVATE_KEY`（不入库）
- 验签工具：`python tools/sign.py --verify`

## 本地开发

```bash
pip install -r requirements.txt
python build.py                # A 路线
python tools/validate.py       # 进阶3 审核
python tools/build_mmrl.py     # B 路线（MMRL）
python tools/sign.py           # 进阶2 签名（需私钥）
python verify_schema.py        # schema 兼容校验
```

环境变量：`GITHUB_TOKEN`（避免限流）、`SHIZUSU_SIGN_PRIVATE_KEY`（签名私钥）。
