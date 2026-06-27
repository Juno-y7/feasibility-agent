# 可行性分析报告渲染器设计文档

> 日期：2026-06-26
> 状态：已确认，待实现

## 1. 背景与目标

### 问题
- Python 代码中的评分模型、品类权重、增长飞轮等与 `main-agent.md` 提示词三重冗余
- Python 品类识别不准确
- 现有 `full_report_generator.py`（1800+ 行）维护困难
- 数据分散在代码、模板、提示词三处，容易不同步

### 目标
- **LLM 做分析**（准确）→ 输出结构化 JSON
- **前端做渲染**（快速）→ 粘贴 JSON 即出 HTML 报告
- **单一数据源**：`main-agent.md` 提示词
- **零 Python 依赖**：打开浏览器就能用

## 2. 架构

```
用户 → 把产品资料发给 LLM（main-agent.md 提示词）
         ↓
      LLM 输出结构化 JSON（按 report-schema.json 格式）
         ↓
      用户把 JSON 粘贴到 report-renderer/index.html
         ↓
      浏览器渲染出完整 HTML 报告（玻璃拟态风格 + Chart.js 图表）
```

## 3. 报告结构（18 章）— 按阅读逻辑排列

### 封面页
- 产品名称、分析日期、可行性评级、一句话结论
- 免责声明

### 第一部分：你是什么？（定位与现状）

| # | 章节ID | 名称 | 渲染方式 |
|---|--------|------|----------|
| 0 | `executive_summary` | 执行摘要 | 文字 + 关键指标卡片 |
| 1 | `project_profile` | 项目画像 | 文字 + 表格 |
| 7 | `case_studies` | 竞品案例研究 | 对比表格 + 可点击链接 |

### 第二部分：市场环境好不好？（外部分析）

| # | 章节ID | 名称 | 渲染方式 |
|---|--------|------|----------|
| 2 | `market_analysis` | 市场分析 | Chart.js 柱状图 + 文字 |
| 3 | `pest_analysis` | PEST 分析 | 2x2 网格卡片 |
| 4 | `porter_five_forces` | 波特五力 | 五力模型布局 |
| 5 | `swot_analysis` | SWOT 分析 | 2x2 四象限 + 详情列表 |

### 第三部分：怎么赚钱？（商业模式）

| # | 章节ID | 名称 | 渲染方式 |
|---|--------|------|----------|
| 6 | `business_model_canvas` | 商业模式画布 | 9 宫格画布 |
| 8 | `market_sizing` | 市场规模估算 | TAM/SAM/SOM 三层图 |
| 9 | `financial_model` | 财务模型 | Chart.js 趋势图 + 表格 |

### 第四部分：怎么增长？（运营策略）

| # | 章节ID | 名称 | 渲染方式 |
|---|--------|------|----------|
| 10 | `growth_flywheel` | 增长飞轮 | AARRR 漏斗图 + 飞轮图 |
| 14 | `timeline` | 时间规划 | 水平时间线 + 阶段卡片 |

### 第五部分：能不能做出来？（能力与风险）

| # | 章节ID | 名称 | 渲染方式 |
|---|--------|------|----------|
| 11 | `tech_architecture` | 技术架构评估 | 评估表格 + 风险标签 |
| 13 | `category_checks` | 品类特别检查 | 检查清单 + 状态标签（✓/✗/⚠） |

### 第六部分：评分与判断（结论区）

| # | 章节ID | 名称 | 渲染方式 |
|---|--------|------|----------|
| 16 | `risk_analysis` | 风险与失败模式 | 风险矩阵 + 5大失败模式 + 项目风险表 |
| 12 | `feasibility_score` | 可行性评分 | Chart.js 雷达图 + 评分明细表 |
| 15 | `exit_strategy` | 退出策略与止损 | 表格 + 阈值标签 |

### 第七部分：募资专项

| # | 章节ID | 名称 | 渲染方式 |
|---|--------|------|----------|
| 17 | `crowdfunding` | 募资可行性评估 | 平台对比表 + 募资评分 + 定价档位 |

