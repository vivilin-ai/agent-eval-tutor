# 补抓取结果

本次处理前一版本中除微信外的 38 个失败链接。18 项已恢复正文，2 项抓取后确认不作为方法来源，18 个链接仍受访问限制。知识库现有 108 个可检索文档。微信来源保持原状态，本次未重试。

## 恢复的正文

- [Trying to instrument an agentic app with Arize Phoenix and litellm](https://mlops.systems/posts/2025-06-04-instrumenting-an-agentic-app-with-arize-phoenix-and-litellm.html)（author_markdown）
- [2  99% of Executives are Misled by AI Advice – AI Essentials For Tech Executives](https://ai-execs.com/2_intro.html)（html_article）
- [Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences](https://arxiv.org/abs/2404.12272)（pdf_fulltext）
- [What is Theoretical Saturation?](https://delvetool.com/blog/theoreticalsaturation)（html_article）
- [GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning](https://arxiv.org/pdf/2507.19457)（pdf_fulltext）
- [Play Favorites: A Statistical Method to Measure Self-Bias in LLM-as-a-Judge](https://arxiv.org/pdf/2508.06709)（pdf_fulltext）
- [LangSmith: Agent & LLM Observability Platform](https://www.langchain.com/langsmith)（html_article）
- [Intro to GitHub for non-technical roles | Ben Balter](https://ben.balter.com/2023/03/02/github-for-non-technical-roles/)（html_article）
- [pash on X: "Boris from the Claude Code team explains why they ditched RAG for agentic discovery.  

"It outperformed everything. By a lot"" / X](https://x.com/pashmerepat/status/1926717705660375463?s=46)（html_article）
- [Aider LLM Leaderboards | aider](https://aider.chat/docs/leaderboards/)（html_article）
- [Introducing Codex | OpenAI](https://openai.com/index/introducing-codex/)（html_article）
- [Clio: Privacy-preserving insights into real-world AI use \ Anthropic](https://www.anthropic.com/research/clio)（html_article）
- [Demystifying evals for AI agents \ Anthropic](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)（html_article）
- [Cyclomatic complexity - Wikipedia](https://en.wikipedia.org/wiki/Cyclomatic_complexity)（html_article）
- [There Are Only 6 RAG Evals - Jason Liu](https://jxnl.co/writing/2025/05/19/there-are-only-6-rag-evals/)（html_article）
- [Writes and Write-Nots](https://paulgraham.com/writes.html)（html_article）
- [Curating LLM data – Hamel’s Blog](https://hamel.dev/notes/llm/finetuning/04_data_cleaning.html)（html_article）
- [Beyond Naive RAG: Practical        Advanced Methods](https://hamel.dev/notes/llm/rag/beyond-naive-rag.pdf)（pdf_fulltext）

## 抓取成功但不作为方法来源

- LinkedIn 个人主页：不是评测方法文章。
- arXiv 的 Abstention Ability 搜索结果：不是论文正文，也不能代表搜索结果中的论文已收录。

## 尚未恢复

16 个 YouTube 链接对应 11 个不同视频；另有 Substack 文章和 Figma 幻灯片。下列失败项均未进入检索，不会被用于方法建议：

- https://youtu.be/aqKUwPKBkB0?si=5KDmMQnRzO_Ce9xH — <urlopen error Tunnel connection failed: 403 Forbidden>
- https://www.youtube.com/watch?v=aqKUwPKBkB0 — <urlopen error Tunnel connection failed: 403 Forbidden>
- https://www.youtube.com/watch?v=qH1dZ8JLLdU — <urlopen error Tunnel connection failed: 403 Forbidden>
- https://m.youtube.com/watch?si=qknrtQeITqJ7VsJH&v=4dUFIRj-BWo&feature=youtu.be — <urlopen error Tunnel connection failed: 403 Forbidden>
- https://www.youtube.com/watch?v=EEw2PpL-_NM — <urlopen error Tunnel connection failed: 403 Forbidden>
- https://www.youtube.com/watch?v=e2i6JbU2R-s — <urlopen error Tunnel connection failed: 403 Forbidden>
- https://www.youtube.com/watch?v=BsWxPI9UM4c — <urlopen error Tunnel connection failed: 403 Forbidden>
- https://youtu.be/tqUDjc1HzO4 — <urlopen error Tunnel connection failed: 403 Forbidden>
- https://youtu.be/e2i6JbU2R-s?si=8p5XVxbBiioz69Xc — <urlopen error Tunnel connection failed: 403 Forbidden>
- https://www.youtube.com/watch?v=tqUDjc1HzO4 — <urlopen error Tunnel connection failed: 403 Forbidden>
- https://youtu.be/fA4pe9bE0LY — <urlopen error Tunnel connection failed: 403 Forbidden>
- https://www.youtube.com/watch?v=fA4pe9bE0LY — <urlopen error Tunnel connection failed: 403 Forbidden>
- https://www.youtube.com/watch?v=N-qAOv_PNPc — <urlopen error Tunnel connection failed: 403 Forbidden>
- https://pashpashpash.substack.com/p/why-i-no-longer-recommend-rag-for — <urlopen error Tunnel connection failed: 403 Forbidden>
- https://www.youtube.com/watch?v=LwLxlEwrtRA&t=534s — <urlopen error Tunnel connection failed: 403 Forbidden>
- https://www.figma.com/deck/nwRlh5renu4s4olaCsf9lG/Failure-is-a-Funnel?node-id=2009-927&t=GJlTtxQ8bLJaQ92A-1 — <urlopen error Tunnel connection failed: 403 Forbidden>
- https://youtu.be/R_HnI9oTv3c?si=hRRhDiydHU5k6ikc — <urlopen error Tunnel connection failed: 403 Forbidden>
- https://www.youtube.com/watch?v=R_HnI9oTv3c — <urlopen error Tunnel connection failed: 403 Forbidden>

## 提取与验证

- 三篇 arXiv 论文获取全文，标题通过其官方摘要页元数据核验。
- 30 MB 的 Beyond Naive RAG PDF 已提取全文，保留 PDF 页码；未做 OCR，图片/公式不保证完整。
- 数据清理旧页面按 Quarto 的常量跳转映射转到新页，未执行 JavaScript。
- MLOps 文章取自作者维护的 strickvl/mlops-dot-systems 仓库；front matter 明确列出原路径为 alias。
- 14 项测试通过，包含真实 PDF 提取、跳转安全检查、来源完整性与检索。三平台对话行为仍未实测。

## 后续条件

网络域名要求已保存在环境草稿，但保存不代表代理已放行。需在环境设置中应用相关网络变更，然后再执行：

```bash
python3 skills/agent-eval-tutor/scripts/kb.py crawl --retry-failed --exclude-domain mp.weixin.qq.com --max-pages 250
```

即使视频页面可读取，也必须取得字幕或可核验的官方文字稿；当前抓取器会拒绝将视频页面元数据当成知识。Substack 如有付费限制不能以预览替代全文；Figma 需要公开可读页面或合法导出的文件。

## 后续更新：微信文字来源已补齐

用户提供了从原文复制的文本，现已作为 user_provided_text 导入知识库。详情见 wechat-import.md。该导入不代表历史网络问题已解决，也不包含缺失图片。
