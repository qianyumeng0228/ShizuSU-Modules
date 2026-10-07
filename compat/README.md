# ShizuSU 兼容适配模块 (compat)

存放需要在 ShizuSU 上适配后才能刷写的第三方模块。ShizuSU 基于 SukiSU-Ultra（KernelSU 系），
正常情况下官方 KernelSU 模块可直接刷入；以下模块因使用非 POSIX 语法或依赖特定 shell 特性
（如进程替换 `<()`），在部分 ROM（toybox sh，如小米 HyperOS）上官方包无法安装，故提供适配版。

## bindhosts-shizusu-v2.1.5.zip

- 来源: [bindhosts/bindhosts](https://github.com/bindhosts/bindhosts) v2.1.5 (WTFPL)
- 适配原因: 官方 `customize.sh` 使用进程替换 `< <()` 监听音量键（询问是否安装 BindHosts-app），
  toybox sh 不支持该语法 → 安装脚本解析失败
- 适配内容: 跳过 BindHosts-app 音量键询问（使用内置 WebUI 即可），其余逻辑与官方一致
- 安装: 管理器 → 模块 → 从本地安装
- 使用: 重启后生效；规则持久化在 `/data/adb/bindhosts/`