## 4. JSON Schema 概要

```json
{
  "meta": {
    "generated_at": "2026-06-26T21:00:00",
    "product_name": "产品名称",
    "category": "hardware|saas|service|content|b2b|platform|community",
    "analyzer": "LLM model name",
    "schema_version": "2.0"
  },
  "executive_summary": {
    "one_line_summary": "一句话概括",
    "conclusion": "核心结论（2-3句）",
    "key_metrics": {
      "total_score": 75,
      "grade": "B",
      "grade_label": "建议补强后继续",
      "market_size_tam": "100亿",
      "market_size_sam": "10亿",
      "market_size_som": "1亿",
      "gross_margin_pct": 45,
      "payback_months": 12
    },
    "top_strengths": ["优势1", "优势2"],
    "top_risks": ["风险1", "风险2"],
    "recommendation": "下一步行动建议"
  },
  "project_profile": {
    "product_description": "产品描述",
    "target_users": ["用户群1", "用户群2"],
    "value_proposition": "核心价值主张",
    "core_features": ["功能1", "功能2"],
    "version_plan": [
      {"version": "MVP", "scope": "核心功能", "timeline": "3个月"},
      {"version": "V2", "scope": "扩展功能", "timeline": "6个月"}
    ]
  },
  "market_analysis": {
    "market_overview": "市场概述",
    "trends": [
      {"trend": "趋势名称", "description": "描述", "impact": "高/中/低"}
    ],
    "market_segments": [
      {"segment": "细分市场", "share_pct": 35, "growth_rate": "15%"}
    ]
  },
  "pest_analysis": {
    "political": {"label": "政治", "factors": ["因素1", "因素2"], "impact": "正面/负面/中性"},
    "economic": {"label": "经济", "factors": ["因素1", "因素2"], "impact": "正面/负面/中性"},
    "social": {"label": "社会", "factors": ["因素1", "因素2"], "impact": "正面/负面/中性"},
    "technological": {"label": "技术", "factors": ["因素1", "因素2"], "impact": "正面/负面/中性"}
  },
  "porter_five_forces": {
    "supplier_power": {"name": "供应商议价能力", "level": "高/中/低", "description": "描述"},
    "buyer_power": {"name": "购买者议价能力", "level": "高/中/低", "description": "描述"},
    "new_entrants": {"name": "新进入者威胁", "level": "高/中/低", "description": "描述"},
    "substitutes": {"name": "替代品威胁", "level": "高/中/低", "description": "描述"},
    "industry_rivalry": {"name": "行业竞争", "level": "高/中/低", "description": "描述"}
  },
  "swot_analysis": {
    "strengths": [
      {"item": "优势项", "impact": "高/中/低", "evidence": "证据", "action": "如何利用"}
    ],
    "weaknesses": [
      {"item": "劣势项", "impact": "高/中/低", "evidence": "证据", "action": "如何改进"}
    ],
    "opportunities": [
      {"item": "机会项", "impact": "高/中/低", "evidence": "证据", "action": "如何把握"}
    ],
    "threats": [
      {"item": "威胁项", "impact": "高/中/低", "evidence": "证据", "action": "如何应对"}
    ]
  },
  "business_model_canvas": {
    "value_proposition": "价值主张",
    "customer_segments": ["客户细分"],
    "channels": ["渠道"],
    "customer_relationships": ["客户关系"],
    "revenue_streams": [{"stream": "收入来源", "model": "模型", "pricing": "定价"}],
    "key_resources": ["核心资源"],
    "key_activities": ["核心活动"],
    "key_partnerships": ["关键伙伴"],
    "cost_structure": [{"cost": "成本项", "type": "固定/可变", "estimate": "估算金额"}]
  },
  "case_studies": {
    "similar_cases": [
      {
        "name": "案例名称",
        "platform": "kickstarter|zeczec|makuake|indiegogo|modian|flyingv",
        "amount": "1,000万",
        "backers": 5000,
        "success_factors": ["因素1", "因素2"],
        "relevance": "与本项目的相似点",
        "url": "https://..."
      }
    ]
  },
  "market_sizing": {
    "tam": {"label": "总市场", "value": "100亿", "description": "描述"},
    "sam": {"label": "可服务市场", "value": "10亿", "description": "描述"},
    "som": {"label": "可获得市场", "value": "1亿", "description": "描述"},
    "assumptions": ["假设1", "假设2"]
  },
  "financial_model": {
    "cost_structure": [
      {"item": "成本项", "type": "固定/可变", "monthly": 10000, "notes": "说明"}
    ],
    "revenue_model": [
      {"item": "收入来源", "unit_price": 299, "monthly_units": 100, "notes": "说明"}
    ],
    "break_even": {
      "months": 12,
      "monthly_revenue_needed": 50000,
      "description": "描述"
    },
    "projections": [
      {"month": "M1", "revenue": 0, "cost": 50000, "profit": -50000},
      {"month": "M6", "revenue": 30000, "cost": 40000, "profit": -10000},
      {"month": "M12", "revenue": 60000, "cost": 35000, "profit": 25000}
    ]
  },
  "growth_flywheel": {
    "flywheel_description": "增长飞轮描述",
    "aarrr": {
      "acquisition": {"name": "获客", "metrics": ["CAC", "渠道ROI"], "notes": "说明"},
      "activation": {"name": "激活", "metrics": ["首单转化率"], "notes": "说明"},
      "retention": {"name": "留存", "metrics": ["D1/D7/D30留存率"], "notes": "说明"},
      "revenue": {"name": "收入", "metrics": ["ARPU", "付费转化率"], "notes": "说明"},
      "referral": {"name": "推荐", "metrics": ["NPS", "病毒系数"], "notes": "说明"}
    }
  },
  "tech_architecture": {
    "tech_maturity": {"name": "技术成熟度", "level": "高/中/低", "notes": "说明"},
    "tech_complexity": {"name": "技术复杂度", "level": "高/中/低", "notes": "说明"},
    "supply_chain": {"name": "供应链可靠性", "level": "高/中/低", "notes": "说明"},
    "security": {"name": "安全合规", "level": "高/中/低", "notes": "说明"},
    "scalability": {"name": "扩展性", "level": "高/中/低", "notes": "说明"},
    "risk_level": "高/中/低",
    "notes": "补充说明"
  },
  "feasibility_score": {
    "category_weights": "hardware|saas|service|content|b2b|platform|default",
    "dimensions": [
      {"name": "痛点强度", "weight": 15, "score": 12, "max": 15, "notes": "评分理由"},
      {"name": "目标用户清晰度", "weight": 10, "score": 8, "max": 10, "notes": "评分理由"},
      {"name": "竞争壁垒", "weight": 10, "score": 6, "max": 10, "notes": "评分理由"},
      {"name": "产品可演示性", "weight": 10, "score": 7, "max": 10, "notes": "评分理由"},
      {"name": "技术/生产可行性", "weight": 10, "score": 5, "max": 10, "notes": "评分理由"},
      {"name": "合规与信任", "weight": 10, "score": 6, "max": 10, "notes": "评分理由"},
      {"name": "商业模式", "weight": 10, "score": 7, "max": 10, "notes": "评分理由"},
      {"name": "市场推广可行性", "weight": 10, "score": 5, "max": 10, "notes": "评分理由"},
      {"name": "团队匹配度", "weight": 10, "score": 5, "max": 10, "notes": "评分理由"},
      {"name": "证据完整度", "weight": 5, "score": 3, "max": 5, "notes": "评分理由"}
    ],
    "total_score": 64,
    "grade": "C",
    "grade_label": "需要重新定位"
  },
  "category_checks": {
    "category": "hardware",
    "checks": [
      {"item": "供应链韧性", "status": "pass|fail|warn", "notes": "说明"},
      {"item": "BOM成本与毛利", "status": "pass|fail|warn", "notes": "说明"},
      {"item": "开模周期", "status": "pass|fail|warn", "notes": "说明"},
      {"item": "物流与关税", "status": "pass|fail|warn", "notes": "说明"}
    ]
  },
  "timeline": {
    "phases": [
      {"phase": "验证期", "period": "0-3个月", "goal": "验证核心假设", "tasks": ["任务1", "任务2"], "success_criteria": "标准"},
      {"phase": "开发期", "period": "3-6个月", "goal": "开发MVP", "tasks": ["任务1", "任务2"], "success_criteria": "标准"},
      {"phase": "内测期", "period": "6-9个月", "goal": "小范围测试", "tasks": ["任务1", "任务2"], "success_criteria": "标准"},
      {"phase": "公测期", "period": "9-12个月", "goal": "公开测试", "tasks": ["任务1", "任务2"], "success_criteria": "标准"},
      {"phase": "规模化期", "period": "12个月+", "goal": "快速增长", "tasks": ["任务1", "任务2"], "success_criteria": "标准"}
    ]
  },
  "exit_strategy": {
    "options": [
      {"option": "被收购", "condition": "条件", "return": "回报", "risk": "风险"},
      {"option": "IPO", "condition": "条件", "return": "回报", "risk": "风险"}
    ],
    "stop_loss_triggers": [
      {"type": "财务止损", "indicator": "现金储备", "threshold": "低于3个月运营成本", "action": "缩减成本"},
      {"type": "用户止损", "indicator": "D7留存率", "threshold": "低于15%", "action": "重新评估产品"}
    ]
  },
  "risk_analysis": {
    "project_risks": [
      {"type": "竞争风险", "description": "描述", "level": "高/中/低", "mitigation": "应对措施"}
    ],
    "failure_patterns": [
      {"pattern": "供应链/履约失败", "frequency": "35%", "prevention": "预防措施", "relevance": "与本项目的关联"}
    ]
  },
  "crowdfunding": {
    "recommended_platform": "kickstarter",
    "platform_comparison": [
      {"platform": "kickstarter", "match_score": 85, "pros": ["优势1"], "cons": ["劣势1"], "fee": "5%+3%", "success_rate": "38%"},
      {"platform": "zeczec", "match_score": 70, "pros": ["优势1"], "cons": ["劣势1"], "fee": "5%+3%", "success_rate": "45%"}
    ],
    "crowdfunding_score": {
      "dimensions": [
        {"name": "产品展示力", "weight": 20, "score": 15, "max": 20},
        {"name": "信任证据", "weight": 20, "score": 10, "max": 20},
        {"name": "定价合理性", "weight": 15, "score": 10, "max": 15},
        {"name": "推广准备度", "weight": 15, "score": 8, "max": 15},
        {"name": "履约能力", "weight": 15, "score": 8, "max": 15},
        {"name": "平台匹配度", "weight": 15, "score": 10, "max": 15}
      ],
      "total_score": 61,
      "grade": "C",
      "grade_label": "需要大幅调整"
    },
    "pricing_strategy": [
      {"tier": "早鸟版", "price": 199, "limit": 100, "description": "基础功能"},
      {"tier": "标准版", "price": 299, "limit": 500, "description": "完整功能"},
      {"tier": "豪华版", "price": 499, "limit": 200, "description": "限量增值"}
    ],
    "supporter_estimates": {
      "target_amount": 500000,
      "avg_pledge": 250,
      "needed_supporters": 2000,
      "daily_target": 67,
      "campaign_days": 30
    },
    "delivery_plan": {
      "estimated_delivery": "6个月后",
      "milestones": [
        {"milestone": "原型完成", "date": "M1", "status": "待定"},
        {"milestone": "小批量生产", "date": "M3", "status": "待定"},
        {"milestone": "量产", "date": "M5", "status": "待定"}
      ]
    },
    "promotion_strategy": {
      "pre_launch": ["邮件列表500+订阅", "社交媒体KOL合作"],
      "during_campaign": ["首日冲刺策略", "每周更新", "互动回复"],
      "final_push": ["紧迫感营销", "追加福利"]
    }
  }
}
```

