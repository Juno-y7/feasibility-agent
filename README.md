# 产品可行性分析 Agent v2.0（通用版）

这是一个用于判断**任何产品或项目方案**是否可行的分析智能体包。

无论是硬件、SaaS、服务、内容、社群、平台还是 B2B 产品，它都能帮助你在投入大量资源之前，系统性地评估可行性。

## v2.0 更新亮点

- **完整HTML报告**：15章节深色主题报告，含Chart.js交互式图表（雷达图、柱状图、饼图）
- **多LLM支持**：OpenAI / Claude / DeepSeek / 通义千问 / 本地模型
- **健壮JSON解析**：自动修复大模型输出的常见JSON格式错误
- **CLI命令行工具**：支持文件分析、文本分析、交互式模式
- **零依赖降级**：sklearn/pandas缺失时自动回退到基础分析

## 核心能力

- **品类自动识别**：从资料中自动判断产品品类，切换评分权重和检查项
- **资料自动整理**：从零散资料中抽取结构化信息，不要求用户填表
- **多品类案例研究**：根据品类从不同来源回溯成功/失败案例（硬件→募资平台、SaaS→Product Hunt、社群→冷启动案例等）
- **弹性评分模型**：10 个通用维度，按品类调整权重，保持 100 分制
- **SWOT + 反方审查**：每个判断标注影响程度、证据强度和处理建议
- **可执行输出**：7 天验证任务 + 30 天推进计划 + 对外沟通话术

## 涵盖的品类

| 品类 | 评分侧重 | 案例来源 |
| --- | --- | --- |
| 🛠️ SaaS/效率工具 | 壁垒、商业模式、推广 | Product Hunt、SaaS 增长案例 |
| 📦 硬件/消费品 | 技术/生产可行性、供应链 | Kickstarter、嘖嘖、Indiegogo |
| 🤝 服务/咨询 | 团队匹配度、合规、证据 | 加盟案例、代运营增长 |
| 🧠 情感/内容/社群 | 留存、合规与伦理 | Patreon、Discord、社群案例 |
| 🏢 B2B/企业级 | 团队匹配度、合规、证据 | 企业 SaaS 增长、Gartner 报告 |
| 🌱 平台/双边市场 | 壁垒、推广、冷启动策略 | Airbnb/Uber 早期、网络效应研究 |
| 🤷 通用默认 | 均衡评估 | 根据资料灵活选择 |

## 使用方式

### 命令行工具（推荐）

```bash
# 从文件分析
python cli.py --file product_info.txt

# 从文本直接分析
python cli.py --text "产品名称：AI翻译耳机，目标用户：商务人士..."

# 交互模式
python cli.py --interactive

# 指定LLM提供商
python cli.py --file info.txt --llm deepseek
```

### LLM 配置

支持以下模型（通过环境变量配置）：

| 提供商 | 环境变量 | 默认模型 |
|--------|----------|----------|
| OpenAI | `OPENAI_API_KEY` | gpt-4o |
| Claude | `ANTHROPIC_API_KEY` | claude-3-sonnet |
| DeepSeek | `DEEPSEEK_API_KEY` | deepseek-chat |
| 通义千问 | `DASHSCOPE_API_KEY` | qwen-max |
| 本地模型 | 无需密钥 | localhost:8080 |

### 作为提示词使用

直接把项目资料发给 Agent，例如：

- 产品介绍
- 官网或营销页草稿
- Notion / 飞书 / Google Doc 内容
- PDF、PPT、Word 文档
- 竞品链接
- 聊天记录
- 老板或导师的反馈
- 零散想法

然后使用 `prompts/main-agent.md` 作为主提示词，让 Agent 自动完成：

1. 从原始资料中抽取产品信息。
2. 自动识别产品品类并切换评分模板。
3. 整理成结构化项目档案。
4. 标记缺失信息和关键假设。
5. 若资料足够，直接生成可行性报告。
6. 若资料不足，先问 3-7 个最关键的问题，再继续分析。

### 推荐命令

```text
我会直接发你一个准备上线的项目资料。请你按「产品可行性分析 Agent」工作：
1. 先自动整理资料，不要要求我手动填表。
2. 抽取产品定位、目标用户、痛点、功能、商业模式、证据和风险。
3. 自动判断品类并切换评分模板。
4. 如果信息不足，只问最关键的问题。
5. 然后输出完整可行性分析报告。
```

### 进阶用法

1. 把原始资料放进 `templates/raw-materials.md` 的格式中，或者直接粘贴给 Agent。
2. Agent 会先生成 `templates/extracted-intake.md` 这种结构化摘要。
3. 再按 `templates/report.md` 输出完整报告。
4. 若需要研究行业案例，用 `templates/case-study.md` 逐个拆解。
5. 每一轮分析后，用 `templates/iteration-log.md` 记录评分变化、假设变化和下一步任务。

## 目录结构

```text
feasibility-agent/
  prompts/
    main-agent.md            # 主提示词（通用版）
    critic-agent.md          # 反方审查提示词
    case-mining-agent.md     # 案例挖掘提示词
    direct-use.md            # 直接使用提示
  templates/
    raw-materials.md         # 原始资料整理模板
    extracted-intake.md      # 结构化摘要模板
    report.md                # 可行性报告模板（通用版）
    case-study.md            # 案例拆解模板（通用版）
    iteration-log.md         # 迭代日志模板
  research/
    crowdfunding-success-patterns.md  # 多品类案例研究笔记
  scoring-rubric.md          # 评分模型（含品类权重模板）
  reports/
    {product-name}/          # 每个产品的分析报告
```

## 判断原则

这个 Agent 的职责不是证明方案一定可行，而是尽早发现：

- 哪些优势是真的
- 哪些风险会拖垮项目
- 哪些地方必须补强
- 哪些假设应该立刻验证
- 是否适合进入 MVP、推广、募资或暂缓阶段
