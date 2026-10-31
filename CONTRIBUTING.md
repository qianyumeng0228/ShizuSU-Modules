# ShizuSU-Modules 收录指南（CONTRIBUTING）

欢迎向本仓库提交模块。本仓库是 KernelSU / Magisk / APatch 生态的开源模块收录中心，同时输出两套格式：

- **A 路线**：`modules.json` + `module/<id>.json`（ShizuSU / SukiSU-Ultra / KernelSU 管理器原生源）
- **B 路线**：`json/config.json` + `json/modules.json` + `modules/<id>/track.json`（MMRL / BakaSU 兼容）

---

## 一、收录标准

### 硬门槛（进入索引的必要条件）

| # | 条件 | 说明 |
|---|---|---|
| 1 | 源码可达 | 公开的 GitHub 仓库（`owner/repo`），可被 GitHub API 访问 |
| 2 | 许可证 | 仓库可检测到标准开源许可证（SPDX 标识：MIT / Apache-2.0 / GPL 系 / BSD / Unlicense 等） |
| 3 | 可下载 | 最新 release 包含可下载的 zip 资产（无 zip 时回退最近有 zip 的 release） |
| 4 | 非内核构建 | 不收纯内核源码 / LKM 构建类仓库（模块仓库只收可安装模块） |

### 管理员背书（adminApproved）

许可证**未声明或不明确**（无 LICENSE 文件 / `NOASSERTION` / `NONE`）但有仓库、有可下载 release 的模块，可走**管理员背书**收录：

- 条目标记 `adminApproved: true`，`note` 注明「上游许可证未声明或不明确，由管理员背书收录，使用需自行评估风险」
- 背书决定由仓库管理员作出并留痕（Issue 或 commit message 注明审核理由）
- **下架机制**：上游作者主张权利，或发现背书收录的模块存在安全/合规风险，24h 内下架

### 不收录

- 无公开仓库（网盘 / Telegram 分发，无法审计源码）
- 无可下载 release zip
- 内核源码 / LKM 构建类
- 恶意 / 投毒 / 已知捆绑恶意行为的模块
- 明显侵权（打包他人闭源应用、未授权再分发）

---

## 二、收录流程

### 方式一：Issue 人工提交（推荐）

1. 使用[模块提交模板](.github/ISSUE_TEMPLATE/module_submission.md) 开 Issue，填写：
   - 模块 ID（英文小写，建议 `snake_case`，2–64 字符）
   - 源码仓库（公开 `owner/repo`）
   - 最新 release 下载地址（zip 直链）
   - 许可证（SPDX 标识）
   - 模块类型与一句话简介
2. 管理员审核（对照硬门槛 + 抽样核验仓库与 release）
3. 通过后加入 `modules.config.json`，每日构建自动生成双格式产物并发布
4. 审核结果在 Issue 中回复：`approved` / `rejected`（附原因）/ `need-license`（转管理员背书）

### 方式二：topic 自动发现 + 审批

1. `discover-modules.yml` 每日按 topic（`shizusu-module`、`kernelsu-module`、`magisk-module`、`apatch-module`）扫描 GitHub
2. 候选写入 `catalog/candidates.json`，每条含 `suggestedConfig` 片段
3. 管理员挑选后把候选片段加入 `modules.config.json` 即可

### 方式三：手机端上传 + 审批

ShizuSU 管理器「模块上传」入口 → Gist 分片上传 → 本仓库 `submission` Issue 待审队列 → 管理员在审批工具中通过后自动入库。

### 审核自动化

每日构建时 `tools/validate.py` 自动执行门槛检查（仓库可达 / 许可证 / module.prop / release 可达），结果写入 `audit.json`：

- `verified`：全部通过，正常进入索引
- `unverified`：某项未达标（许可证缺失只标注 `unknown` 不阻塞；release 不可达则标记），仍展示待审核状态
- 仓库不存在（404）：该模块自动从索引剔除

---

## 三、签名机制

- 发布产物由 Ed25519 签名：
  - `signatures/modules.sig`：A 路线索引签名
  - `signatures/<moduleId>.sig`：私有模块 zip 签名
- 公钥 `signatures/public.pem` 入库公开；私钥存 GitHub Actions secrets（`SHIZUSU_SIGN_PRIVATE_KEY`），**永不入库**
- 验签：`python tools/sign.py --verify`

---

## 四、本地开发

```bash
pip install -r requirements.txt
python build.py                # A 路线（GraphQL 批量预取，省 API 配额）
python tools/validate.py       # 开源门槛审核（进阶3）
python tools/build_mmrl.py     # B 路线 MMRL 输出
python tools/sign.py           # 签名（需私钥）
python verify_schema.py        # schema 兼容校验
```

环境变量：`GITHUB_TOKEN`（避免限流）、`SHIZUSU_SIGN_PRIVATE_KEY`（签名私钥）。

提交 PR 前请确保 `verify_schema.py` 通过；CI 中的 `validate-pr.yml` 会自动复核。

---

## 五、提交清单（Checklist）

提交模块前逐项自查：

- [ ] 源码仓库公开可访问，能被 GitHub API 查询
- [ ] 有标准许可证（LICENSE 文件）或申请管理员背书
- [ ] 最新 release 提供可下载 zip 资产
- [ ] 非内核源码 / LKM 构建类
- [ ] 代码可审计，无恶意行为
- [ ] moduleId 英文小写、合法（字母开头，2–64 字符，允许 `. _ -`）
- [ ] 与现有模块无重复（同名仓库 / 同名 moduleId）
