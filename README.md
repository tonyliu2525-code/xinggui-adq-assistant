# 星轨投放助手

腾讯 ADQ 开户准备、投放诊断、出价分析、广告创意与投后复盘。一个标准 Agent Skill，配套官方知识资料、素材索引、客户模板及报表脚本。

## 安装

```bash
npx -y skills@1.7.2 add tonyliu2525-code/xinggui-adq-assistant --skill xinggui-adq-assistant -a codex claude-code hermes-agent cursor gemini-cli qwen-code opencode --copy -y
```

以上命令已验证从远程安装到当前项目，支持所列七种 Agent。需要用户级安装时添加 `-g`。安装文件完整性已验证，各客户端运行权限以实际环境为准。未被安装器列出但支持标准 Skill 的平台，可导入完整技能目录。平台是否允许自定义导入、容量和工具权限以当前入口为准；不保证所有 AI 产品支持相同功能。

## 使用

> 使用星轨投放助手。请根据业务资料、后台设置和同周期报表，提供具体调整方案与观察条件。

## 正式使用说明

[安装与使用手册](skills/xinggui-adq-assistant/assets/客户手册/安装与使用.md)

## 运行环境

读取规则与模板不依赖脚本。自动核算使用 Python 3 标准库；知识库检索使用 Node.js。截图理解、联网与图片生成由所用 Agent 提供。账户操作由客户执行；未连接腾讯 API。官方资料及第三方素材按来源说明和实际授权使用。
