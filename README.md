# Agent Eval Tutor

一个帮助你开展 Agent 评测的顾问 Skill，面向 Codex、Claude Code 和 Workbuddy。无论你刚开始搭建评测，还是已经有评测集、正在排查效果问题，都可以用它讨论下一步怎么做。

## 它能帮你做什么？

- 梳理评测目标，明确什么算任务成功。
- 从真实案例出发开展错误分析，建立和改进评测集。
- 设计人工标注标准，检查 LLM judge 是否可信。
- 评估检索、工具调用和执行过程，定位失败环节。
- 讨论回归评测、多轮对话评测和上线验收方法。

Skill 会根据你的问题检索知识库，并引用支持建议的来源。需要了解背景时，同一议题累计最多提出 **3 个澄清问题**；你可以在同一会话中继续追问，它会沿用已经提供的信息。

如果知识库没有相应依据，它会明确说明找不到，不编造方法、指标或上线阈值。

## 知识库来自哪里？

知识库目前收录 109 篇资料，主要来自两组来源：

1. **[Hamel Husain 的 Evals FAQ](https://hamel.dev/blog/posts/evals-faq/)**，以及该页面链接的评测文章、论文和相关资料，涵盖错误分析、评测集、人工标注、LLM judge 等主题。
2. **[阿里技术公众号的 Agent 精细化评测文章](https://mp.weixin.qq.com/s?__biz=Mzg4NTczNzg2OA==&mid=2247511370&idx=1&sn=c9f4ff1d054cb229ac2f8c1462fcb05e)**，涵盖任务与模块评测、质量与成本、多轮对话及工程实践。该来源通过用户提供的正文收录，未包含图片中的信息。

部分外部链接尚未收录，因此知识库并非完整覆盖所有来源。你可以查看[资料目录](skills/agent-eval-tutor/references/catalog.md)。第三方资料的权利归原作者所有。

## 如何安装？

先[下载 Skill 压缩包](https://github.com/vivilin-ai/agent-eval-tutor/raw/refs/heads/main/dist/agent-eval-tutor.zip)，解压得到 `agent-eval-tutor` 文件夹。请保留整个文件夹，不要只复制 `SKILL.md`。

也可以从本仓库复制 `skills/agent-eval-tutor` 文件夹。

### Codex

把文件夹放到以下任一位置：

- 当前项目使用：`.agents/skills/agent-eval-tutor/`
- 所有项目使用：`~/.agents/skills/agent-eval-tutor/`

重新打开会话后，输入 `$agent-eval-tutor` 并附上你的问题。

### Claude Code

把文件夹放到以下任一位置：

- 当前项目使用：`.claude/skills/agent-eval-tutor/`
- 所有项目使用：`~/.claude/skills/agent-eval-tutor/`

重新打开会话后，输入 `/agent-eval-tutor` 并附上你的问题。

### Workbuddy

如果你的版本支持导入本地 Skill，在 Skill 管理或导入入口选择解压后的 `agent-eval-tutor` 文件夹，启用后在对话中请求使用它回答评测问题。具体入口和支持格式以当前版本为准；Workbuddy 的安装与调用方式尚未实测。

使用时需要宿主能够读取 Skill 中的资料，并运行 Python 3.10 或更新版本。知识库随包提供，日常使用无需单独配置知识库服务或 API key。三个平台的实际运行效果仍需在你的环境中验证。

## 如何使用？

安装后，直接描述你的 Agent、当前进展和想解决的问题。例如：

> 使用 agent-eval-tutor。我们正在做一个内部客服 Agent，目前还没有评测集，应该从哪里开始？

> 我们已有 200 条人工标注样本，但 LLM judge 经常和人工判断不一致，应该先排查什么？

> Agent 会检索知识库和调用业务工具。我们现在只看任务是否完成，怎样进一步定位过程中出了什么问题？

你不必一次提供全部背景。Skill 会在必要时提出澄清问题，再给出有来源的建议。后续可以继续追问：

> 我们现在只有两个人，每周能投入半天。按照这个条件，第一周应该先做哪些工作？

自动调用是否生效取决于宿主的 Skill 加载机制；如果没有触发，请显式指定 `agent-eval-tutor`。开启新会话时，请补充此前的进展和结论。
