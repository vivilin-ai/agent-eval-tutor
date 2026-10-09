# Agent Reach v1.5.0 补抓取记录

工具版本：官方 tag v1.5.0，提交 f65526cbaaad3879473acc1ba6dbefd195caf2be；隔离安装，无业务凭证。
尝试时间（UTC）：2026-10-09T00:53:29.975440+00:00

结果：16 条 YouTube 来源链接对应 11 个不同视频；全部字幕获取失败。Substack 与 Figma 的直接访问及 Jina Reader 读取均失败。新增知识文档 0 篇，原有 109 篇保留。

YouTube 使用 Agent Reach 推荐的 yt-dlp 2026.08.19，启用英文/中文字幕和自动字幕，未下载视频。所有视频网页与 API 请求均遇到环境代理 CONNECT 403。
Substack 和 Figma 使用 Agent Reach WebChannel / Jina Reader，同样在 CONNECT 阶段被拒绝，未到达正文解析阶段。
这不是证实来源不存在、需要登录或没有字幕。失败响应不纳入知识库。

后续：网络配置草稿已添加 r.jina.ai 并保留原允许域名；需要用户保存并发布环境后才能重试。原来源域名虽在允许列表中，实际连接仍失败，需要重新检查平台代理策略。

## 本轮来源

- https://youtu.be/aqKUwPKBkB0?si=5KDmMQnRzO_Ce9xH
- https://www.youtube.com/watch?v=aqKUwPKBkB0
- https://www.youtube.com/watch?v=qH1dZ8JLLdU
- https://m.youtube.com/watch?si=qknrtQeITqJ7VsJH&v=4dUFIRj-BWo&feature=youtu.be
- https://www.youtube.com/watch?v=EEw2PpL-_NM
- https://www.youtube.com/watch?v=e2i6JbU2R-s
- https://www.youtube.com/watch?v=BsWxPI9UM4c
- https://youtu.be/tqUDjc1HzO4
- https://youtu.be/e2i6JbU2R-s?si=8p5XVxbBiioz69Xc
- https://www.youtube.com/watch?v=tqUDjc1HzO4
- https://youtu.be/fA4pe9bE0LY
- https://www.youtube.com/watch?v=fA4pe9bE0LY
- https://www.youtube.com/watch?v=N-qAOv_PNPc
- https://pashpashpash.substack.com/p/why-i-no-longer-recommend-rag-for
- https://www.youtube.com/watch?v=LwLxlEwrtRA&t=534s
- https://www.figma.com/deck/nwRlh5renu4s4olaCsf9lG/Failure-is-a-Funnel?node-id=2009-927&t=GJlTtxQ8bLJaQ92A-1
- https://youtu.be/R_HnI9oTv3c?si=hRRhDiydHU5k6ikc
- https://www.youtube.com/watch?v=R_HnI9oTv3c

## 环境发布后的重试

UTC：2026-10-09T04:32:29.256508+00:00。网络状态 enforced，r.jina.ai 已生效。

- Substack：成功取得《Why I No Longer Recommend RAG for Autonomous Coding Agents》文章正文并收录，保留原 URL、读取路径、时间与哈希；图片未读取。观点限于自主编码 Agent，不能作为所有 RAG 系统的通用结论。
- YouTube：11 个视频用 yt-dlp 再次尝试字幕，全部 CONNECT 403。Jina 可读 9 个视频页面，但 Transcript 区域没有字幕；另 2 个返回异常流量验证页。标题、简介、章节和推荐视频均未作为视频正文收录。
- Figma：Jina 返回 Failure is a Funnel 标题、14/16 页码和界面提示，缺少幻灯片正文，仍未收录。

本轮新增 1 篇，现有 110 篇可用、17 条失败、17 条排除。未绕过代理、验证码或登录限制。
