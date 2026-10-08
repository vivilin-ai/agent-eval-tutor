# 微信文章读取 Skill 搜索与实测

搜索范围：本会话云端 Skill 目录、本机 Skill 目录、GitHub 公开仓库。云端与本机目录没有微信读取 Skill。

公开候选：

- [wechat-article-archive](https://github.com/freestylefly/wechat-article-archive-skill)：已阅读 SKILL.md，审查并使用公开文章采集脚本；本次选用。
- [wechat-article-extractor](https://github.com/freestylefly/wechat-article-extractor-skill)：已阅读 SKILL.md 和部分实现，未运行。
- [tianyi-1349/wechat-article-reader](https://github.com/tianyi-1349/wechat-article-reader)：已检查入口及实现，未运行其多级反检测流程。
- [sanfan3/wechat-article-reader](https://github.com/sanfan3/wechat-article-reader)：MCP/CLI 读取器，含浏览器回退实现；不是带 SKILL.md 的 Skill 包。

实测采用用户原始完整 URL，核验 __biz、mid、idx、sn 与知识库现有记录相同。未使用用户登录凭证。

1. 在 /tmp 虚拟环境安装 requests 与 lxml，调用 archive Skill 的 fetch_html（不做盲目重试）。结果：代理 CONNECT 403，未取得页面。
2. 使用现有 Chromium 与 Playwright，经同一托管代理访问完整链接。结果：ERR_TUNNEL_CONNECTION_FAILED，未取得页面。
3. 运行环境报告 mp.weixin.qq.com 未出现在当前有效访问列表；配置草稿已有此域名。草稿保存不证明运行时已经应用。

这是代理连接阻塞，不能据此声称微信文章已删除、需要登录、出现验证码，或 Skill 本身不可用。没有正文，未新增知识文档，未把错误页面当成文章。

后续：在环境设置应用 mp.weixin.qq.com 网络配置后，重试公开文章采集。成功后核验文章标题、公众号、原文参数、正文完整性和图片/代码等内容，再更新知识库及下载包。

选用 Skill 的源码提交：4820880eb51de1f05683a1511657db3a8cea59d0
实测时间（UTC）：2026-10-08T14:57:11.741513+00:00

## 发布后复测

运行配置已变为版本 3，允许列表包含 mp.weixin.qq.com。实际 urllib、经批准的沙箱外复测及 curl 仍返回 CONNECT 403；响应服务为 Envoy，尚未取得微信页面。运行时策略执行状态为 unknown，不能确认代理已正确执行新策略。当前需平台侧诊断，不能继续把原因归为用户未保存或未发布。

## 第二次发布后复测

2026-10-08T15:24:00.113695+00:00：运行版本 5，网络模式 restricted、状态 enforced，允许列表包含 mp.weixin.qq.com。

- 标准 HTTP：分别请求核心参数链接、用户完整链接，CONNECT 403。
- 经批准的沙箱外请求：CONNECT 403，排除普通命令沙箱差异。
- Chromium/Playwright：保留托管代理与 TLS 验证，ERR_TUNNEL_CONNECTION_FAILED。
- 依据 [tianyi-1349/wechat-article-reader](https://github.com/tianyi-1349/wechat-article-reader) 的 curl_cffi 方案尝试 Chrome 读取。当前库不支持文档中的 chrome126，改用受支持的 chrome 配置后仍返回 CONNECT 403；未关闭 TLS 验证或绕开网络策略。
- 在 GitHub 公开索引按 mid 与 sn 分别搜索，未找到匹配副本；没有将其他文章替代该来源。

没有获取正文。平台策略报告与实际代理行为不一致，需要平台侧排查或从其他已授权环境取得可核验的原文导出。不能保证只更换读取库就能获取该链接。

## 后续更新：微信文字来源已补齐

用户提供了从原文复制的文本，现已作为 user_provided_text 导入知识库。详情见 wechat-import.md。该导入不代表历史网络问题已解决，也不包含缺失图片。