## 5. 文件结构

```
feasibility-agent/
├── prompts/
│   ├── main-agent.md              # 主提示词（含评分模型、品类权重等）
│   ├── critic-agent.md           # 反方审查
│   ├── case-mining-agent.md      # 案例挖掘
│   ├── crowdfunding-analysis-workflow.md  # 募资分析
│   └── direct-use.md             # 直接使用
├── data/
│   ├── competitors.json          # 竞品数据库
│   └── real_crowdfunding_cases.json  # 募资案例数据库
├── report-renderer/              # 纯前端渲染器（新增）
│   ├── index.html                # 主页面：JSON 输入 + 报告渲染
│   ├── schema/
│   │   └── report-schema.json    # JSON Schema 校验文件
│   └── README.md                 # 使用说明
├── reports/                      # 已生成的报告（保留）
├── examples/                     # 示例（保留）
├── AGENTS.md
└── README.md
```

## 6. 渲染器设计

### index.html 功能
- **上半部分**：JSON 输入区（textarea + 粘贴按钮）
- **下半部分**：实时渲染的报告预览
- **左侧导航**：18 章节固定导航栏（按 7 个部分分组）
- **图表**：Chart.js 渲染雷达图、趋势图、漏斗图等
- **三种导出**：
  - **下载 HTML**：完整的可交互 HTML 报告（可直接发客户）
  - **下载 Markdown**：纯文本 Markdown 格式（可复制编辑）
  - **导出 PDF**：调用浏览器 `window.print()`，选择"另存为 PDF"（Edge/Chrome 原生支持）

