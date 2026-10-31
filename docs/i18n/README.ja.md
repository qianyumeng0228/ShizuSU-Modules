# ShizuSU-Modules

[![ビルド状態](https://github.com/qianyumeng0228/ShizuSU-Modules/actions/workflows/update-modules.yml/badge.svg)](https://github.com/qianyumeng0228/ShizuSU-Modules/actions/workflows/update-modules.yml)
[![サイト](https://img.shields.io/website?url=https%3A%2F%2Fqianyumeng0228.github.io%2FShizuSU-Modules&label=Pages)](https://qianyumeng0228.github.io/ShizuSU-Modules)
[![モジュール数](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fqianyumeng0228.github.io%2FShizuSU-Modules%2Fmodules.json&query=length&label=モジュール&color=blue)](https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json)
[![ライセンス](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

**言語:** [中文](https://github.com/qianyumeng0228/ShizuSU-Modules/blob/main/README.md) · [English](README.en.md) · [Deutsch](README.de.md) · [Русский](README.ru.md) · 日本語 · [Français](README.fr.md) · [Italiano](README.it.md) · [Español](README.es.md)

**KernelSU / Magisk / APatch** エコシステム向けのオープンソースモジュールリポジトリソースです。1 つの設定で 2 つの互換形式を出力します — **ShizuSU / SukiSU-Ultra（ルート A）** と **MMRL / BakaSU（ルート B）** — 廃止された公式ソース `modules.kernelsu.org` の代替として提供します。

**1,532 件のグローバルリスト** から選別したオープンソースモジュールを収録し、バージョンとダウンロードリンクは毎日自動で再構築されます。

## 特徴

- **二形式出力**: `modules.json`（マネージャー標準スキーマ）+ `json/modules.json`（MMRL プロトコル）— 1 つのリポジトリで ShizuSU・KernelSU・SukiSU-Ultra・MMRL・BakaSU に対応
- **完全自動メンテナンス**: GitHub Actions が毎日 UTC 00:30 にメタデータ・最新リリース・直接ダウンロードリンクを更新し、再署名
- **オープンソース閾値監査**: `tools/validate.py` が各モジュールを「ソース到達可能＋ライセンス＋ダウンロード可能なリリース」で検証し、結果は追跡可能な形で `audit.json` に記録
- **署名メカニズム**: インデックスとプライベートモジュールの ZIP は Ed25519 署名付き。公開鍵はリポジトリに同梱され、オフライン検証が可能
- **手動＋自動の二重収録**: Issue 提出・GitHub topic 自動発見・端末からのアップロード＋承認の 3 経路
- **管理者承認収録**: ライセンス不明瞭なモジュールは管理者審査後に収録（`adminApproved`）、透明に表示し、リスクは利用者が自己判断

## クイックスタート

### ShizuSU / SukiSU-Ultra マネージャー

マネージャーは実行時リポジトリソースの上書きに対応しています。「settings」設定にキー `module_repo_base_url` をこのリポジトリの Pages URL で書き込みます:

```
https://qianyumeng0228.github.io/ShizuSU-Modules
```

### KernelSU 公式マネージャー（ルート A）

`modules.json` リスト形式に対応したマネージャーで、リポジトリソースを追加:

```
https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json
```

### MMRL

MMRL でリポジトリを追加。末尾の `/` はあってもなくても構いません:

```
https://qianyumeng0228.github.io/ShizuSU-Modules/
```

MMRL は `json/config.json` と `json/modules.json` を読み取り、収録済みモジュールを直接閲覧・インストールできます。

### BakaSU

BakaSU の「リポジトリ設定 → + リポジトリを追加」:

- **API 形式: 必ず `MMRL` を選択**
- **サーバー URL**（`/json/modules.json` の接尾辞なし）:

```
https://qianyumeng0228.github.io/ShizuSU-Modules
```

> `KernelSU Modules API` は選択**しないでください**: それは Registry プロトコルです。本リポジトリは `api/v1` エンドポイントを提供しておらず、BakaSU は Registry ソースに対し実 SHA-256 検証を強制するため、404/インストールエラーになります。

## リポジトリ構造

```
modules.json                  # ルート A: モジュールカタログ（公式スキーマ準拠のリスト）
module/<moduleId>.json        # ルート A: モジュールごとの詳細（リリース / README / ダウンロードリンク）
json/config.json              # ルート B: MMRL リポジトリ説明
json/modules.json             # ルート B: MMRL モジュールインデックス
modules/<id>/track.json       # ルート B: MMRL track 定義
modules/<id>/update.json      # ルート B: MagiskUpdateJson（バージョン/ダウンロード）
signatures/public.pem         # Ed25519 公開鍵
signatures/modules.sig        # modules.json の署名
signatures/<moduleId>.sig     # プライベートモジュール ZIP の署名
audit.json                    # オープンソース閾値監査結果
catalog/candidates.json       # topic 自動発見の候補一覧
private/*.zip                 # プライベートモジュール（管理者承認）
compat/                       # 互換モジュール
```

データは `build.py`（ルート A）+ `tools/build_mmrl.py`（ルート B）+ `tools/validate.py`（監査）+ `tools/sign.py`（署名）で生成され、ルート A スキーマは SukiSU-Ultra / ShizuSU マネージャーのパースコードとフィールド単位で一致しています。

## 収録内容

- ルート A インデックスに **871 モジュール**、うち **804** が MMRL/BakaSU から直接インストール可能
- **19 カテゴリ**をカバー: Root 隠蔽 / Play Integrity、メタモジュール（マウントエンジン）、Zygisk 実装、パフォーマンス調整、ネットワークプロキシ、広告ブロック、音声、フォント/表示、バックアップ/復旧、Xposed/LSPosed、WebUI など
- **324 件は管理者承認**（`adminApproved`）: 上流ライセンスが未宣言または不明瞭 — 管理者審査後に収録、各項目に `note` 付き。利用時はリスクを自己判断
- データソース: KernelSU モジュール全网まとめ（1,532 件の重複排除リスト）

## 収録基準

インデックスに収録されるには、モジュールは以下の条件を満たす必要があります（詳細は [CONTRIBUTING.md](https://github.com/qianyumeng0228/ShizuSU-Modules/blob/main/CONTRIBUTING.md)）:

1. **ソース到達可能**: 公開の GitHub リポジトリ
2. **ライセンス**: 検出可能な標準オープンソースライセンス（SPDX）; 不明瞭なものは管理者承認経由
3. **ダウンロード可能**: 最新リリースにダウンロード可能な ZIP を含む
4. **カーネルビルド以外**: カーネルソース / LKM ビルド系は収録しない（インストール可能なモジュールのみ）

基準に満たないモジュールは `unverified` と表示（「審査待ち」状態で表示継続）; 公開リポジトリのないプライベートモジュールは管理者承認で `origin=manual` とマークされます。

## モジュールの提出

3 つの経路から選択:

1. **Issue 提出（推奨）**: [モジュール提出テンプレート](.github/ISSUE_TEMPLATE/module_submission.md) を使用して Issue を開き、ソースリポジトリとリリース URL を記載
2. **自動発見**: `discover-modules.yml` が毎日 topic（`shizusu-module` / `kernelsu-module` / `magisk-module` / `apatch-module`）で GitHub をスキャンし、候補は `catalog/candidates.json` へ
3. **端末からのアップロード**: ShizuSU マネージャー「モジュールアップロード」入口 → 審査キュー → 管理者承認 → 自動収録

## 更新メカニズム

- **毎日ビルド**: UTC 00:30（北京時間 08:30）にバージョン・ダウンロードリンク・統計を自動更新
- **手動トリガー**: リポジトリの Actions ページで `Update module repo` workflow を実行
- ビルドチェーン: ルート A 生成 → オープンソース閾値監査 → MMRL 出力 → 署名 → スキーマ検証 → GitHub Pages 同期

## 引用と連携（歓迎）

あらゆるマネージャー・ツール・サイトが本リポジトリのデータを参照できます。推奨方法:

- **JSON を直接読む**: `https://qianyumeng0228.github.io/ShizuSU-Modules/modules.json`（リスト）と `module/<id>.json`（詳細）
- **動的バッジ**: モジュール数バッジは動的です（shields.io がリアルタイムで読取。本ファイル冒頭参照）
- **連携仕様**: フィールド定義は [API.md](https://github.com/qianyumeng0228/ShizuSU-Modules/blob/main/API.md) を参照。ダウンロードリンクは上流 GitHub リリースへの直リンクで、そのまま保存可能
- **出典表示**: 参照時は「データソース: ShizuSU-Modules」とリポジトリへのリンクを記載。上流への負荷軽減のため JSON のキャッシュを推奨（データは毎日 08:30 頃更新）

## ライセンスと免責事項

- 本リポジトリの**コードとインデックス**は [MIT ライセンス](LICENSE) に従います
- 収録した第三者モジュールの**著作権は原作者に帰属**します: 本リポジトリは索引/リンクのみを提供し、「収録」は利用許諾を意味しません。使用前に各モジュールの上流ライセンスを確認してください。管理者承認モジュール（`adminApproved`）はライセンス不明瞭のため、リスクは自己判断で
- 上流の作者が権利を主張する場合、Issue を開けば 24 時間以内に該当項目を削除します
