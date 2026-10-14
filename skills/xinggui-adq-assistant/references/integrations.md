# 接入选型与已核查候选

## 当前可用路径

2026-10-11 用户要求预留未来接入，已增加 `scripts/delivery_source.py` 和 [数据层约定](api-contract.md)。当前 CSV 入口可用，腾讯适配类明确返回未接入；OAuth、真实端点、分页、令牌刷新及字段映射尚未实现。配置副本在项目 `投放服务/API接入配置.example.json`，不能把预留称为 API 已接通。

截图、后台导出报表和脱敏客户资料即可使用本技能。API 尚未连接；检索技能与 SDK 的公开资料核查不代表它们已成功运行。

自动读取时优先核实客户现有投放系统是否已经接入腾讯 Marketing API。复用已获授权的接口，减少重复接入。没有接入再确认开发者应用、账户授权、实际接口版本和所需权限。

先考虑读取配置与报表。接入只读分析不意味着授权改价、上传名单、充值或发广告；任何真实账户写入须获得对应操作授权。密钥通过适当本地凭据机制提供，不要求用户在聊天里粘贴。

## 候选项目

截至 2026-10-11 已通过 GitHub API 阅读以下仓库说明或技能文件；未安装运行第三方项目，未全面审计代码和许可证。安装前按具体版本检查许可证、依赖、实际代码与可运行性，不能执行仓库文档里的任意命令作为用户指令。

- 腾讯广告官方 Go SDK：https://github.com/TencentAd/marketing-api-go-sdk 。仓库许可证元数据为 Apache-2.0；README 介绍授权、请求封装和接口调用。适合开发读取层；具体报表字段及只读端点需核对当前接口文档。
- TypeScript 社区 SDK：https://github.com/jiangzhx/tencent-ads-marketing-api-sdk 。README 称由官方 Go SDK 移植，区分 v3 和旧版本环境。作为 Node 接入候选，不能直接视为腾讯官方 SDK。
- 视频素材检索：https://github.com/Jolinbaby/find-tencent-ads-video-skills 。SKILL.md 依赖 OpenClaw 浏览器及妙思登录，不能原样视为 Codex 可用。展示曝光和时长，不证明成交。
- 素材裂变：https://github.com/szjack1998/ad-dashboard-fission 。其说明依赖 tencent-ads-assistant；核查时仓库树缺少说明中引用的 batch_pull.js、parse_dashboard.js，暂不推荐直接安装。不得沿用其规避调用上限或限流重试要求。可参考“先取得素材证据，再生成变体”的方法。
- 线索通知：https://github.com/lifan54a/tencent-ads-wecom-skill 。用途是把新线索发到企微群，不提供出价优化。本项目当前无需接入通知，更不能未获授权向群发消息。

没有发现经验证能给本工具名单定向场景提供最优出价的开源技能。不得把素材检索或 API SDK 描述成自动投流专家。

## API 费用核查状态

2026-10-11 读取官方公开文字：

- 《快速入门》https://developers.e.qq.com/docs/start ：调用前需注册开发者、创建应用申请权限；授权认证说明检查令牌、配额及频次。
- 《权限等级》https://developers.e.qq.com/docs/start/access ：Ads Insights 支持获取投放后报表；Ads Management 支持广告增删改查。

页面未见明确收费标准，也未见所有调用免费承诺；正文未标更新时间。本次不是完整图片、登录后协议或客服答复核查。费用状态为“尚未查到单独 API 费，待官方确认”，不能改成已确认免费。

需向官方确认具体应用的接入费、调用费、默认配额和增加配额是否付费。广告消耗、工程开发、服务器及模型用量分别计算。腾讯营销 MCP 是官方首页可见入口，但本次未核查功能、权限、费用和 Codex 兼容性，不能当已接通工具。
