#!/usr/bin/env python3
import os
import json
from datetime import datetime
from typing import Dict, List, Any
from jinja2 import Environment, FileSystemLoader


class ReportGenerator:
    def __init__(self, templates_dir: str = None):
        if templates_dir is None:
            templates_dir = os.path.join(os.path.dirname(__file__), '../templates')
        self.templates_dir = os.path.abspath(templates_dir)
        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def generate_markdown_report(self, analysis_data: Dict) -> str:
        template = self.env.get_template('report.md')
        return template.render(**analysis_data)
    
    def generate_extracted_intake(self, intake_data: Dict) -> str:
        template = self.env.get_template('extracted-intake.md')
        return template.render(**intake_data)
    
    def generate_case_study(self, case_data: Dict) -> str:
        template = self.env.get_template('case-study.md')
        return template.render(**case_data)
    
    def generate_financial_model(self, financial_data: Dict) -> str:
        template = self.env.get_template('financial-model.md')
        return template.render(**financial_data)
    
    def generate_market_sizing(self, sizing_data: Dict) -> str:
        template = self.env.get_template('market-sizing.md')
        return template.render(**sizing_data)
    
    def generate_growth_flywheel(self, growth_data: Dict) -> str:
        template = self.env.get_template('growth-flywheel.md')
        return template.render(**growth_data)
    
    def generate_tech_architecture(self, tech_data: Dict) -> str:
        template = self.env.get_template('tech-architecture.md')
        return template.render(**tech_data)
    
    def generate_timeline_plan(self, timeline_data: Dict) -> str:
        template = self.env.get_template('timeline-plan.md')
        return template.render(**timeline_data)
    
    def generate_exit_strategy(self, exit_data: Dict) -> str:
        template = self.env.get_template('exit-strategy.md')
        return template.render(**exit_data)
    
    def generate_metrics_framework(self, metrics_data: Dict) -> str:
        template = self.env.get_template('metrics-framework.md')
        return template.render(**metrics_data)
    
    def generate_iteration_log(self, log_data: Dict) -> str:
        template = self.env.get_template('iteration-log.md')
        return template.render(**log_data)
    
    def generate_crowdfunding_analysis(self, cf_data: Dict) -> str:
        template = self.env.get_template('crowdfunding-analysis.md')
        return template.render(**cf_data)
    
    def generate_crowdfunding_copy(self, copy_data: Dict) -> str:
        template = self.env.get_template('crowdfunding-copy.md')
        return template.render(**copy_data)
    
    def generate_full_report(self, report_data: Dict) -> str:
        sections = []
        
        sections.append(f"# 可行性分析报告：{report_data.get('product', {}).get('name', '未命名产品')}")
        sections.append(f"\n> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        sections.append("## 1. 一句话判断")
        if report_data.get('scoring', {}).get('total_score'):
            score = report_data['scoring']['total_score']
            if score >= 80:
                sections.append("**值得继续投入** — 产品方向明确，可行性较高，可以进入正式开发/预热/推广阶段。")
            elif score >= 65:
                sections.append("**方向可行，但需补强** — 整体方向正确，但必须先补强2-3个关键短板。")
            elif score >= 50:
                sections.append("**需要重新定义** — 建议重新定义用户、场景或卖点后再评估。")
            else:
                sections.append("**暂不建议投入** — 风险较高，建议先验证核心假设。")
        else:
            sections.append("需要更多数据来做出判断。")
        
        if 'product' in report_data:
            p = report_data['product']
            sections.append("## 2. 产品理解")
            sections.append("### 产品定位")
            sections.append(p.get('description', '') or '待补充')
            sections.append("\n### 目标用户")
            sections.append(p.get('target_users', '') or '待补充')
            sections.append("\n### 核心价值")
            sections.append(p.get('value_proposition', '') or '待补充')
        
        if 'competitor_analysis' in report_data:
            ca = report_data['competitor_analysis']
            sections.append("## 3. 市场与竞品")
            if ca.get('competitors'):
                sections.append("| 竞品名称 | 品类 | 核心功能 | 价格 | 与本项目关系 |")
                sections.append("| --- | --- | --- | --- | --- |")
                for comp in ca['competitors'][:5]:
                    sections.append(f"| {comp.get('name', '')} | {comp.get('category', '')} | {comp.get('features', '')} | {comp.get('price', '')} | {comp.get('relation', '')} |")
            if ca.get('real_cases'):
                sections.append("\n### 相似成功案例")
                sections.append("| 案例名称 | 平台 | 金额 | 成功因素 |")
                sections.append("| --- | --- | --- | --- |")
                for case in ca['real_cases'][:3]:
                    factors = ', '.join(case.get('success_factors', [])[:3]) if case.get('success_factors') else ''
                    sections.append(f"| {case.get('name', '')} | {case.get('platform', '')} | {case.get('amount_raised', '')} | {factors} |")
        
        if 'scoring' in report_data:
            s = report_data['scoring']
            sections.append("## 4. 可行性评分")
            sections.append(f"**总分：{s.get('total_score', 0)}/100**（{s.get('rating', '')}）")
            sections.append("\n| 维度 | 权重 | 得分 | 说明 |")
            sections.append("| --- | ---: | ---: | --- |")
            if s.get('scores'):
                for dim, score_info in s['scores'].items():
                    sections.append(f"| {dim} | {score_info.get('weight', 0)} | {score_info.get('score', 0)} | {score_info.get('comment', '')} |")
            
            if s.get('strengths'):
                sections.append("\n### 最大优势")
                for st in s['strengths'][:3]:
                    sections.append(f"- {st}")
            
            if s.get('weaknesses'):
                sections.append("\n### 最大风险")
                for w in s['weaknesses'][:3]:
                    sections.append(f"- {w}")
        
        if 'financial_analysis' in report_data and report_data['financial_analysis']:
            f = report_data['financial_analysis']
            sections.append("## 5. 财务可行性")
            if f.get('pricing'):
                sections.append(f"- 建议零售价：¥{f['pricing'].get('retail_price', 0)}")
                sections.append(f"- 建议早鸟价：¥{f['pricing'].get('early_bird_price', 0)}")
            if f.get('breakeven'):
                sections.append(f"- 盈亏平衡所需支持者：{f['breakeven'].get('backers_needed', 0)}人")
                sections.append(f"- 平台费用（啧啧）：¥{f['platform_fees'].get('total_fee_cny', 0)}")
        
        if 'success_checklist' in report_data:
            checklist = report_data['success_checklist']
            sections.append("## 6. 成功因素检查")
            sections.append("| 检查项 | 状态 | 建议 |")
            sections.append("| --- | --- | --- |")
            for item in checklist[:10]:
                sections.append(f"| {item.get('item', '')} | {item.get('status', '')} | {item.get('suggestion', '')} |")
        
        sections.append("## 7. 7天验证任务")
        sections.append("| 任务 | 目的 | 产出 | 完成标准 |")
        sections.append("| --- | --- | --- | --- |")
        verify_tasks = [
            {"task": "用户访谈（5-10人）", "purpose": "验证痛点真实性和付费意愿", "output": "访谈记录", "criteria": "80%用户认同痛点"},
            {"task": "竞品深度分析", "purpose": "了解竞品优缺点", "output": "竞品分析报告", "criteria": "覆盖3-5个直接竞品"},
            {"task": "MVP原型制作", "purpose": "验证产品可演示性", "output": "产品原型/Demo", "criteria": "30秒内讲清价值"},
            {"task": "成本核算", "purpose": "确认成本结构", "output": "成本清单", "criteria": "毛利率>=50%"},
            {"task": "目标用户画像", "purpose": "明确第一批用户", "output": "用户画像文档", "criteria": "可执行的获客渠道"},
        ]
        for task in verify_tasks:
            sections.append(f"| {task['task']} | {task['purpose']} | {task['output']} | {task['criteria']} |")
        
        sections.append("\n## 8. 30天推进计划")
        sections.append("| 周期 | 重点 | 产出 |")
        sections.append("| --- | --- | --- |")
        plan_items = [
            {"period": "第1周", "focus": "产品定义与原型", "output": "MVP功能清单、产品原型"},
            {"period": "第2周", "focus": "市场验证与竞品", "output": "用户访谈报告、竞品分析"},
            {"period": "第3周", "focus": "财务与定价", "output": "财务模型、定价方案"},
            {"period": "第4周", "focus": "推广准备", "output": "预热计划、募资文案草稿"},
        ]
        for plan in plan_items:
            sections.append(f"| {plan['period']} | {plan['focus']} | {plan['output']} |")
        
        sections.append("\n## 9. 对外沟通话术")
        sections.append("### 给投资人")
        sections.append(f"我们正在做一款{report_data.get('product', {}).get('name', '')}，帮用户解决{report_data.get('product', {}).get('description', '')}的问题。目前已完成初步验证，可行性评分{report_data.get('scoring', {}).get('total_score', 0)}/100，计划通过{report_data.get('product', {}).get('platform', '募资平台')}进行募资，目标金额{report_data.get('product', {}).get('target_amount', '')}。")
        
        sections.append("\n### 给合作伙伴")
        sections.append(f"{report_data.get('product', {}).get('name', '')}是一款面向{report_data.get('product', {}).get('target_users', '')}的产品，核心价值在于{report_data.get('product', {}).get('value_proposition', '')}。我们正在寻找{report_data.get('product', {}).get('cooperation', '')}方面的合作伙伴，共同推动产品落地。")
        
        return '\n'.join(sections)
    
    def save_report(self, content: str, filename: str, reports_dir: str = None) -> str:
        if reports_dir is None:
            reports_dir = os.path.join(os.path.dirname(__file__), '../reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        safe_name = ''.join(c for c in filename if c.isalnum() or c in ('-', '_', ' ')).strip().replace(' ', '-')
        if not safe_name.endswith('.md'):
            safe_name += '.md'
        
        filepath = os.path.join(reports_dir, safe_name)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath


class HTMLReportGenerator:
    def __init__(self):
        self.css = """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .report-container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .report-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .report-header h1 {
            font-size: 28px;
            margin-bottom: 8px;
            font-weight: 600;
        }
        .report-header .subtitle {
            opacity: 0.9;
            font-size: 14px;
        }
        .score-badge {
            display: inline-block;
            margin-top: 20px;
            background: rgba(255,255,255,0.2);
            padding: 12px 30px;
            border-radius: 50px;
            font-size: 24px;
            font-weight: bold;
        }
        .report-body {
            padding: 40px;
        }
        .section {
            margin-bottom: 36px;
        }
        .section-title {
            color: #333;
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 2px solid #f0f0f0;
        }
        .section-title::before {
            content: '◆';
            color: #667eea;
            margin-right: 8px;
        }
        .highlight-box {
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }
        .highlight-box p {
            color: #333;
            line-height: 1.6;
            font-size: 15px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }
        th {
            background: #f8f9fa;
            padding: 12px 16px;
            text-align: left;
            font-weight: 600;
            color: #555;
            border-bottom: 2px solid #e9ecef;
        }
        td {
            padding: 12px 16px;
            border-bottom: 1px solid #e9ecef;
            color: #666;
        }
        tr:hover td {
            background: #f8f9fa;
        }
        .metric-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #f0f0f0;
        }
        .metric-label {
            color: #666;
        }
        .metric-value {
            font-weight: 600;
            color: #667eea;
        }
        .tag {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
            margin-right: 8px;
            margin-bottom: 8px;
        }
        .tag-success {
            background: #d4edda;
            color: #155724;
        }
        .tag-warning {
            background: #fff3cd;
            color: #856404;
        }
        .tag-danger {
            background: #f8d7da;
            color: #721c24;
        }
        .tag-info {
            background: #d1ecf1;
            color: #0c5460;
        }
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }
        .card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
        }
        .card-title {
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
        }
        .card-content {
            color: #666;
            font-size: 14px;
            line-height: 1.6;
        }
        .quote {
            font-style: italic;
            color: #888;
            padding: 16px 20px;
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            border-radius: 0 8px 8px 0;
            margin: 16px 0;
        }
        .progress-bar {
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
            margin: 8px 0;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 4px;
            transition: width 0.5s ease;
        }
        .score-detail {
            margin-bottom: 12px;
        }
        .score-bar {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 8px;
        }
        .score-label {
            flex: 1;
            font-size: 14px;
            color: #555;
        }
        .score-value {
            width: 40px;
            text-align: right;
            font-weight: 600;
            color: #667eea;
        }
        .footer {
            background: #f8f9fa;
            padding: 24px 40px;
            text-align: center;
            color: #999;
            font-size: 13px;
            border-top: 1px solid #e9ecef;
        }
        @media (max-width: 768px) {
            .grid-2 {
                grid-template-columns: 1fr;
            }
            .report-header {
                padding: 24px 20px;
            }
            .report-header h1 {
                font-size: 22px;
            }
            .report-body {
                padding: 24px 20px;
            }
            table {
                font-size: 12px;
            }
            th, td {
                padding: 8px 10px;
            }
        }
        """
    
    def generate_html(self, analysis_data: Dict) -> str:
        product = analysis_data.get('product', {})
        scoring = analysis_data.get('scoring', {})
        competitors = analysis_data.get('competitor_analysis', {}).get('competitors', [])
        real_cases = analysis_data.get('competitor_analysis', {}).get('real_cases', [])
        financials = analysis_data.get('financial_analysis', {})
        checklist = analysis_data.get('success_checklist', [])
        
        score = scoring.get('total_score', 0)
        rating = scoring.get('rating', '')
        
        if score >= 80:
            rating_text = "强烈推荐"
            rating_color = "#155724"
        elif score >= 65:
            rating_text = "建议补强后继续"
            rating_color = "#856404"
        elif score >= 50:
            rating_text = "需要重新定位"
            rating_color = "#dc3545"
        else:
            rating_text = "暂不建议投入"
            rating_color = "#6c757d"
        
        html_parts = []
        html_parts.append("<!DOCTYPE html>")
        html_parts.append("<html lang='zh-CN'>")
        html_parts.append("<head>")
        html_parts.append("<meta charset='UTF-8'>")
        html_parts.append("<meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        html_parts.append(f"<title>{product.get('name', '')} - 可行性分析报告</title>")
        html_parts.append(f"<style>{self.css}</style>")
        html_parts.append("</head>")
        html_parts.append("<body>")
        html_parts.append("<div class='report-container'>")
        
        html_parts.append("<div class='report-header'>")
        html_parts.append(f"<h1>{product.get('name', '未命名产品')}</h1>")
        html_parts.append(f"<div class='subtitle'>可行性分析报告 · {datetime.now().strftime('%Y-%m-%d')}</div>")
        html_parts.append(f"<div class='score-badge'>综合评分：{score}/100</div>")
        html_parts.append(f"<div style='margin-top: 10px; font-size: 14px; opacity: 0.9;'>{rating_text}</div>")
        html_parts.append("</div>")
        
        html_parts.append("<div class='report-body'>")
        
        html_parts.append("<div class='section'>")
        html_parts.append("<div class='section-title'>一句话判断</div>")
        if score >= 80:
            html_parts.append("<div class='highlight-box'><p><strong>值得继续投入</strong> — 产品方向明确，可行性较高，可以进入正式开发/预热/推广阶段。</p></div>")
        elif score >= 65:
            html_parts.append("<div class='highlight-box'><p><strong>方向可行，但需补强</strong> — 整体方向正确，但必须先补强2-3个关键短板。</p></div>")
        elif score >= 50:
            html_parts.append("<div class='highlight-box'><p><strong>需要重新定义</strong> — 建议重新定义用户、场景或卖点后再评估。</p></div>")
        else:
            html_parts.append("<div class='highlight-box'><p><strong>暂不建议投入</strong> — 风险较高，建议先验证核心假设。</p></div>")
        html_parts.append("</div>")
        
        html_parts.append("<div class='section'>")
        html_parts.append("<div class='section-title'>产品信息</div>")
        html_parts.append("<div class='grid-2'>")
        html_parts.append("<div class='card'>")
        html_parts.append("<div class='card-title'>产品描述</div>")
        html_parts.append(f"<div class='card-content'>{product.get('description', '待补充')}</div>")
        html_parts.append("</div>")
        html_parts.append("<div class='card'>")
        html_parts.append("<div class='card-title'>目标用户</div>")
        html_parts.append(f"<div class='card-content'>{product.get('target_users', '待补充')}</div>")
        html_parts.append("</div>")
        html_parts.append("</div>")
        html_parts.append("<div class='grid-2'>")
        html_parts.append("<div class='card'>")
        html_parts.append("<div class='card-title'>核心价值</div>")
        html_parts.append(f"<div class='card-content'>{product.get('value_proposition', '待补充')}</div>")
        html_parts.append("</div>")
        html_parts.append("<div class='card'>")
        html_parts.append("<div class='card-title'>目标平台</div>")
        html_parts.append(f"<div class='card-content'>{product.get('platform', '待补充')}</div>")
        html_parts.append("</div>")
        html_parts.append("</div>")
        html_parts.append("</div>")
        
        html_parts.append("<div class='section'>")
        html_parts.append("<div class='section-title'>评分详情</div>")
        if scoring.get('scores'):
            for dim, score_info in scoring['scores'].items():
                s = score_info.get('score', 0)
                w = score_info.get('weight', 0)
                html_parts.append("<div class='score-detail'>")
                html_parts.append(f"<div class='score-bar'><span class='score-label'>{dim}</span><span class='score-value'>{s}分</span></div>")
                html_parts.append(f"<div class='progress-bar'><div class='progress-fill' style='width: {s}%'></div></div>")
                html_parts.append(f"<div style='font-size: 12px; color: #999; margin-bottom: 8px;'>权重: {w}%</div>")
                html_parts.append("</div>")
        
        if scoring.get('strengths'):
            html_parts.append("<div style='margin-top: 20px;'>")
            html_parts.append("<h4 style='color: #155724; margin-bottom: 8px;'>★ 最大优势</h4>")
            for st in scoring['strengths'][:3]:
                html_parts.append(f"<div class='tag tag-success'>{st}</div>")
            html_parts.append("</div>")
        
        if scoring.get('weaknesses'):
            html_parts.append("<div style='margin-top: 12px;'>")
            html_parts.append("<h4 style='color: #dc3545; margin-bottom: 8px;'>⚠️ 最大风险</h4>")
            for w in scoring['weaknesses'][:3]:
                html_parts.append(f"<div class='tag tag-danger'>{w}</div>")
            html_parts.append("</div>")
        html_parts.append("</div>")
        
        html_parts.append("<div class='section'>")
        html_parts.append("<div class='section-title'>竞品分析</div>")
        if competitors:
            html_parts.append("<table>")
            html_parts.append("<tr><th>竞品名称</th><th>品类</th><th>价格</th><th>关系</th></tr>")
            for comp in competitors[:5]:
                html_parts.append(f"<tr><td>{comp.get('name', '')}</td><td>{comp.get('category', '')}</td><td>{comp.get('price', '')}</td><td>{comp.get('relation', '')}</td></tr>")
            html_parts.append("</table>")
        else:
            html_parts.append("<div style='color: #999; padding: 16px; background: #f8f9fa; border-radius: 8px;'>暂无竞品数据</div>")
        html_parts.append("</div>")
        
        html_parts.append("<div class='section'>")
        html_parts.append("<div class='section-title'>相似成功案例</div>")
        if real_cases:
            html_parts.append("<table>")
            html_parts.append("<tr><th>案例名称</th><th>平台</th><th>金额</th><th>成功因素</th></tr>")
            for case in real_cases[:3]:
                factors = ', '.join(case.get('success_factors', [])[:2]) if case.get('success_factors') else ''
                html_parts.append(f"<tr><td><a href='{case.get('platform_url', '#')}' target='_blank' style='color: #667eea;'>{case.get('name', '')}</a></td><td>{case.get('platform', '')}</td><td>{case.get('amount_raised', '')}</td><td>{factors}</td></tr>")
            html_parts.append("</table>")
        else:
            html_parts.append("<div style='color: #999; padding: 16px; background: #f8f9fa; border-radius: 8px;'>暂无案例数据</div>")
        html_parts.append("</div>")
        
        html_parts.append("<div class='section'>")
        html_parts.append("<div class='section-title'>财务可行性</div>")
        if financials:
            html_parts.append("<div class='grid-2'>")
            if financials.get('pricing'):
                html_parts.append("<div class='card'>")
                html_parts.append("<div class='card-title'>定价建议</div>")
                html_parts.append(f"<div class='metric-row'><span class='metric-label'>建议零售价</span><span class='metric-value'>¥{financials['pricing'].get('retail_price', 0)}</span></div>")
                html_parts.append(f"<div class='metric-row'><span class='metric-label'>建议早鸟价</span><span class='metric-value'>¥{financials['pricing'].get('early_bird_price', 0)}</span></div>")
                html_parts.append("</div>")
            if financials.get('breakeven'):
                html_parts.append("<div class='card'>")
                html_parts.append("<div class='card-title'>盈亏平衡</div>")
                html_parts.append(f"<div class='metric-row'><span class='metric-label'>所需支持者</span><span class='metric-value'>{financials['breakeven'].get('backers_needed', 0)}人</span></div>")
                html_parts.append(f"<div class='metric-row'><span class='metric-label'>平台费用</span><span class='metric-value'>¥{financials.get('platform_fees', {}).get('total_fee_cny', 0)}</span></div>")
                html_parts.append("</div>")
            html_parts.append("</div>")
        else:
            html_parts.append("<div style='color: #999; padding: 16px; background: #f8f9fa; border-radius: 8px;'>请提供成本和目标金额以计算财务可行性</div>")
        html_parts.append("</div>")
        
        html_parts.append("<div class='section'>")
        html_parts.append("<div class='section-title'>成功因素检查</div>")
        if checklist:
            html_parts.append("<table>")
            html_parts.append("<tr><th>检查项</th><th>状态</th></tr>")
            for item in checklist[:8]:
                status = item.get('status', '')
                if '高' in status or '强' in status:
                    status_class = 'tag-success'
                elif '中' in status:
                    status_class = 'tag-warning'
                else:
                    status_class = 'tag-danger'
                html_parts.append(f"<tr><td>{item.get('item', '')}</td><td><div class='tag {status_class}'>{status}</div></td></tr>")
            html_parts.append("</table>")
        html_parts.append("</div>")
        
        html_parts.append("<div class='section'>")
        html_parts.append("<div class='section-title'>7天验证任务</div>")
        verify_tasks = [
            {"task": "用户访谈（5-10人）", "purpose": "验证痛点真实性和付费意愿", "output": "访谈记录", "criteria": "80%用户认同痛点"},
            {"task": "竞品深度分析", "purpose": "了解竞品优缺点", "output": "竞品分析报告", "criteria": "覆盖3-5个直接竞品"},
            {"task": "MVP原型制作", "purpose": "验证产品可演示性", "output": "产品原型/Demo", "criteria": "30秒内讲清价值"},
            {"task": "成本核算", "purpose": "确认成本结构", "output": "成本清单", "criteria": "毛利率>=50%"},
            {"task": "目标用户画像", "purpose": "明确第一批用户", "output": "用户画像文档", "criteria": "可执行的获客渠道"},
        ]
        html_parts.append("<table>")
        html_parts.append("<tr><th>任务</th><th>目的</th><th>产出</th></tr>")
        for task in verify_tasks:
            html_parts.append(f"<tr><td>{task['task']}</td><td>{task['purpose']}</td><td>{task['output']}</td></tr>")
        html_parts.append("</table>")
        html_parts.append("</div>")
        
        html_parts.append("<div class='section'>")
        html_parts.append("<div class='section-title'>30天推进计划</div>")
        plan_items = [
            {"period": "第1周", "focus": "产品定义与原型", "output": "MVP功能清单、产品原型"},
            {"period": "第2周", "focus": "市场验证与竞品", "output": "用户访谈报告、竞品分析"},
            {"period": "第3周", "focus": "财务与定价", "output": "财务模型、定价方案"},
            {"period": "第4周", "focus": "推广准备", "output": "预热计划、募资文案草稿"},
        ]
        html_parts.append("<table>")
        html_parts.append("<tr><th>周期</th><th>重点</th><th>产出</th></tr>")
        for plan in plan_items:
            html_parts.append(f"<tr><td>{plan['period']}</td><td>{plan['focus']}</td><td>{plan['output']}</td></tr>")
        html_parts.append("</table>")
        html_parts.append("</div>")
        
        html_parts.append("<div class='section'>")
        html_parts.append("<div class='section-title'>对外沟通话术</div>")
        html_parts.append("<div class='grid-2'>")
        html_parts.append("<div class='card'>")
        html_parts.append("<div class='card-title'>给投资人</div>")
        html_parts.append(f"<div class='card-content'>我们正在做一款{product.get('name', '')}，帮用户解决{product.get('description', '')}的问题。目前已完成初步验证，可行性评分{score}/100，计划通过{product.get('platform', '募资平台')}进行募资，目标金额{product.get('target_amount', '')}。</div>")
        html_parts.append("</div>")
        html_parts.append("<div class='card'>")
        html_parts.append("<div class='card-title'>给合作伙伴</div>")
        html_parts.append(f"<div class='card-content'>{product.get('name', '')}是一款面向{product.get('target_users', '')}的产品，核心价值在于{product.get('value_proposition', '')}。我们正在寻找相关方面的合作伙伴，共同推动产品落地。</div>")
        html_parts.append("</div>")
        html_parts.append("</div>")
        html_parts.append("</div>")
        
        html_parts.append("</div>")
        
        html_parts.append("<div class='footer'>")
        html_parts.append("产品可行性分析智能体 · 分析报告")
        html_parts.append("</div>")
        
        html_parts.append("</div>")
        html_parts.append("</body>")
        html_parts.append("</html>")
        
        return '\n'.join(html_parts)
    
    def save_html(self, content: str, filename: str, reports_dir: str = None) -> str:
        if reports_dir is None:
            reports_dir = os.path.join(os.path.dirname(__file__), '../reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        safe_name = ''.join(c for c in filename if c.isalnum() or c in ('-', '_', ' ')).strip().replace(' ', '-')
        if not safe_name.endswith('.html'):
            safe_name += '.html'
        
        filepath = os.path.join(reports_dir, safe_name)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath


if __name__ == '__main__':
    sample_data = {
        'product': {
            'name': 'AI智能陪伴机器人',
            'description': '一款基于AI技术的情感陪伴机器人，具备语音交互、表情识别、个性化定制等功能',
            'target_users': '独居老人、儿童、情感需求人群',
            'value_proposition': '24小时陪伴，情感交流，个性化服务',
            'platform': '啧啧',
            'target_amount': '¥500,000',
            'cost': 300,
        },
        'scoring': {
            'total_score': 72,
            'rating': '方向可行，但需补强',
            'scores': {
                '痛点强度': {'weight': 15, 'score': 8, 'comment': '情感陪伴需求真实存在'},
                '目标用户清晰度': {'weight': 10, 'score': 7, 'comment': '用户群体明确'},
                '竞争壁垒': {'weight': 10, 'score': 5, 'comment': '技术壁垒一般'},
                '产品可演示性': {'weight': 10, 'score': 8, 'comment': 'Demo直观'},
                '技术可行性': {'weight': 10, 'score': 6, 'comment': 'AI技术成熟'},
                '合规与信任': {'weight': 10, 'score': 7, 'comment': '需关注隐私合规'},
                '商业模式': {'weight': 10, 'score': 7, 'comment': '定价合理'},
                '市场推广': {'weight': 10, 'score': 6, 'comment': '需要精准获客'},
                '团队匹配度': {'weight': 10, 'score': 7, 'comment': '团队有相关经验'},
                '证据完整度': {'weight': 5, 'score': 4, 'comment': '需要更多用户验证'},
            },
            'strengths': ['痛点真实明确', '产品演示性强', '定价合理'],
            'weaknesses': ['竞争壁垒不足', '获客难度较大', '隐私合规风险'],
        },
        'competitor_analysis': {
            'competitors': [
                {'name': 'Rokid Glasses', 'category': '智能穿戴/AR', 'price': '¥2999+', 'relation': '间接竞品'},
                {'name': 'Olivia AI', 'category': 'AI机器人', 'price': '¥1500+', 'relation': '直接竞品'},
                {'name': 'Memo AI', 'category': '银发科技', 'price': '¥899+', 'relation': '间接竞品'},
            ],
            'real_cases': [
                {'name': '快點翻譯錄音機 WONDER Pro', 'platform': '啧啧', 'amount_raised': 'NT$23,209,044', 'platform_url': 'https://www.zeczec.com/projects/wonder-pro', 'success_factors': ['痛点明确', '产品形态直观', '定价合理']},
                {'name': 'TITANSHIELD 穩如鈦山', 'platform': '啧啧', 'amount_raised': 'NT$1,035万', 'platform_url': 'https://www.zeczec.com/projects/titanshield', 'success_factors': ['视觉冲击强', '品质感', '需求真实']},
            ],
        },
        'financial_analysis': {
            'pricing': {'retail_price': 899, 'early_bird_price': 599},
            'breakeven': {'backers_needed': 723},
            'platform_fees': {'total_fee_cny': 27500},
        },
        'success_checklist': [
            {'item': '痛点真实且高频', 'status': '高', 'suggestion': '继续验证用户付费意愿'},
            {'item': '产品可演示性强', 'status': '高', 'suggestion': '制作高质量Demo视频'},
            {'item': '团队匹配度', 'status': '中', 'suggestion': '补充AI技术人才'},
            {'item': '竞争壁垒', 'status': '低', 'suggestion': '考虑差异化定位'},
        ],
    }
    
    md_gen = ReportGenerator()
    md_report = md_gen.generate_full_report(sample_data)
    md_file = md_gen.save_report(md_report, 'AI智能陪伴机器人-可行性分析')
    print(f"Markdown报告已保存: {md_file}")
    
    html_gen = HTMLReportGenerator()
    html_report = html_gen.generate_html(sample_data)
    html_file = html_gen.save_html(html_report, 'AI智能陪伴机器人-可行性分析')
    print(f"HTML报告已保存: {html_file}")
