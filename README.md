# Agent Eval Tutor

面向 Codex、Claude Code、Workbuddy 的 Agent 评测顾问 Skill。使用本地资料检索，支持多轮，同一议题累计最多三个澄清问题，无资料依据时明确承认找不到。

**当前状态：已收录 109 个知识文档（包括 Hamel FAQ、相关文章、PDF 全文及用户提供的微信正文）；18 个链接仍失败，17 项明确排除。微信来源通过用户粘贴文本补齐，未宣称网页抓取成功，缺失图片与原始标题等信息已标记。核心检索测试已通过，知识库仍有缺口，不能声称完整收录。平台文档访问受阻，三个宿主尚未实测，Workbuddy 安装路径及自动触发能力待核实。**

## 文件与依赖

`skills/agent-eval-tutor/` 是可整体复制的 Skill 包：`SKILL.md` 为入口，`references/coverage.json` 为覆盖清单，`references/documents/` 为知识正文，`scripts/kb.py` 为检索/更新工具。离线检索仅需 Python 3.10+ 标准库，无 API key，无第三方 Python 依赖。更新需要 HTTPS 来源访问；PDF 提取另需 Poppler 的 `pdftotext`，当前环境已安装。第三方正文的权利归原作者，分发前检查各来源许可；不要将外部文章视为本项目原创。

## 使用

在项目根目录执行：

```bash
python3 -m unittest discover -s tests -v
python3 skills/agent-eval-tutor/scripts/kb.py status
python3 skills/agent-eval-tutor/scripts/kb.py search '错误分析 error analysis'
python3 skills/agent-eval-tutor/scripts/kb.py crawl --max-pages 250
```

抓取使用 TLS 验证；失败、验证码和不支持的格式记录在覆盖清单中，不作为知识。FAQ 的直接链接逐项记录，相关 Hamel 评测文章再下钻一层，外链不递归。250 页是保护性上限，超出时显式标记，不能声称全部收录。自动抽取后仍需审查正文质量、链接范围、遗漏和引用；PDF 自动提取全文（上限 40 MB），保留 PDF 页码；无法提取的扫描件需要 OCR 或手动导入。视频必须获取字幕或官方文字稿，当前工具不会把视频页面信息当成正文；任意动态页面不会执行 JavaScript。支持 Quarto 常量跳转，不执行其脚本。当前检索为词法检索，中文问题需要扩展英文关键词；它不保证语义召回，命中也不证明答案有依据。

微信正文已通过用户粘贴文本导入：第 1–9 章、22,344 个字符。保存原始文本及哈希，检索结果附带缺失图表与未核验元信息的限制。正文为商品中心 Agent 的工程案例；案例中的配置和数字不作为通用标准。第 5.1 节六类 Judge Task 的细节在缺失图片中，不能据此列出具体六类任务。

后续可用 `import-text --file <UTF-8文本文件> --url <原始HTTPS链接> --title <内容标签> --note <缺失或未核验信息>` 导入资料；重复导入同一文本不会重复收录，抓取更新会保留手工导入来源。

## 三个平台

以下是通用 Skill 包的部署指引，不代表已在这三个宿主上做过运行验证。

- **Codex**：将整个 `agent-eval-tutor` 文件夹放入项目 `.agents/skills/` 或个人 `~/.agents/skills/`。可显式调用 `$agent-eval-tutor`；是否自动选中取决于宿主加载和描述匹配。
- **Claude Code**：将整个文件夹放入项目 `.claude/skills/` 或个人 `~/.claude/skills/`。可显式调用 `/agent-eval-tutor`。需允许读取本地资料与运行 Python。
- **Workbuddy**：先使用该版本的本地 Skill 导入功能选择整个文件夹（如果支持）。安装路径、压缩包格式和触发方式需依据其当前官方文档确认；本项目不猜测路径。若只支持提示词而无法读文件/执行脚本，此包不能实现知识库功能。

不必同时安装到用户级和项目级，以免加载重复版本。各平台在当前会话维护问题计数；跨会话需由用户提供前情，不宣称持久记忆。

## 完成知识库的步骤

1. 对剩余失败来源运行 `crawl --retry-failed --exclude-domain mp.weixin.qq.com --max-pages 250` 重试（保留已成功的正文和手动导入文本）。
2. 审查覆盖清单：确认 FAQ、微信正文确实存在，直接链接逐项已收录或解释排除；给正文与 URL 抽样核验。
3. 检查文章抽取质量和中文/英文问题的检索召回。
4. 在每个宿主运行 `references/dialogue-checks.md` 中的对话用例。单元测试验证检索工具，不验证模型是否遵守三问规则。

源码与可下载的 Skill 压缩包在本仓库中维护。

来源完整清单在 `references/coverage.json`，可读目录在 `references/catalog.md`。下载包由整个 Skill 文件夹与说明组成，不含 Git 元数据或临时测试资料。

本轮补抓取的详细结果与仍缺失的链接见 [抓取报告](skills/agent-eval-tutor/references/fetch-report.md)。

微信正文导入后的验收说明见 [导入记录](skills/agent-eval-tutor/references/wechat-import.md)。