### 视觉风格
- 复用现有 `template.html` 的 glassmorphism 风格
- 深色主题（深蓝紫渐变背景）
- Tailwind CSS + Chart.js
- 响应式布局
- 封面页：产品名称居中、大号评级标签、日期和免责声明

### 渲染逻辑
1. 粘贴 JSON 后自动校验格式
2. 校验通过后按 schema 逐章渲染（按 7 部分顺序）
3. 每章独立渲染函数，互不干扰
4. JSON 字段缺失时显示"数据不足"提示而非报错
5. 渲染完成后可一键导出三种格式

## 7. 待删除的文件

| 文件 | 理由 |
|------|------|
| `tools/feasibility_agent.py` | 品类识别不准确，评分与提示词重复 |
| `tools/full_report_generator.py` | 硬编码数据与提示词冗余 |
| `tools/premium_report_generator.py` | 孤立文件，不在主流程 |
| `tools/generate_konglan_report.py` | 一次性脚本，无复用价值 |
| `tools/analysis_tool.py` | 简单公式，LLM 可直接计算 |
| `tools/agent_iteration_engine.py` | 迭代记录功能保留需求不大 |
| `tools/data_manager.py` | 独立 CLI，无其他文件引用 |
| `tools/zeczec_crawler.py` | 与核心流程解耦 |
| `tools/zeczec_playwright_crawler.py` | 与核心流程解耦 |
| `tools/competitor_analysis.py` | 爬虫功能保留但孤立 |
| `tools/llm_analyzer.py` | LLM 调用层（由用户直接与 LLM 交互替代） |
| `cli.py` | CLI 入口（不再需要） |
| `requirements.txt` | Python 依赖（不再需要） |
| `templates/web-report/` | 旧模板（被 report-renderer 替代） |
| `web-report/` | 旧报告（被 report-renderer 替代） |
| `tools/case-db/cases.json` | 空壳文件 |
| `tools/iterations/` | 迭代历史（不再需要） |
| `tools/extracted_product_info.txt` | 临时文件 |
| `publish/` | 发布配置（不再需要） |
