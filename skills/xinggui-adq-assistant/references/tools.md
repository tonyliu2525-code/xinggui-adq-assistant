# 包内工具

使用本机python或python3运行scripts/analyze_delivery.py、rank_creatives.py及delivery_source.py。
analyze_delivery.py --config <输入JSON> --csv <报表CSV> --output <客户项目结果JSON>。
rank_creatives.py --input <素材输入JSON> --output <客户项目排序JSON>。
delivery_source.py当前只支持CSV标准入口，腾讯模式明确未接入。无API也可以通过截图诊断。
出价是有条件的首轮启发式，不是最佳价格；缺少依据不产生通用出价。平均频次需确认同范围。
没有Python时可手工核算并明确未运行脚本，不得编造执行结果。

175条候选素材在assets/project/素材库/，分类与证据状态以index.json为准。22条有平台详情，153条初筛。
图片是来源卡片截图，不是广告原始图；视频未打包完整媒体。8条不完整预览默认隐藏。
本包不附自动采集浏览器脚本；公开检索可用宿主实际浏览器，遇到登录或限流停止，不索要Cookie。
