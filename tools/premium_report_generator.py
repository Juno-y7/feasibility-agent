#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高端可行性分析报告生成器 v5.0
整合：6维度分析框架 + 17个完整章节 + 竞品对比 + 风险矩阵 + 数据可视化
输出：Markdown / HTML / PDF 三种格式
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any


class PremiumReportGenerator:
    """高端报告生成器 - Markdown格式"""
    
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = os.path.dirname(__file__)
        self.base_dir = base_dir
        self._load_resources()
    
    def _load_resources(self):
        """加载所有分析框架资源"""
        self.scoring_model = self._get_scoring_model()
        self.growth_flywheels = self._get_growth_flywheels()
        self.metrics_frameworks = self._get_metrics_frameworks()
        self.tech_framework = self._get_tech_framework()
        self.timeline = self._get_timeline()
        self.exit_strategy = self._get_exit_strategy()
        self.market_data = self._get_market_data()
        self.category_checks = self._get_category_checks()
    
    def _get_scoring_model(self) -> Dict:
        return {
            'dimensions': [
                {'key': 'pain_point', 'name': '痛点强度', 'weight': 15, 'high': '高频高价值、用户已付费', 'low': '新鲜有趣、低频无付费'},
                {'key': 'user_clarity', 'name': '目标用户清晰度', 'weight': 10, 'high': '能找到第一批100人', 'low': '用户太泛'},
                {'key': 'moat', 'name': '竞争壁垒', 'weight': 10, 'high': '品牌/专利/网络效应', 'low': '任何人可复制'},
                {'key': 'demo_ability', 'name': '产品可演示性', 'weight': 10, 'high': '30秒看懂价值', 'low': '只能文字解释'},
                {'key': 'tech_feasibility', 'name': '技术/生产可行性', 'weight': 10, 'high': 'MVP路径清晰', 'low': '技术/供应链不确定'},
                {'key': 'compliance', 'name': '合规与信任', 'weight': 10, 'high': '隐私法规安全到位', 'low': '无合规设计'},
                {'key': 'business_model', 'name': '商业模式', 'weight': 10, 'high': '定价与价值匹配', 'low': '转化路径不清'},
                {'key': 'marketing', 'name': '市场推广可行性', 'weight': 10, 'high': '有冷启动路径', 'low': '只有发社交媒体'},
                {'key': 'team_fit', 'name': '团队匹配度', 'weight': 10, 'high': '背景与行业匹配', 'low': '能力严重错位'},
                {'key': 'evidence', 'name': '证据完整度', 'weight': 5, 'high': '有访谈原型付费证据', 'low': '只有想法'},
            ],
            'category_weights': {
                'saas': {'pain_point': 15, 'user_clarity': 10, 'moat': 10, 'demo_ability': 10, 'tech_feasibility': 8, 'compliance': 8, 'business_model': 10, 'marketing': 12, 'team_fit': 10, 'evidence': 7},
                'hardware': {'pain_point': 15, 'user_clarity': 10, 'moat': 8, 'demo_ability': 10, 'tech_feasibility': 15, 'compliance': 10, 'business_model': 12, 'marketing': 8, 'team_fit': 7, 'evidence': 5},
                'service': {'pain_point': 12, 'user_clarity': 10, 'moat': 8, 'demo_ability': 8, 'tech_feasibility': 5, 'compliance': 12, 'business_model': 12, 'marketing': 10, 'team_fit': 12, 'evidence': 11},
                'content': {'pain_point': 15, 'user_clarity': 10, 'moat': 8, 'demo_ability': 8, 'tech_feasibility': 5, 'compliance': 15, 'business_model': 8, 'marketing': 10, 'team_fit': 10, 'evidence': 11},
                'b2b': {'pain_point': 10, 'user_clarity': 8, 'moat': 10, 'demo_ability': 8, 'tech_feasibility': 10, 'compliance': 12, 'business_model': 10, 'marketing': 10, 'team_fit': 12, 'evidence': 10},
                'platform': {'pain_point': 12, 'user_clarity': 10, 'moat': 15, 'demo_ability': 8, 'tech_feasibility': 8, 'compliance': 12, 'business_model': 10, 'marketing': 12, 'team_fit': 8, 'evidence': 5},
            },
            'grade_levels': {
                'A': {'min': 80, 'label': '强烈推荐', 'action': '可进入正式开发/预热/募资阶段'},
                'B': {'min': 65, 'label': '建议补强后继续', 'action': '方向可行，需先补强2-3个关键短板'},
                'C': {'min': 50, 'label': '需要重新定位', 'action': '需重新定义用户、场景或卖点'},
                'D': {'min': 0, 'label': '暂不建议投入', 'action': '暂不建议投入大量资源'},
            }
        }
    
    def _get_growth_flywheels(self) -> Dict:
        return {
            'hardware': {'name': '硬件增长飞轮', 'cycle': '产品销售→口碑传播→用户增长→规模效应→成本降低→价格优势→更多销售', 'key_elements': ['产品质量', '口碑传播', '规模效应'], 'bottlenecks': ['首批用户获取', '供应链成本', '售后体系']},
            'saas': {'name': 'SaaS增长飞轮', 'cycle': '用户使用→数据积累→产品智能提升→用户粘性增强→用户推荐→更多用户→更多数据', 'key_elements': ['数据驱动优化', '用户粘性', '推荐机制'], 'bottlenecks': ['免费到付费转化', '用户留存', '竞品切换成本']},
            'service': {'name': '服务增长飞轮', 'cycle': '客户服务→满意度提升→口碑传播→新客户获取→规模扩大→服务能力增强→更好服务', 'key_elements': ['服务质量', '口碑传播', '规模扩张'], 'bottlenecks': ['服务标准化', '人才复制', '客户获取成本']},
            'content': {'name': '内容社群增长飞轮', 'cycle': '内容/互动→用户参与→社区活跃→更多内容→更多用户→更强社区', 'key_elements': ['优质内容', '社区活跃', '用户参与'], 'bottlenecks': ['内容生产门槛', '冷启动密度', 'UGC治理']},
            'b2b': {'name': 'B2B增长飞轮', 'cycle': '客户成功→续约与增购→口碑与案例→新客户获取→产品优化→更好的客户成功', 'key_elements': ['客户成功', '案例积累', '续约增购'], 'bottlenecks': ['决策周期长', 'POC转化率', '集成难度']},
            'platform': {'name': '平台增长飞轮', 'cycle': '供应方增长→交易体验提升→需求方增长→更多供应→更好体验→更多需求', 'key_elements': ['供需平衡', '交易体验', '网络效应'], 'bottlenecks': ['冷启动鸡生蛋', '信任机制', '防作弊']},
        }
    
    def _get_metrics_frameworks(self) -> Dict:
        return {
            'north_star': {
                'hardware': {'metric': '活跃用户数 × 客单价 × 复购率', 'desc': '衡量产品被使用和产生收入的能力'},
                'saas': {'metric': 'MRR（月经常性收入）', 'desc': '衡量订阅业务的健康度'},
                'service': {'metric': 'LTV（客户生命周期价值）', 'desc': '衡量服务的长期价值'},
                'content': {'metric': 'DAU（日活跃用户数）', 'desc': '衡量社区的活跃度和粘性'},
                'b2b': {'metric': 'ACV（年度合同价值）', 'desc': '衡量企业客户的价值'},
                'platform': {'metric': 'GMV（商品交易总额）', 'desc': '衡量平台的交易规模'},
            },
            'aarrr': {
                '获客(Acquisition)': {'metrics': ['CAC', '渠道ROI'], 'target': 'LTV/CAC >= 3'},
                '激活(Activation)': {'metrics': ['首单转化率', '核心功能使用率'], 'target': '-'},
                '留存(Retention)': {'metrics': ['D1/D7/D30留存率'], 'target': 'D1>=30%, D7>=15%, D30>=5%'},
                '收入(Revenue)': {'metrics': ['ARPU', '付费转化率', 'LTV'], 'target': '-'},
                '推荐(Referral)': {'metrics': ['NPS', '推荐转化率', '病毒系数'], 'target': '病毒系数 >= 1'},
            }
        }
    
    def _get_tech_framework(self) -> Dict:
        return {
            'dimensions': [
                {'name': '技术栈成熟度', 'high': '成熟稳定', 'low': '风险高'},
                {'name': '技术复杂度', 'high': '简单可实现', 'low': '极复杂'},
                {'name': '供应链可靠性', 'high': '供应稳定', 'low': '风险高'},
                {'name': '安全合规', 'high': '完全合规', 'low': '严重问题'},
                {'name': '扩展性', 'high': '扩展性强', 'low': '扩展性差'},
            ],
            'risk_levels': {
                'high': ['核心技术未验证', '供应链单一', '合规问题'],
                'medium': ['技术复杂度高', '依赖第三方服务'],
                'low': ['技术选型保守', '有替代方案'],
            }
        }
    
    def _get_timeline(self) -> Dict:
        return {
            'stages': [
                {'stage': '验证期', 'time': '0-3个月', 'goal': '验证核心假设', 'tasks': ['用户调研', '竞品分析', 'MVP定义', '原型测试'], 'success': '种子用户验证通过'},
                {'stage': '开发期', 'time': '3-6个月', 'goal': '开发MVP', 'tasks': ['技术架构', '核心功能', '测试修复'], 'success': 'MVP内部验收'},
                {'stage': '内测期', 'time': '6-9个月', 'goal': '小范围测试', 'tasks': ['内测招募', '反馈收集', '迭代优化'], 'success': '内测满意度达标'},
                {'stage': '公测期', 'time': '9-12个月', 'goal': '公开测试', 'tasks': ['用户扩展', '付费测试', '市场推广'], 'success': '商业模式验证'},
                {'stage': '规模化期', 'time': '12个月+', 'goal': '快速增长', 'tasks': ['规模扩大', '模式优化', '团队扩充'], 'success': '建立竞争壁垒'},
            ]
        }
    
    def _get_exit_strategy(self) -> Dict:
        return {
            'options': [
                {'option': '被收购', 'condition': '有收购意向方', 'timing': '有一定规模用户', 'return': '中-高', 'risk': '估值不确定'},
                {'option': 'IPO', 'condition': '达到上市标准', 'timing': '公司成熟财务健康', 'return': '高', 'risk': '周期长门槛高'},
                {'option': '股权转让', 'condition': '找到接盘方', 'timing': '创始人想退出', 'return': '中', 'risk': '流动性差'},
                {'option': '停业清算', 'condition': '无法继续运营', 'timing': '资金耗尽', 'return': '低', 'risk': '损失投资'},
            ],
            'stop_loss': [
                {'type': '财务止损', 'indicator': '现金储备', 'threshold': '低于3个月运营成本', 'action': '紧急融资或缩减成本'},
                {'type': '财务止损', 'indicator': '收入增长', 'threshold': '连续3月低于目标50%', 'action': '重新评估商业模式'},
                {'type': '用户止损', 'indicator': 'D7留存率', 'threshold': '低于15%', 'action': '重新评估产品价值'},
                {'type': '用户止损', 'indicator': '付费转化率', 'threshold': '低于1%', 'action': '重新设计定价'},
                {'type': '运营止损', 'indicator': '团队流失率', 'threshold': '季度超30%', 'action': '审查企业文化'},
            ]
        }
    
    def _get_market_data(self) -> Dict:
        return {
            'ai_hardware': {
                'global_2026': '$800亿', 'china_2026': '¥2,000亿', 'growth': '35%',
                'ks_avg': '$50万-$100万', 'zeczec_avg': '¥500万-¥1,500万'
            }
        }
    
    def _get_category_checks(self) -> Dict:
        return {
            'hardware': ['供应链韧性：关键元器件是否受制于单一供应商？', 'BOM成本与定价的毛利空间是否合理？', '模具/开模周期和首批量产时间表是否现实？', '物流、关税、退货处理是否有预案？'],
            'saas': ['用户是否有持续使用理由，还是一次性体验？', '竞品的切换成本有多高？', 'API/基础设施依赖风险？', '免费tier到付费的转化路径是否清晰？'],
            'service': ['服务是否可标准化，还是只能靠人堆？', '单个客户的交付成本与收入是否可持续？', '规模化瓶颈在哪里？', '客户获取是否依赖个人关系？'],
            'content': ['伦理边界：是否涉及情感操控、防沉迷、未成年人保护？', '持续使用动机：用户为什么每天都回来？', '内容治理：UGC内容审核和风险如何管理？', '是否容易引发舆论风险或监管关注？'],
            'b2b': ['企业决策链长度和周期是否在可控范围？', 'POC到付费的转化率预期？', '合规认证（ISO、SOC2、信创等）是否必要？', '集成难度和客户IT支持能力是否匹配？'],
            'platform': ['先发哪一侧？冷启动的"鸡生蛋"问题如何解决？', '网络效应拐点在哪里？', '平台抽佣和定价机制是否合理？', '防止作弊和信任机制如何设计？'],
        }
    
    def generate_markdown(self, data: Dict) -> str:
        """生成完整的Markdown报告"""
        sections = []
        
        # 封面
        sections.append(self._md_cover(data))
        
        # 0. 执行摘要
        sections.append(self._md_executive_summary(data))
        
        # 维度一：产品与市场匹配
        sections.append(self._md_dimension_product_market(data))
        
        # 维度二：募资平台匹配
        sections.append(self._md_dimension_platform(data))
        
        # 维度三：财务可行性
        sections.append(self._md_dimension_financial(data))
        
        # 维度四：证据可信度
        sections.append(self._md_dimension_evidence(data))
        
        # 维度五：风险与合规
        sections.append(self._md_dimension_risk(data))
        
        # 维度六：行动路线图
        sections.append(self._md_dimension_roadmap(data))
        
        # 附录：评分详情
        sections.append(self._md_appendix_scoring(data))
        
        return '\n\n---\n\n'.join(sections)
    
    def _md_cover(self, data: Dict) -> str:
        product = data.get('product', {})
        scoring = data.get('scoring', {})
        score = scoring.get('total_score', 0)
        grade = scoring.get('grade', 'D')
        rating = scoring.get('rating', '')
        
        return f"""# {product.get('name', '未命名产品')}
## 产品可行性分析报告

| 项目 | 内容 |
|------|------|
| **产品名称** | {product.get('name', '-')} |
| **识别品类** | {data.get('category', '-')} |
| **分析日期** | {datetime.now().strftime('%Y年%m月%d日')} |
| **可行性评分** | **{score}/100** |
| **评级** | {grade} - {rating} |
| **报告版本** | v5.0 |

> 本报告由产品可行性分析智能体自动生成，基于6维度分析框架，包含17个详细章节。"""
    
    def _md_executive_summary(self, data: Dict) -> str:
        product = data.get('product', {})
        scoring = data.get('scoring', {})
        score = scoring.get('total_score', 0)
        grade = scoring.get('grade', 'D')
        rating = scoring.get('rating', '')
        rec = scoring.get('recommendation', '')
        
        strengths = scoring.get('strengths', [])[:3]
        weaknesses = scoring.get('weaknesses', [])[:3]
        
        return f"""# 0. 执行摘要

## 0.1 核心结论

**综合评分：{score}/100 | 评级：{grade} - {rating}**

**建议：{rec}**

## 0.2 关键指标一览

| 维度 | 状态 | 说明 |
|------|------|------|
| 产品与市场匹配 | {'良好' if score >= 65 else '待加强'} | 痛点强度、用户清晰度、市场规模 |
| 募资平台匹配 | {'良好' if score >= 60 else '待加强'} | 品类匹配、竞品表现、传播潜力 |
| 财务可行性 | {'良好' if score >= 60 else '待加强'} | 成本结构、毛利空间、盈亏平衡 |
| 证据可信度 | {'良好' if score >= 55 else '待加强'} | 原型状态、团队背景、第三方验证 |
| 风险与合规 | {'可控' if score >= 60 else '需关注'} | 交付风险、隐私合规、市场风险 |
| 行动路线 | 已规划 | 7天验证、30天推进、6个月路线 |

## 0.3 三大核心优势

{chr(10).join([f"- **{s}**" for s in strengths]) if strengths else "- 待补充"}

## 0.4 三大关键短板

{chr(10).join([f"- **{w}**" for w in weaknesses]) if weaknesses else "- 待补充"}

## 0.5 最紧急的验证任务

1. **用户访谈验证**：5-10位目标用户深度访谈，确认痛点真实性和付费意愿
2. **竞品深度对标**：找出3-5个直接竞品，分析其优劣势和差异化机会
3. **MVP原型演示**：制作最简可用原型，30秒内能讲清产品价值"""
    
    def _md_dimension_product_market(self, data: Dict) -> str:
        product = data.get('product', {})
        category = data.get('category', 'hardware')
        
        return f"""# 维度一：产品与市场匹配

## 1. 项目画像识别

### 1.1 品类识别
- **识别品类**：{category}
- **识别依据**：基于产品描述关键词智能匹配
- **品类评分侧重**：{self._get_category_focus(category)}

### 1.2 产品定位
| 项目 | 内容 |
|------|------|
| **产品名称** | {product.get('name', '-')} |
| **一句话描述** | {product.get('description', '-')[:100]} |
| **核心价值主张** | {product.get('value_proposition', '-')} |
| **目标用户** | {product.get('target_users', '-')} |
| **核心痛点** | {product.get('pain_points', '-')} |

### 1.3 品类特别检查项
{chr(10).join([f"- {c}" for c in self.category_checks.get(category, [])])}

## 2. 市场分析

### 2.1 PEST分析
| 维度 | 分析 | 影响程度 |
|------|------|----------|
| **政治(P)** | AI产业政策支持，数据安全法规趋严 | 中等正面 + 合规要求 |
| **经济(E)** | AI硬件市场年增长35%，消费升级趋势 | 高正面 |
| **社会(S)** | AI工具教育完成，用户接受度提升 | 高正面 |
| **技术(T)** | AI技术快速成熟，供应链体系完善 | 高正面 |

### 2.2 波特五力分析
| 力量 | 分析 | 强度 |
|------|------|------|
| 供应商议价能力 | AI芯片/核心模组供应商集中 | 高 |
| 购买者议价能力 | 消费者选择多，价格敏感度高 | 中 |
| 新进入者威胁 | 技术门槛降低，入局者增多 | 高 |
| 替代品威胁 | 手机APP、云端服务可替代部分功能 | 中 |
| 行业竞争程度 | 同质化产品多，竞争激烈 | 高 |

### 2.3 市场趋势
- **全球AI硬件市场**：{self.market_data['ai_hardware']['global_2026']}（年增长{self.market_data['ai_hardware']['growth']}）
- **中国AI硬件市场**：{self.market_data['ai_hardware']['china_2026']}
- **募资平台表现**：Kickstarter平均{self.market_data['ai_hardware']['ks_avg']}，啧啧平均{self.market_data['ai_hardware']['zeczec_avg']}

## 3. SWOT分析

### 3.1 优势 (Strengths)
| 条目 | 影响程度 | 证据强度 | 处理建议 |
|------|----------|----------|----------|
{self._format_swot_rows(data.get('swot', {}).get('strengths', []))}

### 3.2 劣势 (Weaknesses)
| 条目 | 影响程度 | 证据强度 | 处理建议 |
|------|----------|----------|----------|
{self._format_swot_rows(data.get('swot', {}).get('weaknesses', []))}

### 3.3 机会 (Opportunities)
| 条目 | 影响程度 | 证据强度 | 处理建议 |
|------|----------|----------|----------|
{self._format_swot_rows(data.get('swot', {}).get('opportunities', []))}

### 3.4 威胁 (Threats)
| 条目 | 影响程度 | 证据强度 | 处理建议 |
|------|----------|----------|----------|
{self._format_swot_rows(data.get('swot', {}).get('threats', []))}

## 4. 市场规模估算 (TAM/SAM/SOM)

| 指标 | 定义 | 估算值 | 依据 |
|------|------|--------|------|
| **TAM** | 总可寻址市场 | ¥100亿+ | 全球AI硬件/情感科技市场规模 |
| **SAM** | 可服务市场 | ¥10亿 | 目标地区+目标人群细分市场 |
| **SOM** | 可获得市场 | ¥5,000万-1亿 | 1-3年预期可获取的市场份额 |

**市场规模评分：7/10** - 市场空间足够大，但细分赛道竞争激烈

## 5. 用户洞察分析

### 5.1 核心用户画像
| 用户类型 | 典型特征 | 核心诉求 | 付费意愿 |
|---------|---------|---------|---------|
{self._format_user_personas(data.get('user_insights', {}).get('personas', []))}

### 5.2 用户旅程地图
| 阶段 | 用户行为 | 接触点 | 关键痛点 | 机会点 |
|------|---------|--------|---------|--------|
{self._format_user_journey(data.get('user_insights', {}).get('journey', []))}

### 5.3 典型使用场景
{self._format_use_cases(data.get('user_insights', {}).get('use_cases', []))}

### 5.4 用户洞察成熟度评分
**评分：{data.get('user_insights', {}).get('score', '待评估')}/10**
{self._format_user_insight_summary(data.get('user_insights', {}))}

## 6. 产品定义与MVP

### 6.1 功能优先级矩阵（MoSCoW方法）
| 优先级 | 功能模块 | 具体功能 | 说明 |
|--------|---------|---------|------|
{self._format_moscow_features(data.get('product_definition', {}).get('moscow_features', []))}

### 6.2 MVP范围建议
{self._format_mvp_scope(data.get('product_definition', {}).get('mvp_scope', {}))}

### 6.3 产品路线图
| 阶段 | 时间 | 核心目标 | 关键功能 |
|------|------|---------|---------|
{self._format_product_roadmap(data.get('product_definition', {}).get('roadmap', []))}

### 6.4 产品定义清晰度评分
**评分：{data.get('product_definition', {}).get('score', '待评估')}/10**
{self._format_product_definition_summary(data.get('product_definition', {}))}"""
    
    def _md_dimension_platform(self, data: Dict) -> str:
        competitors = data.get('competitor_analysis', {}).get('competitors', [])
        real_cases = data.get('competitor_analysis', {}).get('real_cases', [])
        similar = data.get('similar_cases', [])
        
        return f"""# 维度二：募资平台匹配

## 5. 竞品案例研究

### 5.1 直接竞品分析
| 竞品名称 | 品类 | 核心功能 | 价格区间 | 募集金额 | 支持者 |
|----------|------|----------|----------|----------|--------|
{self._format_competitor_rows(competitors[:5])}

### 5.2 相似成功案例
| 项目名称 | 平台 | 募集金额 | 支持者 | 达成率 | 成功关键因素 |
|----------|------|----------|--------|--------|--------------|
{self._format_real_case_rows(real_cases[:5])}

### 5.3 成功因素提炼
基于案例库分析，高成功概率项目通常具备：

1. **刚需痛点明确**：解决用户真实存在且愿意付费的问题
2. **视觉冲击力强**：产品外观/演示视频有传播力和记忆点
3. **价格带合理**：处于平台用户可接受的甜蜜区间
4. **团队可信度高**：有相关经验或背书，降低履约风险
5. **预热充分**：上线前已有种子用户和社群基础

### 5.4 失败风险预警
常见失败模式包括：
- 痛点模糊，产品"为了AI而AI"
- 定价过高或过低，偏离平台用户习惯
- 团队缺乏相关经验，履约风险不可控
- 产品过于复杂，MVP定义不清
- 缺乏传播点，纯靠平台自然流量

## 6. 产品演示力评估（新增）

### 6.1 演示力评估矩阵
| 评估维度 | 评估项 | 得分 | 说明 |
|---------|--------|------|------|
{self._format_demo_evaluation(data.get('demo_evaluation', {}).get('dimensions', []))}

### 6.2 演示素材清单
| 素材类型 | 当前状态 | 优先级 | 建议 |
|---------|----------|--------|------|
{self._format_demo_assets(data.get('demo_evaluation', {}).get('assets', []))}

### 6.3 演示力总评
**综合演示力评分：{data.get('demo_evaluation', {}).get('score', '待评估')}/10**
{self._format_demo_summary(data.get('demo_evaluation', {}))}

## 7. 众筹策略专项（新增）

### 7.1 档位设计建议
| 档位类型 | 价格区间 | 核心权益 | 限量策略 |
|---------|---------|---------|---------|
{self._format_tier_design(data.get('crowdfunding_strategy', {}).get('tiers', []))}

### 7.2 预热节奏规划
| 阶段 | 时间 | 核心动作 | 目标 |
|------|------|---------|------|
{self._format_preheat_timeline(data.get('crowdfunding_strategy', {}).get('preheat_timeline', []))}

### 7.3 推广渠道策略
| 渠道类型 | 具体渠道 | 投入预算 | 预期效果 |
|---------|---------|---------|---------|
{self._format_promotion_channels(data.get('crowdfunding_strategy', {}).get('channels', []))}

### 7.4 KOL/媒体合作清单
| 合作类型 | 目标对象 | 合作方式 | 优先级 |
|---------|---------|---------|--------|
{self._format_kol_partners(data.get('crowdfunding_strategy', {}).get('kol_partners', []))}

### 7.5 众筹策略总评
**众筹策略成熟度：{data.get('crowdfunding_strategy', {}).get('score', '待评估')}/10**
{self._format_crowdfunding_summary(data.get('crowdfunding_strategy', {}))}

## 8. 竞品对比分析

### 8.1 多维度竞品对比矩阵

| 对比维度 | 本项目 | 竞品A | 竞品B | 竞品C |
|----------|--------|-------|-------|-------|
| **核心功能** | 待评估 | - | - | - |
| **价格定位** | 待评估 | - | - | - |
| **目标用户** | 待评估 | - | - | - |
| **技术壁垒** | 待评估 | - | - | - |
| **品牌影响力** | 待评估 | - | - | - |
| **用户体验** | 待评估 | - | - | - |
| **供应链成熟度** | 待评估 | - | - | - |
| **募资表现** | 待评估 | - | - | - |

### 8.2 差异化机会点
1. **差异化方向一**：待根据具体产品分析
2. **差异化方向二**：待根据具体产品分析
3. **差异化方向三**：待根据具体产品分析

### 8.3 平台匹配度评估
| 评估项 | 得分 | 说明 |
|--------|------|------|
| 品类匹配度 | 7/10 | AI硬件/情感科技赛道在募资平台表现活跃 |
| 价格带匹配 | 6/10 | 需验证定价是否符合平台用户消费习惯 |
| 视觉传播性 | 待评估 | 产品外观和演示视频的传播潜力 |
| 故事叙述性 | 待评估 | 产品背后的故事是否能打动人 |
| **综合匹配度** | **6.5/10** | 整体适合募资平台，需优化呈现方式 |"""
    
    def _md_dimension_financial(self, data: Dict) -> str:
        fin = data.get('financial_analysis', {})
        product = data.get('product', {})
        pricing = fin.get('pricing', {})
        revenue = fin.get('revenue', {})
        backers = fin.get('backers_needed', {})
        
        cost = product.get('cost', 300)
        target = product.get('target_amount', '500,000')
        retail = pricing.get('retail_price', cost * 2)
        margin = fin.get('margin', 50)
        
        return f"""# 维度三：财务可行性

## 7. 财务模型分析

### 7.1 募资目标与收入预测
| 指标 | 数值 | 说明 |
|------|------|------|
| 目标募资金额 | ¥{target} | 基于首批生产+营销需求 |
| 平台费率 | 约10-11% | 平台费8% + 支付手续费2-3% |
| 预计实际到手 | ¥{revenue.get('actual_revenue_cny', int(float(str(target).replace(',','')) * 0.89))} | 扣除平台费用后 |
| 预计支持者数量 | {backers.get('total_backers', '1,000')}人 | 基于平均单价估算 |
| 平均客单价 | ¥{retail} | 建议零售价 |

### 7.2 成本结构分析
| 成本类型 | 单台成本 | 占比 | 说明 |
|----------|----------|------|------|
| **硬件/BOM成本** | ¥{cost} | ~50% | 核心元器件、壳体、包装 |
| 制造成本 | ¥{int(cost*0.15)} | ~8% | 组装、测试、良率损耗 |
| 运输与物流 | ¥{int(cost*0.1)} | ~5% | 国内物流、国际物流、关税 |
| 营销与推广 | ¥{int(cost*0.3)} | ~17% | KOL、广告、社群运营 |
| 运营与管理 | ¥{int(cost*0.25)} | ~20% | 团队、办公、售后 |
| **总成本估算** | **¥{cost + int(cost*0.8)}** | **100%** | |

### 7.3 盈利分析
| 指标 | 数值 | 评估 |
|------|------|------|
| 毛利率 | {margin}% | {'良好' if margin >= 50 else '偏低' if margin >= 30 else '过低'} |
| 盈亏平衡点 | {fin.get('break_even_units', int(float(str(target).replace(',','')) * 0.3 / (retail * margin / 100)))}台 | 需卖出这么多台才能覆盖固定成本 |
| 预计回收期 | 12-18个月 | 基于月净利润估算 |
| LTV/CAC | 待测算 | 目标 >= 3 |

### 7.4 财务健康度评分
**综合评分：6.5/10**

- 毛利率处于合理区间
- 盈亏平衡可实现，但有一定压力
- 现金流管理是关键，需严格控制成本

## 8. 商业模式画布

| 模块 | 内容 |
|------|------|
| **价值主张** | {product.get('value_proposition', '待补充')} |
| **客户细分** | {product.get('target_users', '待补充')} |
| **渠道通路** | 募资平台、社交媒体、KOL合作、社群运营 |
| **客户关系** | 社群运营、用户反馈闭环、持续迭代更新 |
| **收入来源** | 产品销售收入、后续配件/耗材、订阅服务（可选） |
| **核心资源** | 技术团队、供应链资源、品牌、用户社群 |
| **关键业务** | 产品研发、生产制造、市场推广、用户运营 |
| **重要合作** | 元器件供应商、代工厂、分销渠道、技术合作伙伴 |
| **成本结构** | 硬件成本、研发成本、营销成本、运营成本 |"""
    
    def _md_dimension_evidence(self, data: Dict) -> str:
        product = data.get('product', {})
        category = data.get('category', 'hardware')
        tech = self.tech_framework
        
        return f"""# 维度四：证据可信度

## 9. 技术架构评估

### 9.1 技术可行性分析
| 评估维度 | 当前状态 | 风险等级 | 应对建议 |
|----------|----------|----------|----------|
| 技术栈成熟度 | 待评估 | - | 需详细盘点技术选型 |
| 技术复杂度 | 待评估 | - | 需评估开发难度和周期 |
| 供应链可靠性 | 待评估 | - | 需核实供应商和交期 |
| 安全合规性 | 待评估 | - | 需排查隐私/法规风险 |
| 系统扩展性 | 待评估 | - | 需考虑用户增长后的扩展 |

### 9.2 技术风险清单
- **高风险项**：{', '.join(tech['risk_levels']['high'])}
- **中风险项**：{', '.join(tech['risk_levels']['medium'])}
- **低风险项**：{', '.join(tech['risk_levels']['low'])}

### 9.3 MVP技术路线
- **MVP核心功能**：{product.get('mvp_features', '待定义')}
- **技术架构选型**：{product.get('tech_stack', '待评估')}
- **预计开发周期**：{product.get('dev_cycle', '3-6个月')}
- **关键技术难点**：待识别和验证

## 10. 团队与证据评估

### 10.1 团队匹配度评估
| 评估项 | 状态 | 说明 |
|--------|------|------|
| 行业经验 | 待评估 | 团队是否有相关行业背景 |
| 技术能力 | 待评估 | 核心技术人员的能力和经验 |
| 产品能力 | 待评估 | 产品定义和迭代能力 |
| 运营能力 | 待评估 | 用户运营和增长能力 |
| 供应链能力 | 待评估 | 硬件类产品的供应链资源 |
| **综合匹配度** | **待评估** | |

### 10.2 证据完整度评估
| 证据类型 | 当前状态 | 重要性 |
|----------|----------|--------|
| 用户访谈记录 | 待补充 | 高 |
| 产品原型/Demo | 待补充 | 高 |
| 设计文档/技术方案 | 待补充 | 中 |
| 团队背景介绍 | 待补充 | 高 |
| 供应链意向书 | 待补充 | 中（硬件类高） |
| 预注册/意向用户 | 待补充 | 中 |
| 第三方背书/合作 | 待补充 | 中 |

### 10.3 交付计划可信度
| 里程碑 | 计划时间 | 可信度 |
|--------|----------|--------|
| 设计定稿 | 待确认 | - |
| 模具开发 | 待确认 | - |
| 首版样机 | 待确认 | - |
| 小批量试产 | 待确认 | - |
| 批量生产 | 待确认 | - |
| 发货交付 | 待确认 | - |"""
    
    def _md_dimension_risk(self, data: Dict) -> str:
        risks = data.get('risks', [])
        
        return f"""# 维度五：风险与合规

## 11. 风险矩阵（新增）

### 11.1 风险评估矩阵（概率 × 影响）

| | **低影响** | **中影响** | **高影响** |
|------|-----------|-----------|-----------|
| **高概率** | 需关注 | 优先级高 | **红灯区：必须规避** |
| **中概率** | 可接受 | 需监控 | **黄灯区：制定预案** |
| **低概率** | 可忽略 | 可接受 | **绿灯区：保险即可** |

### 11.2 已识别风险清单
| 风险类型 | 具体风险 | 发生概率 | 影响程度 | 风险等级 | 应对策略 |
|----------|----------|----------|----------|----------|----------|
| 技术风险 | 核心技术未达预期 | 中 | 高 | 高 | MVP验证、技术储备 |
| 供应链风险 | 元器件缺货/涨价 | 中 | 高 | 高 | 多供应商备选、提前备货 |
| 市场风险 | 竞品抢先发布 | 高 | 中 | 高 | 快速迭代、差异化定位 |
| 合规风险 | 数据隐私/法规问题 | 低 | 高 | 中 | 合规设计、法律咨询 |
| 履约风险 | 交付延期/质量问题 | 中 | 高 | 高 | 充足缓冲、严格品控 |
| 财务风险 | 资金链断裂 | 中 | 高 | 高 | 分阶段投入、预留缓冲 |
| 团队风险 | 核心人员流失 | 低 | 中 | 中 | 激励机制、知识沉淀 |

### 11.3 风险应对总策略
1. **预防优先**：在前期设计阶段就考虑风险规避
2. **预案前置**：对高风险项提前制定B计划
3. **快速响应**：建立风险监控机制，及时发现及时处理
4. **成本可控**：风险应对成本不超过风险本身的30%

## 12. 合规与信任

### 12.1 合规检查清单
- [ ] 数据隐私保护（个人信息保护法、GDPR等）
- [ ] 网络安全等级保护
- [ ] 产品质量标准（3C认证、CE、FCC等）
- [ ] 知识产权（专利、商标、著作权）
- [ ] 广告法合规（宣传话术、功能承诺）
- [ ] 用户协议和隐私政策
- [ ] 未成年人保护机制（如适用）

### 12.2 用户信任建设
- 透明的产品信息和进度更新
- 真实的团队背景和联系方式
- 第三方认证和背书
- 用户评价和案例展示
- 完善的售后保障政策"""
    
    def _md_dimension_roadmap(self, data: Dict) -> str:
        category = data.get('category', 'hardware')
        flywheel = self.growth_flywheels.get(category, self.growth_flywheels['hardware'])
        metrics = self.metrics_frameworks
        ns = metrics['north_star'].get(category, metrics['north_star']['hardware'])
        tl = self.timeline
        exit_s = self.exit_strategy
        
        return f"""# 维度六：行动路线图

## 13. 增长飞轮分析

### 13.1 {flywheel['name']}
**飞轮循环**：{flywheel['cycle']}

**关键环节**：{', '.join(flywheel['key_elements'])}

**增长瓶颈**：{', '.join(flywheel['bottlenecks'])}

### 13.2 增长阶段规划
| 阶段 | 用户规模 | 核心目标 | 主要策略 | 关键指标 |
|------|----------|----------|----------|----------|
| 冷启动期 | 0-1,000人 | 验证产品价值 | 种子用户测试、深度访谈 | 激活率、留存率、NPS |
| 增长期 | 1,000-10,000人 | 扩大用户规模 | 付费广告、内容营销、SEO | 用户增长率、CAC |
| 规模化期 | 10,000人+ | 建立竞争壁垒 | 网络效应、品牌建设、专利 | 市场份额、品牌认知度 |

## 14. 数据指标框架

### 14.1 北极星指标
- **指标**：{ns['metric']}
- **定义**：{ns['desc']}
- **当前值**：待设定
- **目标值**：待设定

### 14.2 AARRR漏斗指标
| 环节 | 关键指标 | 目标值 |
|------|----------|--------|
{chr(10).join([f"| {k} | {', '.join(v['metrics'])} | {v['target']} |" for k, v in metrics['aarrr'].items()])}

### 14.3 本品类特定指标
- **硬件类**：复购率、用户满意度、售后响应时间、良率
- **内容/社群类**：人均使用时长、UGC产出率、互动率
- **SaaS类**：MRR增长率、 churn率、NDR

## 15. 时间规划

### 15.1 项目五阶段路线图
| 阶段 | 时间 | 核心目标 | 关键任务 | 成功标准 |
|------|------|----------|----------|----------|
{chr(10).join([f"| {s['stage']} | {s['time']} | {s['goal']} | {', '.join(s['tasks'][:3])} | {s['success']} |" for s in tl['stages']])}

### 15.2 关键路径
- **最长任务链**：用户调研 → MVP开发 → 内测 → 公测 → 规模化
- **关键里程碑**：MVP完成、首次付费、盈亏平衡
- **资源需求**：{data.get('product', {}).get('team_size', '3-5人核心团队')}

## 16. 退出策略与止损机制

### 16.1 退出选项评估
| 退出方式 | 可行性 | 时机 | 预期回报 | 风险 |
|----------|--------|------|----------|------|
{chr(10).join([f"| {o['option']} | 待评估 | {o['timing']} | {o['return']} | {o['risk']} |" for o in exit_s['options']])}

### 16.2 止损触发条件
| 类型 | 监控指标 | 阈值 | 触发动作 |
|------|----------|------|----------|
{chr(10).join([f"| {c['type']} | {c['indicator']} | {c['threshold']} | {c['action']} |" for c in exit_s['stop_loss']])}

### 16.3 风险监控体系
- **监控频率**：每周财务复盘、每月用户指标复盘
- **预警机制**：设定黄线和红线两级预警
- **决策流程**：触发预警后24小时内启动评估

## 17. 行动建议与沟通话术

### 17.1 7天验证任务
| 任务 | 目的 | 产出 | 完成标准 |
|------|------|------|----------|
| 用户深度访谈（5-10人） | 验证痛点真实性和付费意愿 | 访谈记录+洞察报告 | 80%用户认同痛点 |
| 竞品深度分析（3-5个） | 了解竞品优劣势和差异化 | 竞品分析报告 | 完整的竞品对比矩阵 |
| MVP原型/演示视频 | 验证产品可演示性 | 原型/Demo/视频 | 30秒内讲清价值 |
| 详细成本核算 | 确认成本结构和毛利 | BOM成本清单 | 毛利率目标>=50% |
| 目标用户画像 | 明确第一批用户是谁 | 用户画像文档 | 有可执行的获客渠道 |

### 17.2 30天推进计划
| 周次 | 重点工作 | 产出物 |
|------|----------|--------|
| 第1周 | 产品定义与原型 | MVP功能清单、产品原型、用户故事 |
| 第2周 | 市场验证与用户 | 用户访谈报告、种子用户群、竞品分析 |
| 第3周 | 财务与供应链 | 财务模型、定价方案、供应商接触 |
| 第4周 | 推广准备 | 预热计划、募资文案、素材准备 |

### 17.3 关键短板补强建议
{chr(10).join([f"- **{w}**：制定专项补强计划" for w in data.get('need_improve', ['待补充'])[:5]])}

### 17.4 沟通话术

**给投资人（30秒电梯演讲）**：
> 我们正在做一款{data.get('product', {}).get('name', '')}，针对{data.get('product', {}).get('target_users', '')}的{data.get('product', {}).get('pain_points', '')}痛点。目前{data.get('product', {}).get('value_proposition', '')}，市场空间{self.market_data['ai_hardware']['china_2026']}。团队有相关背景，计划募资{data.get('product', {}).get('target_amount', '')}用于首批生产和推广。

**给合作伙伴**：
> {data.get('product', {}).get('name', '')}是一款面向{data.get('product', {}).get('target_users', '')}的创新产品，核心价值是{data.get('product', {}).get('value_proposition', '')}。我们正在寻找供应链/渠道/技术方面的合作伙伴，共同推动产品落地，实现互利共赢。

**给募资平台审核**：
> 本项目属于{data.get('category', '')}品类，已有产品原型和设计方案，团队具备相关行业经验。目标用户明确，痛点真实存在，商业模式清晰。预计募集{data.get('product', {}).get('target_amount', '')}，主要用于首批生产和市场推广。项目已完成前期调研，具备上线条件。"""
    
    def _md_appendix_scoring(self, data: Dict) -> str:
        scoring = data.get('scoring', {})
        dims = scoring.get('dimension_scores', [])
        
        rows = []
        for d in dims:
            rows.append(f"| {d.get('name', '')} | {d.get('score', 0)} | {d.get('weight', 0)}% | {d.get('weighted_score', 0)} | {d.get('comment', '待评估')} |")
        
        return f"""# 附录：可行性评分详情

## 评分明细表
| 维度 | 得分(0-100) | 权重 | 加权分 | 说明 |
|------|-------------|------|--------|------|
{chr(10).join(rows) if rows else '| 待补充 | - | - | - | - |'}

**总分：{scoring.get('total_score', 0)}/100**
**评级：{scoring.get('grade', 'D')} - {scoring.get('rating', '')}**

---
*本报告由产品可行性分析智能体 v5.0 自动生成*  
*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"""
    
    # ---------- 辅助方法 ----------
    def _get_category_focus(self, category: str) -> str:
        focuses = {
            'hardware': '技术/生产可行性、供应链、定价',
            'saas': '壁垒、商业模式、推广',
            'service': '团队匹配度、合规、证据',
            'content': '留存、合规与伦理',
            'b2b': '团队匹配度、合规、证据',
            'platform': '壁垒、推广、冷启动策略',
        }
        return focuses.get(category, '均衡评估')
    
    def _format_swot_rows(self, items: List) -> str:
        if not items:
            return "| 待补充 | - | - | - |"
        rows = []
        for item in items[:5]:
            if isinstance(item, dict):
                rows.append(f"| {item.get('item', '')} | {item.get('impact', '中')} | {item.get('evidence', '中')} | {item.get('suggestion', '关注')} |")
            else:
                rows.append(f"| {item} | 中 | 中 | 需验证 |")
        return '\n'.join(rows)
    
    def _format_competitor_rows(self, comps: List) -> str:
        if not comps:
            return "| 待补充 | - | - | - | - | - |"
        rows = []
        for c in comps[:5]:
            rows.append(f"| {c.get('name', '')} | {c.get('category', '')} | {c.get('features', '')[:30]} | {c.get('price', '-')} | {c.get('amount_raised', '-')} | {c.get('backers', '-')} |")
        return '\n'.join(rows)
    
    def _format_real_case_rows(self, cases: List) -> str:
        if not cases:
            return "| 待补充 | - | - | - | - | - |"
        rows = []
        for c in cases[:5]:
            factors = c.get('success_factors', [])
            factor_str = ', '.join(factors[:2]) if factors else '待分析'
            link = c.get('link', '')
            name = c.get('name', '')
            if link:
                name = f"[{name}]({link})"
            rows.append(f"| {name} | {c.get('platform', '-')} | {c.get('amount_raised', '-')} | {c.get('backers', '-')} | {c.get('success_rate', '-')} | {factor_str} |")
        return '\n'.join(rows)
    
    def _format_user_personas(self, personas: List) -> str:
        if not personas:
            return "| 待补充 | 待补充 | 待补充 | 待补充 |"
        rows = []
        for p in personas[:4]:
            rows.append(f"| **{p.get('type', '')}** | {p.get('characteristics', '')} | {p.get('needs', '')} | {p.get('willingness', '')} |")
        return '\n'.join(rows)
    
    def _format_user_journey(self, journey: List) -> str:
        if not journey:
            return "| 待补充 | 待补充 | 待补充 | 待补充 | 待补充 |"
        rows = []
        for j in journey[:6]:
            rows.append(f"| **{j.get('stage', '')}** | {j.get('behavior', '')} | {j.get('touchpoints', '')} | {j.get('pain_points', '')} | {j.get('opportunities', '')} |")
        return '\n'.join(rows)
    
    def _format_use_cases(self, cases: List) -> str:
        if not cases:
            return "待补充用户场景，建议通过用户访谈收集"
        items = []
        for i, c in enumerate(cases[:5], 1):
            items.append(f"{i}. **{c.get('title', '')}**：{c.get('description', '')}")
        return '\n'.join(items)
    
    def _format_user_insight_summary(self, insights: Dict) -> str:
        if not insights:
            return "待评估 - 需要补充用户调研数据"
        summary = insights.get('summary', [])
        if not summary:
            return "待评估"
        return '\n'.join([f"- {s}" for s in summary])
    
    def _format_moscow_features(self, features: List) -> str:
        if not features:
            return "| 待补充 | 待补充 | 待补充 | 待补充 |"
        rows = []
        for f in features[:12]:
            priority = f.get('priority', '')
            priority_label = {
                'must': 'Must Have（必须有）',
                'should': 'Should Have（应该有）',
                'could': 'Could Have（可以有）',
                'wont': "Won't Have（暂不做）"
            }.get(priority, priority)
            rows.append(f"| **{priority_label}** | {f.get('module', '')} | {f.get('feature', '')} | {f.get('description', '')} |")
        return '\n'.join(rows)
    
    def _format_mvp_scope(self, scope: Dict) -> str:
        if not scope:
            return "待补充 - 需要明确MVP功能范围"
        core = scope.get('core_features', [])
        enhanced = scope.get('enhanced_features', [])
        cut = scope.get('cut_features', [])
        timeline = scope.get('timeline', '待评估')
        
        parts = []
        if core:
            parts.append(f"- **核心功能（{len(core)}个）**：{', '.join(core)}")
        if enhanced:
            parts.append(f"- **增强功能（{len(enhanced)}个）**：{', '.join(enhanced)}")
        if cut:
            parts.append(f"- **砍掉功能（{len(cut)}个）**：{', '.join(cut)}")
        parts.append(f"\n**MVP开发周期估算：{timeline}**")
        return '\n'.join(parts)
    
    def _format_product_roadmap(self, roadmap: List) -> str:
        if not roadmap:
            return "| 待补充 | 待补充 | 待补充 | 待补充 |"
        rows = []
        for r in roadmap[:4]:
            rows.append(f"| {r.get('stage', '')} | {r.get('time', '')} | {r.get('goal', '')} | {r.get('features', '')} |")
        return '\n'.join(rows)
    
    def _format_product_definition_summary(self, definition: Dict) -> str:
        if not definition:
            return "待评估 - 需要补充产品定义文档"
        summary = definition.get('summary', [])
        if not summary:
            return "待评估"
        return '\n'.join([f"- {s}" for s in summary])
    
    def _format_demo_evaluation(self, dimensions: List) -> str:
        if not dimensions:
            return "| 待补充 | 待补充 | 待评估 | 待补充 |"
        rows = []
        for d in dimensions[:8]:
            rows.append(f"| {d.get('dimension', '')} | {d.get('item', '')} | {d.get('score', '待评估')} | {d.get('description', '')} |")
        return '\n'.join(rows)
    
    def _format_demo_assets(self, assets: List) -> str:
        if not assets:
            return "| 待补充 | 待补充 | 待补充 | 待补充 |"
        rows = []
        for a in assets[:8]:
            rows.append(f"| {a.get('type', '')} | {a.get('status', '待补充')} | {a.get('priority', '中')} | {a.get('suggestion', '')} |")
        return '\n'.join(rows)
    
    def _format_demo_summary(self, demo: Dict) -> str:
        if not demo:
            return "待评估 - 需要补充产品演示素材和评估"
        summary = demo.get('summary', [])
        if not summary:
            return "待评估"
        return '\n'.join([f"- {s}" for s in summary])
    
    def _format_tier_design(self, tiers: List) -> str:
        if not tiers:
            return "| 待补充 | 待补充 | 待补充 | 待补充 |"
        rows = []
        for t in tiers[:6]:
            rows.append(f"| **{t.get('name', '')}** | {t.get('price', '')} | {t.get('benefits', '')} | {t.get('limit', '')} |")
        return '\n'.join(rows)
    
    def _format_preheat_timeline(self, timeline: List) -> str:
        if not timeline:
            return "| 待补充 | 待补充 | 待补充 | 待补充 |"
        rows = []
        for t in timeline[:5]:
            rows.append(f"| **{t.get('stage', '')}** | {t.get('time', '')} | {t.get('actions', '')} | {t.get('goal', '')} |")
        return '\n'.join(rows)
    
    def _format_promotion_channels(self, channels: List) -> str:
        if not channels:
            return "| 待补充 | 待补充 | 待补充 | 待补充 |"
        rows = []
        for c in channels[:6]:
            rows.append(f"| {c.get('type', '')} | {c.get('channels', '')} | {c.get('budget', '')} | {c.get('expected_effect', '')} |")
        return '\n'.join(rows)
    
    def _format_kol_partners(self, partners: List) -> str:
        if not partners:
            return "| 待补充 | 待补充 | 待补充 | 待补充 |"
        rows = []
        for p in partners[:6]:
            rows.append(f"| {p.get('type', '')} | {p.get('target', '')} | {p.get('cooperation', '')} | {p.get('priority', '')} |")
        return '\n'.join(rows)
    
    def _format_crowdfunding_summary(self, strategy: Dict) -> str:
        if not strategy:
            return "待评估 - 需要补众筹策略规划"
        summary = strategy.get('summary', [])
        if not summary:
            return "待评估"
        return '\n'.join([f"- {s}" for s in summary])


class PremiumHTMLGenerator:
    """高端HTML报告生成器 - 玻璃态设计 + 完整交互"""
    
    def __init__(self):
        pass
    
    def generate_html(self, data: Dict) -> str:
        """生成完整HTML报告"""
        product = data.get('product', {})
        scoring = data.get('scoring', {})
        score = scoring.get('total_score', 0)
        grade = scoring.get('grade', 'D')
        rating = scoring.get('rating', '')
        name = product.get('name', '未命名产品')
        
        dims = scoring.get('dimension_scores', [])
        score_labels = [d.get('name', '') for d in dims]
        score_values = [d.get('score', 0) for d in dims]
        score_weights = [d.get('weight', 0) for d in dims]
        
        strengths = scoring.get('strengths', [])[:3]
        weaknesses = scoring.get('weaknesses', [])[:3]
        category = data.get('category', 'hardware')
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - 产品可行性分析报告</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ font-family: 'Noto Sans SC', sans-serif; }}
        body {{
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            min-height: 100vh;
            color: #e4e4e7;
        }}
        .glass-card {{
            background: rgba(30, 30, 46, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            transition: all 0.3s ease;
        }}
        .glass-card:hover {{ border-color: rgba(96, 165, 250, 0.2); }}
        .gradient-text {{
            background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .nav-item {{ transition: all 0.3s ease; cursor: pointer; }}
        .nav-item:hover {{ background: rgba(96, 165, 250, 0.15); transform: translateX(4px); }}
        .nav-item.active {{ background: rgba(96, 165, 250, 0.2); border-left: 3px solid #60a5fa; }}
        .section-header {{ position: relative; }}
        .section-header::after {{
            content: '';
            position: absolute;
            bottom: -8px;
            left: 0;
            width: 60px;
            height: 3px;
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            border-radius: 2px;
        }}
        .tag {{ padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 500; }}
        .tag-excellent {{ background: rgba(34, 197, 94, 0.2); color: #4ade80; }}
        .tag-good {{ background: rgba(96, 165, 250, 0.2); color: #93c5fd; }}
        .tag-normal {{ background: rgba(251, 191, 36, 0.2); color: #fcd34d; }}
        .tag-poor {{ background: rgba(249, 115, 22, 0.2); color: #fdba74; }}
        .tag-risk {{ background: rgba(239, 68, 68, 0.2); color: #fca5a5; }}
        .scrollbar-hide::-webkit-scrollbar {{ display: none; }}
        .scrollbar-hide {{ -ms-overflow-style: none; scrollbar-width: none; }}
        .dimension-card {{
            background: rgba(96, 165, 250, 0.05);
            border: 1px solid rgba(96, 165, 250, 0.2);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
        }}
        .dimension-bar {{
            height: 6px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
            overflow: hidden;
        }}
        .dimension-fill {{
            height: 100%;
            border-radius: 3px;
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            transition: width 1s ease;
        }}
        .collapsible {{ cursor: pointer; user-select: none; }}
        .collapsible-content {{ 
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.5s ease;
        }}
        .collapsible-content.open {{ max-height: 5000px; }}
        .chevron {{ transition: transform 0.3s ease; }}
        .chevron.rotated {{ transform: rotate(180deg); }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .fade-in {{ animation: fadeIn 0.5s ease forwards; }}
        @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
        .loader {{ border: 3px solid rgba(255,255,255,0.1); border-top-color: #60a5fa; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; }}
        .loading-overlay {{ position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%); display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 9999; transition: opacity 0.5s ease; }}
        .loading-overlay.hidden {{ opacity: 0; pointer-events: none; }}
        .hamburger-btn {{ display: none; background: rgba(255,255,255,0.1); border: none; border-radius: 8px; padding: 8px; cursor: pointer; }}
        .risk-matrix-cell {{
            border: 1px solid rgba(255,255,255,0.1);
            padding: 12px;
            text-align: center;
            font-size: 12px;
        }}
        .risk-high {{ background: rgba(239, 68, 68, 0.2); }}
        .risk-medium {{ background: rgba(251, 191, 36, 0.2); }}
        .risk-low {{ background: rgba(34, 197, 94, 0.2); }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ background: rgba(255,255,255,0.05); padding: 12px; text-align: left; font-weight: 500; font-size: 13px; color: #93c5fd; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        td {{ padding: 12px; font-size: 13px; color: #a1a1aa; border-bottom: 1px solid rgba(255,255,255,0.05); }}
        tr:hover td {{ background: rgba(255,255,255,0.02); }}
        .quote-box {{
            border-left: 3px solid #60a5fa;
            padding: 16px 20px;
            background: rgba(96, 165, 250, 0.05);
            border-radius: 0 12px 12px 0;
            margin: 16px 0;
            font-style: italic;
            color: #93c5fd;
        }}
        @media (max-width: 768px) {{
            .sidebar {{ position: fixed; left: -100%; transition: left 0.3s ease; z-index: 100; }}
            .sidebar.open {{ left: 0; }}
            .main-content {{ margin-left: 0 !important; padding: 16px !important; }}
            .hamburger-btn {{ display: block; position: fixed; top: 16px; left: 16px; z-index: 101; }}
            .grid-cols-2, .grid-cols-3, .grid-cols-4 {{ grid-template-columns: 1fr !important; }}
        }}
    </style>
</head>
<body class="flex">
    <div class="loading-overlay" id="loadingOverlay">
        <div class="loader"></div>
        <p class="text-gray-400 mt-4 text-sm">正在加载分析报告...</p>
    </div>
    
    <button class="hamburger-btn" onclick="document.querySelector('.sidebar').classList.toggle('open')">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
    </button>
    
    <!-- 侧边栏 -->
    <aside class="sidebar w-72 fixed left-0 top-0 h-screen bg-[#16162a]/95 backdrop-blur-xl border-r border-white/5 flex flex-col z-50">
        <div class="p-6 border-b border-white/5">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <path d="M12 6v6l4 2"></path>
                    </svg>
                </div>
                <div>
                    <h1 class="text-lg font-semibold text-white">可行性分析</h1>
                    <p class="text-xs text-gray-400">v5.0 · 6维度框架</p>
                </div>
            </div>
        </div>
        
        <div class="p-4 mx-4 mt-4 glass-card">
            <div class="flex items-center justify-center relative">
                <svg width="110" height="110" viewBox="0 0 100 100">
                    <defs>
                        <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#60a5fa" />
                            <stop offset="100%" stop-color="#a78bfa" />
                        </linearGradient>
                    </defs>
                    <circle cx="50" cy="50" r="42" fill="none" stroke-width="7" stroke="rgba(255,255,255,0.1)" />
                    <circle id="scoreCircle" cx="50" cy="50" r="42" fill="none" stroke-width="7" stroke="url(#scoreGradient)"
                            stroke-linecap="round" stroke-dasharray="264" stroke-dashoffset="264" />
                </svg>
                <div class="absolute inset-0 flex flex-col items-center justify-center">
                    <span id="scoreNum" class="text-3xl font-bold gradient-text">0</span>
                    <span class="text-xs text-gray-400">总分/100</span>
                </div>
            </div>
            <div class="text-center mt-3">
                <span class="tag {self._score_tag_class(score)}">{rating}</span>
                <p class="text-xs text-gray-400 mt-1">{self._grade_action(grade)}</p>
            </div>
        </div>
        
        <nav class="flex-1 overflow-y-auto p-4 scrollbar-hide">
            <div class="space-y-1">
                <div onclick="scrollToSection('section0')" class="nav-item w-full text-left px-4 py-3 rounded-lg text-sm font-medium text-gray-300 active">📋 执行摘要</div>
                <div onclick="scrollToSection('section1')" class="nav-item w-full text-left px-4 py-3 rounded-lg text-sm font-medium text-gray-400">🎯 产品与市场匹配</div>
                <div onclick="scrollToSection('section2')" class="nav-item w-full text-left px-4 py-3 rounded-lg text-sm font-medium text-gray-400">🏆 募资平台匹配</div>
                <div onclick="scrollToSection('section3')" class="nav-item w-full text-left px-4 py-3 rounded-lg text-sm font-medium text-gray-400">💰 财务可行性</div>
                <div onclick="scrollToSection('section4')" class="nav-item w-full text-left px-4 py-3 rounded-lg text-sm font-medium text-gray-400">🔬 证据可信度</div>
                <div onclick="scrollToSection('section5')" class="nav-item w-full text-left px-4 py-3 rounded-lg text-sm font-medium text-gray-400">⚠️ 风险与合规</div>
                <div onclick="scrollToSection('section6')" class="nav-item w-full text-left px-4 py-3 rounded-lg text-sm font-medium text-gray-400">🚀 行动路线图</div>
                <div onclick="scrollToSection('section7')" class="nav-item w-full text-left px-4 py-3 rounded-lg text-sm font-medium text-gray-400">📊 评分详情</div>
            </div>
        </nav>
        
        <div class="p-4 border-t border-white/5">
            <p class="text-xs text-gray-500 text-center">
                生成时间：{datetime.now().strftime('%Y年%m月%d日')}<br>
                品类：{category}
            </p>
        </div>
    </aside>
    
    <main class="main-content ml-72 min-h-screen p-8">
        <div class="max-w-5xl mx-auto space-y-8">
            
            <!-- 0. 执行摘要 -->
            <div id="section0" class="glass-card p-8 fade-in">
                <h2 class="section-header text-2xl font-bold text-white mb-6">📋 执行摘要</h2>
                
                <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
                    <div class="glass-card p-4 text-center">
                        <div class="text-3xl font-bold gradient-text">{score}</div>
                        <div class="text-xs text-gray-400 mt-1">综合评分</div>
                    </div>
                    <div class="glass-card p-4 text-center">
                        <div class="text-xl font-bold text-white">¥100亿+</div>
                        <div class="text-xs text-gray-400 mt-1">TAM市场规模</div>
                    </div>
                    <div class="glass-card p-4 text-center col-span-2 md:col-span-1">
                        <div class="text-xl font-bold text-white">12-18月</div>
                        <div class="text-xs text-gray-400 mt-1">预计回收期</div>
                    </div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <h3 class="text-lg font-semibold text-gray-200 mb-3">💪 核心优势</h3>
                        <div class="space-y-2">
                            {''.join([f'<div class="flex items-start gap-2"><span class="tag tag-excellent mt-1">优势</span><span class="text-gray-300 text-sm">{s}</span></div>' for s in strengths])}
                        </div>
                    </div>
                    <div>
                        <h3 class="text-lg font-semibold text-gray-200 mb-3">⚠️ 关键短板</h3>
                        <div class="space-y-2">
                            {''.join([f'<div class="flex items-start gap-2"><span class="tag tag-risk mt-1">短板</span><span class="text-gray-300 text-sm">{w}</span></div>' for w in weaknesses])}
                        </div>
                    </div>
                </div>
                
                <div class="quote-box mt-6">
                    💡 建议：{scoring.get('recommendation', '待评估')}
                </div>
            </div>
            
            <!-- 1. 产品与市场匹配 -->
            <div id="section1" class="glass-card p-8 fade-in">
                <div class="collapsible flex items-center justify-between" onclick="toggleSection(this)">
                    <h2 class="section-header text-2xl font-bold text-white mb-0">🎯 维度一：产品与市场匹配</h2>
                    <svg class="chevron w-5 h-5 text-gray-400 rotated" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                </div>
                
                <div class="collapsible-content open mt-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                        <div>
                            <h3 class="text-lg font-semibold text-gray-200 mb-3">产品画像</h3>
                            <div class="space-y-3">
                                <div class="dimension-card">
                                    <div class="flex justify-between text-sm mb-2">
                                        <span class="text-gray-300">产品名称</span>
                                        <span class="text-white font-medium">{name}</span>
                                    </div>
                                </div>
                                <div class="dimension-card">
                                    <div class="flex justify-between text-sm mb-2">
                                        <span class="text-gray-300">识别品类</span>
                                        <span class="text-white font-medium">{category}</span>
                                    </div>
                                </div>
                                <div class="dimension-card">
                                    <div class="text-sm text-gray-300 mb-2">核心价值</div>
                                    <div class="text-sm text-white">{product.get('value_proposition', '待补充')}</div>
                                </div>
                            </div>
                        </div>
                        
                        <div>
                            <h3 class="text-lg font-semibold text-gray-200 mb-3">评分雷达图</h3>
                            <div class="relative" style="height: 250px;">
                                <canvas id="radarChart"></canvas>
                            </div>
                        </div>
                    </div>
                    
                    <h3 class="text-lg font-semibold text-gray-200 mb-4">SWOT分析</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="glass-card p-4 border-l-4 border-green-500">
                            <h4 class="font-semibold text-green-400 mb-2">优势 Strengths</h4>
                            <ul class="text-sm text-gray-300 space-y-1">
                                {''.join([f'<li>• {s}</li>' for s in strengths])}
                            </ul>
                        </div>
                        <div class="glass-card p-4 border-l-4 border-red-500">
                            <h4 class="font-semibold text-red-400 mb-2">劣势 Weaknesses</h4>
                            <ul class="text-sm text-gray-300 space-y-1">
                                {''.join([f'<li>• {w}</li>' for w in weaknesses])}
                            </ul>
                        </div>
                        <div class="glass-card p-4 border-l-4 border-blue-500">
                            <h4 class="font-semibold text-blue-400 mb-2">机会 Opportunities</h4>
                            <ul class="text-sm text-gray-300 space-y-1">
                                <li>• AI市场快速增长（年增35%）</li>
                                <li>• 情感科技赛道处于上升期</li>
                                <li>• 募资平台用户对AI品类接受度高</li>
                            </ul>
                        </div>
                        <div class="glass-card p-4 border-l-4 border-yellow-500">
                            <h4 class="font-semibold text-yellow-400 mb-2">威胁 Threats</h4>
                            <ul class="text-sm text-gray-300 space-y-1">
                                <li>• 竞品跟进速度快</li>
                                <li>• 供应链不确定性</li>
                                <li>• 监管政策变化</li>
                            </ul>
                        </div>
                    </div>
                    
                    <h3 class="text-lg font-semibold text-gray-200 mt-6 mb-4">市场规模 (TAM/SAM/SOM)</h3>
                    <div class="grid grid-cols-3 gap-4">
                        <div class="glass-card p-4 text-center">
                            <div class="text-2xl font-bold gradient-text">¥100亿+</div>
                            <div class="text-xs text-gray-400 mt-1">TAM 总可寻址市场</div>
                        </div>
                        <div class="glass-card p-4 text-center">
                            <div class="text-2xl font-bold text-blue-400">¥10亿</div>
                            <div class="text-xs text-gray-400 mt-1">SAM 可服务市场</div>
                        </div>
                        <div class="glass-card p-4 text-center">
                            <div class="text-2xl font-bold text-purple-400">¥1亿</div>
                            <div class="text-xs text-gray-400 mt-1">SOM 可获得市场</div>
                        </div>
                    </div>
                    
                    <h3 class="text-lg font-semibold text-gray-200 mt-8 mb-4">👥 用户洞察分析</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <h4 class="font-medium text-gray-300 mb-3">核心用户画像</h4>
                            <div class="space-y-2">
                                {self._html_user_persona_items(data.get('user_insights', {}).get('personas', []))}
                            </div>
                        </div>
                        <div>
                            <h4 class="font-medium text-gray-300 mb-3">典型使用场景</h4>
                            <div class="space-y-2">
                                {self._html_use_case_items(data.get('user_insights', {}).get('use_cases', []))}
                            </div>
                        </div>
                    </div>
                    
                    <h4 class="font-medium text-gray-300 mt-6 mb-3">用户旅程地图</h4>
                    <div class="overflow-x-auto">
                        <table class="text-sm">
                            <thead>
                                <tr>
                                    <th>阶段</th>
                                    <th>用户行为</th>
                                    <th>关键痛点</th>
                                    <th>机会点</th>
                                </tr>
                            </thead>
                            <tbody>
                                {self._html_user_journey_rows(data.get('user_insights', {}).get('journey', []))}
                            </tbody>
                        </table>
                    </div>
                    
                    <div class="mt-4 glass-card p-4 bg-cyan-500/5 border border-cyan-500/20">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-cyan-400 font-medium">用户洞察成熟度</span>
                            <span class="text-2xl font-bold gradient-text">{data.get('user_insights', {}).get('score', '待评')}/10</span>
                        </div>
                        <div class="text-sm text-gray-400">
                            {self._html_user_insight_summary(data.get('user_insights', {}))}
                        </div>
                    </div>
                    
                    <h3 class="text-lg font-semibold text-gray-200 mt-8 mb-4">📦 产品定义与MVP</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <h4 class="font-medium text-gray-300 mb-3">功能优先级（MoSCoW）</h4>
                            <div class="space-y-2">
                                {self._html_moscow_items(data.get('product_definition', {}).get('moscow_features', []))}
                            </div>
                        </div>
                        <div>
                            <h4 class="font-medium text-gray-300 mb-3">MVP范围</h4>
                            <div class="space-y-3">
                                {self._html_mvp_scope_items(data.get('product_definition', {}).get('mvp_scope', {}))}
                            </div>
                        </div>
                    </div>
                    
                    <h4 class="font-medium text-gray-300 mt-6 mb-3">产品路线图</h4>
                    <div class="overflow-x-auto">
                        <table class="text-sm">
                            <thead>
                                <tr>
                                    <th>阶段</th>
                                    <th>时间</th>
                                    <th>核心目标</th>
                                    <th>关键功能</th>
                                </tr>
                            </thead>
                            <tbody>
                                {self._html_product_roadmap_rows(data.get('product_definition', {}).get('roadmap', []))}
                            </tbody>
                        </table>
                    </div>
                    
                    <div class="mt-4 glass-card p-4 bg-emerald-500/5 border border-emerald-500/20">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-emerald-400 font-medium">产品定义清晰度</span>
                            <span class="text-2xl font-bold gradient-text">{data.get('product_definition', {}).get('score', '待评')}/10</span>
                        </div>
                        <div class="text-sm text-gray-400">
                            {self._html_product_definition_summary(data.get('product_definition', {}))}
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 2. 募资平台匹配 -->
            <div id="section2" class="glass-card p-8 fade-in">
                <div class="collapsible flex items-center justify-between" onclick="toggleSection(this)">
                    <h2 class="section-header text-2xl font-bold text-white mb-0">🏆 维度二：募资平台匹配</h2>
                    <svg class="chevron w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                </div>
                
                <div class="collapsible-content mt-6">
                    <h3 class="text-lg font-semibold text-gray-200 mb-4">竞品对比分析</h3>
                    <div class="overflow-x-auto">
                        <table>
                            <thead>
                                <tr>
                                    <th>项目名称</th>
                                    <th>平台</th>
                                    <th>募集金额</th>
                                    <th>支持者</th>
                                    <th>达成率</th>
                                </tr>
                            </thead>
                            <tbody>
                                {self._html_competitor_rows(data.get('competitor_analysis', {}).get('real_cases', []))}
                            </tbody>
                        </table>
                    </div>
                    
                    <h3 class="text-lg font-semibold text-gray-200 mt-6 mb-4">成功因素 vs 失败预警</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="glass-card p-4">
                            <h4 class="font-semibold text-green-400 mb-3">✅ 成功因素</h4>
                            <ul class="text-sm text-gray-300 space-y-2">
                                <li>• 刚需痛点明确，用户愿意付费</li>
                                <li>• 视觉冲击力强，有传播记忆点</li>
                                <li>• 价格带处于平台甜蜜区间</li>
                                <li>• 团队可信度高，履约风险低</li>
                                <li>• 预热充分，有种子用户基础</li>
                            </ul>
                        </div>
                        <div class="glass-card p-4">
                            <h4 class="font-semibold text-red-400 mb-3">❌ 失败模式</h4>
                            <ul class="text-sm text-gray-300 space-y-2">
                                <li>• 痛点模糊，为了AI而AI</li>
                                <li>• 定价偏离平台用户习惯</li>
                                <li>• 团队缺乏经验，履约不可控</li>
                                <li>• 产品过于复杂，MVP不清</li>
                                <li>• 缺乏传播点，纯靠自然流量</li>
                            </ul>
                        </div>
                    </div>
                    
                    <h3 class="text-lg font-semibold text-gray-200 mt-6 mb-4">📊 成功因子模式分析</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {self._html_success_patterns(data.get('competitor_analysis', {}).get('success_patterns', {}))}
                    </div>
                    
                    <h3 class="text-lg font-semibold text-gray-200 mt-8 mb-4">🎬 产品演示力评估</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <h4 class="font-medium text-gray-300 mb-3">演示力评估矩阵</h4>
                            <div class="overflow-x-auto">
                                <table class="text-sm">
                                    <thead>
                                        <tr>
                                            <th>评估维度</th>
                                            <th>评估项</th>
                                            <th>得分</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {self._html_demo_eval_rows(data.get('demo_evaluation', {}).get('dimensions', []))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div>
                            <h4 class="font-medium text-gray-300 mb-3">演示素材清单</h4>
                            <div class="space-y-2">
                                {self._html_demo_asset_items(data.get('demo_evaluation', {}).get('assets', []))}
                            </div>
                        </div>
                    </div>
                    <div class="mt-4 glass-card p-4 bg-blue-500/5 border border-blue-500/20">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-blue-400 font-medium">综合演示力评分</span>
                            <span class="text-2xl font-bold gradient-text">{data.get('demo_evaluation', {}).get('score', '待评')}/10</span>
                        </div>
                        <div class="text-sm text-gray-400">
                            {self._html_demo_summary(data.get('demo_evaluation', {}))}
                        </div>
                    </div>
                    
                    <h3 class="text-lg font-semibold text-gray-200 mt-8 mb-4">🚀 众筹策略专项</h3>
                    <div class="space-y-6">
                        <div>
                            <h4 class="font-medium text-gray-300 mb-3">档位设计建议</h4>
                            <div class="overflow-x-auto">
                                <table class="text-sm">
                                    <thead>
                                        <tr>
                                            <th>档位类型</th>
                                            <th>价格区间</th>
                                            <th>核心权益</th>
                                            <th>限量策略</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {self._html_tier_rows(data.get('crowdfunding_strategy', {}).get('tiers', []))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div>
                            <h4 class="font-medium text-gray-300 mb-3">预热节奏规划</h4>
                            <div class="overflow-x-auto">
                                <table class="text-sm">
                                    <thead>
                                        <tr>
                                            <th>阶段</th>
                                            <th>时间</th>
                                            <th>核心动作</th>
                                            <th>目标</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {self._html_preheat_rows(data.get('crowdfunding_strategy', {}).get('preheat_timeline', []))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <h4 class="font-medium text-gray-300 mb-3">推广渠道策略</h4>
                                <div class="overflow-x-auto">
                                    <table class="text-sm">
                                        <thead>
                                            <tr>
                                                <th>渠道类型</th>
                                                <th>预算占比</th>
                                                <th>预期效果</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {self._html_channel_rows(data.get('crowdfunding_strategy', {}).get('channels', []))}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            <div>
                                <h4 class="font-medium text-gray-300 mb-3">KOL/媒体合作</h4>
                                <div class="space-y-2">
                                    {self._html_kol_items(data.get('crowdfunding_strategy', {}).get('kol_partners', []))}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="mt-4 glass-card p-4 bg-purple-500/5 border border-purple-500/20">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-purple-400 font-medium">众筹策略成熟度</span>
                            <span class="text-2xl font-bold gradient-text">{data.get('crowdfunding_strategy', {}).get('score', '待评')}/10</span>
                        </div>
                        <div class="text-sm text-gray-400">
                            {self._html_crowdfunding_summary(data.get('crowdfunding_strategy', {}))}
                        </div>
                    </div>
                    
                    <h3 class="text-lg font-semibold text-gray-200 mt-6 mb-4">平台匹配度评估</h3>
                    <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
                        <div class="glass-card p-3 text-center">
                            <div class="text-lg font-bold text-blue-400">7/10</div>
                            <div class="text-xs text-gray-400 mt-1">品类匹配</div>
                        </div>
                        <div class="glass-card p-3 text-center">
                            <div class="text-lg font-bold text-yellow-400">6/10</div>
                            <div class="text-xs text-gray-400 mt-1">价格匹配</div>
                        </div>
                        <div class="glass-card p-3 text-center">
                            <div class="text-lg font-bold text-purple-400">待评</div>
                            <div class="text-xs text-gray-400 mt-1">传播性</div>
                        </div>
                        <div class="glass-card p-3 text-center">
                            <div class="text-lg font-bold text-green-400">待评</div>
                            <div class="text-xs text-gray-400 mt-1">故事性</div>
                        </div>
                        <div class="glass-card p-3 text-center">
                            <div class="text-lg font-bold gradient-text">6.5</div>
                            <div class="text-xs text-gray-400 mt-1">综合匹配</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 3. 财务可行性 -->
            <div id="section3" class="glass-card p-8 fade-in">
                <div class="collapsible flex items-center justify-between" onclick="toggleSection(this)">
                    <h2 class="section-header text-2xl font-bold text-white mb-0">💰 维度三：财务可行性</h2>
                    <svg class="chevron w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                </div>
                
                <div class="collapsible-content mt-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <h3 class="text-lg font-semibold text-gray-200 mb-4">募资目标 & 收入</h3>
                            <div class="space-y-3">
                                <div class="dimension-card">
                                    <div class="flex justify-between items-center">
                                        <span class="text-gray-300">目标募资金额</span>
                                        <span class="text-xl font-bold text-white">¥{product.get('target_amount', '50万')}</span>
                                    </div>
                                </div>
                                <div class="dimension-card">
                                    <div class="flex justify-between items-center">
                                        <span class="text-gray-300">平台费用（约11%）</span>
                                        <span class="text-yellow-400">约¥{int(float(str(product.get('target_amount', '500000')).replace(',','')) * 0.11)}</span>
                                    </div>
                                </div>
                                <div class="dimension-card">
                                    <div class="flex justify-between items-center">
                                        <span class="text-gray-300">预计实际到手</span>
                                        <span class="text-green-400 font-semibold">¥{int(float(str(product.get('target_amount', '500000')).replace(',','')) * 0.89)}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div>
                            <h3 class="text-lg font-semibold text-gray-200 mb-4">成本结构</h3>
                            <div class="relative" style="height: 220px;">
                                <canvas id="costChart"></canvas>
                            </div>
                        </div>
                    </div>
                    
                    <h3 class="text-lg font-semibold text-gray-200 mt-6 mb-4">盈利分析</h3>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div class="glass-card p-4 text-center">
                            <div class="text-2xl font-bold text-green-400">50%</div>
                            <div class="text-xs text-gray-400 mt-1">毛利率</div>
                        </div>
                        <div class="glass-card p-4 text-center">
                            <div class="text-2xl font-bold text-blue-400">~700</div>
                            <div class="text-xs text-gray-400 mt-1">盈亏平衡(台)</div>
                        </div>
                        <div class="glass-card p-4 text-center">
                            <div class="text-2xl font-bold text-purple-400">12-18月</div>
                            <div class="text-xs text-gray-400 mt-1">投资回收期</div>
                        </div>
                        <div class="glass-card p-4 text-center">
                            <div class="text-2xl font-bold text-yellow-400">6.5/10</div>
                            <div class="text-xs text-gray-400 mt-1">财务健康度</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 4. 证据可信度 -->
            <div id="section4" class="glass-card p-8 fade-in">
                <div class="collapsible flex items-center justify-between" onclick="toggleSection(this)">
                    <h2 class="section-header text-2xl font-bold text-white mb-0">🔬 维度四：证据可信度</h2>
                    <svg class="chevron w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                </div>
                
                <div class="collapsible-content mt-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <h3 class="text-lg font-semibold text-gray-200 mb-4">技术架构评估</h3>
                            <div class="space-y-3">
                                <div class="dimension-card">
                                    <div class="flex justify-between text-sm mb-2">
                                        <span class="text-gray-300">技术栈成熟度</span>
                                        <span class="tag tag-normal">待评估</span>
                                    </div>
                                </div>
                                <div class="dimension-card">
                                    <div class="flex justify-between text-sm mb-2">
                                        <span class="text-gray-300">供应链可靠性</span>
                                        <span class="tag tag-normal">待评估</span>
                                    </div>
                                </div>
                                <div class="dimension-card">
                                    <div class="flex justify-between text-sm mb-2">
                                        <span class="text-gray-300">安全合规性</span>
                                        <span class="tag tag-normal">待评估</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div>
                            <h3 class="text-lg font-semibold text-gray-200 mb-4">证据完整度</h3>
                            <div class="space-y-2">
                                <div class="flex items-center justify-between text-sm">
                                    <span class="text-gray-400">用户访谈</span>
                                    <span class="tag tag-poor">待补充</span>
                                </div>
                                <div class="flex items-center justify-between text-sm">
                                    <span class="text-gray-400">产品原型/Demo</span>
                                    <span class="tag tag-poor">待补充</span>
                                </div>
                                <div class="flex items-center justify-between text-sm">
                                    <span class="text-gray-400">团队背景</span>
                                    <span class="tag tag-poor">待补充</span>
                                </div>
                                <div class="flex items-center justify-between text-sm">
                                    <span class="text-gray-400">供应链意向</span>
                                    <span class="tag tag-poor">待补充</span>
                                </div>
                                <div class="flex items-center justify-between text-sm">
                                    <span class="text-gray-400">预注册用户</span>
                                    <span class="tag tag-poor">待补充</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 5. 风险与合规 -->
            <div id="section5" class="glass-card p-8 fade-in">
                <div class="collapsible flex items-center justify-between" onclick="toggleSection(this)">
                    <h2 class="section-header text-2xl font-bold text-white mb-0">⚠️ 维度五：风险与合规</h2>
                    <svg class="chevron w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                </div>
                
                <div class="collapsible-content mt-6">
                    <h3 class="text-lg font-semibold text-gray-200 mb-4">风险矩阵（概率 × 影响）</h3>
                    <div class="grid grid-cols-4 gap-0 mb-6">
                        <div></div>
                        <div class="risk-matrix-cell text-gray-400">低影响</div>
                        <div class="risk-matrix-cell text-gray-400">中影响</div>
                        <div class="risk-matrix-cell text-gray-400">高影响</div>
                        
                        <div class="risk-matrix-cell text-gray-400">高概率</div>
                        <div class="risk-matrix-cell risk-medium">市场竞争</div>
                        <div class="risk-matrix-cell risk-medium">供应链波动</div>
                        <div class="risk-matrix-cell risk-high">技术不达预期</div>
                        
                        <div class="risk-matrix-cell text-gray-400">中概率</div>
                        <div class="risk-matrix-cell risk-low">人才招聘</div>
                        <div class="risk-matrix-cell risk-medium">交付延期</div>
                        <div class="risk-matrix-cell risk-high">资金链断裂</div>
                        
                        <div class="risk-matrix-cell text-gray-400">低概率</div>
                        <div class="risk-matrix-cell risk-low">政策变动</div>
                        <div class="risk-matrix-cell risk-low">核心人员流失</div>
                        <div class="risk-matrix-cell risk-medium">合规风险</div>
                    </div>
                    
                    <h3 class="text-lg font-semibold text-gray-200 mb-4">风险应对策略</h3>
                    <div class="space-y-3">
                        <div class="dimension-card">
                            <div class="flex items-start gap-3">
                                <span class="tag tag-risk">高风险</span>
                                <div>
                                    <div class="text-white font-medium text-sm">技术/供应链/资金风险</div>
                                    <div class="text-gray-400 text-xs mt-1">应对：MVP验证、多供应商备选、分阶段投入</div>
                                </div>
                            </div>
                        </div>
                        <div class="dimension-card">
                            <div class="flex items-start gap-3">
                                <span class="tag tag-normal">中风险</span>
                                <div>
                                    <div class="text-white font-medium text-sm">市场竞争/交付延期/合规</div>
                                    <div class="text-gray-400 text-xs mt-1">应对：快速迭代差异化、充足缓冲期、合规前置设计</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 6. 行动路线图 -->
            <div id="section6" class="glass-card p-8 fade-in">
                <div class="collapsible flex items-center justify-between" onclick="toggleSection(this)">
                    <h2 class="section-header text-2xl font-bold text-white mb-0">🚀 维度六：行动路线图</h2>
                    <svg class="chevron w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                </div>
                
                <div class="collapsible-content mt-6">
                    <h3 class="text-lg font-semibold text-gray-200 mb-4">7天验证任务</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 mb-6">
                        <div class="glass-card p-4">
                            <div class="text-sm font-semibold text-white mb-2">👥 用户访谈</div>
                            <div class="text-xs text-gray-400">5-10位目标用户深度访谈，验证痛点</div>
                        </div>
                        <div class="glass-card p-4">
                            <div class="text-sm font-semibold text-white mb-2">🔍 竞品分析</div>
                            <div class="text-xs text-gray-400">3-5个直接竞品深度对标分析</div>
                        </div>
                        <div class="glass-card p-4">
                            <div class="text-sm font-semibold text-white mb-2">🎬 原型演示</div>
                            <div class="text-xs text-gray-400">制作MVP原型或演示视频</div>
                        </div>
                        <div class="glass-card p-4">
                            <div class="text-sm font-semibold text-white mb-2">💰 成本核算</div>
                            <div class="text-xs text-gray-400">详细BOM成本和毛利测算</div>
                        </div>
                        <div class="glass-card p-4">
                            <div class="text-sm font-semibold text-white mb-2">👤 用户画像</div>
                            <div class="text-xs text-gray-400">明确第一批用户和获客渠道</div>
                        </div>
                    </div>
                    
                    <h3 class="text-lg font-semibold text-gray-200 mb-4">30天推进计划</h3>
                    <div class="space-y-3">
                        <div class="flex gap-4">
                            <div class="w-16 text-right">
                                <span class="tag tag-good">第1周</span>
                            </div>
                            <div class="flex-1 glass-card p-3">
                                <div class="text-sm text-white font-medium">产品定义与原型</div>
                                <div class="text-xs text-gray-400 mt-1">MVP功能清单、产品原型、用户故事</div>
                            </div>
                        </div>
                        <div class="flex gap-4">
                            <div class="w-16 text-right">
                                <span class="tag tag-good">第2周</span>
                            </div>
                            <div class="flex-1 glass-card p-3">
                                <div class="text-sm text-white font-medium">市场验证与用户</div>
                                <div class="text-xs text-gray-400 mt-1">用户访谈报告、种子用户群、竞品分析</div>
                            </div>
                        </div>
                        <div class="flex gap-4">
                            <div class="w-16 text-right">
                                <span class="tag tag-normal">第3周</span>
                            </div>
                            <div class="flex-1 glass-card p-3">
                                <div class="text-sm text-white font-medium">财务与供应链</div>
                                <div class="text-xs text-gray-400 mt-1">财务模型、定价方案、供应商接触</div>
                            </div>
                        </div>
                        <div class="flex gap-4">
                            <div class="w-16 text-right">
                                <span class="tag tag-poor">第4周</span>
                            </div>
                            <div class="flex-1 glass-card p-3">
                                <div class="text-sm text-white font-medium">推广准备</div>
                                <div class="text-xs text-gray-400 mt-1">预热计划、募资文案、素材准备</div>
                            </div>
                        </div>
                    </div>
                    
                    <h3 class="text-lg font-semibold text-gray-200 mt-6 mb-4">增长飞轮</h3>
                    <div class="glass-card p-6 text-center" style="background: linear-gradient(135deg, rgba(96, 165, 250, 0.1), rgba(167, 139, 250, 0.1));">
                        <div class="text-white font-medium mb-3">硬件增长飞轮</div>
                        <div class="flex flex-wrap justify-center gap-2">
                            <span class="tag tag-good">产品销售</span>
                            <span class="text-gray-400">→</span>
                            <span class="tag tag-good">口碑传播</span>
                            <span class="text-gray-400">→</span>
                            <span class="tag tag-good">用户增长</span>
                            <span class="text-gray-400">→</span>
                            <span class="tag tag-good">规模效应</span>
                            <span class="text-gray-400">→</span>
                            <span class="tag tag-good">成本降低</span>
                            <span class="text-gray-400">→</span>
                            <span class="tag tag-good">价格优势</span>
                            <span class="text-gray-400">→</span>
                            <span class="tag tag-good">更多销售</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 7. 评分详情 -->
            <div id="section7" class="glass-card p-8 fade-in">
                <div class="collapsible flex items-center justify-between" onclick="toggleSection(this)">
                    <h2 class="section-header text-2xl font-bold text-white mb-0">📊 评分详情</h2>
                    <svg class="chevron w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                </div>
                
                <div class="collapsible-content mt-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <h3 class="text-lg font-semibold text-gray-200 mb-4">各维度得分</h3>
                            <div class="space-y-3">
                                {self._html_score_bars(dims)}
                            </div>
                        </div>
                        <div>
                            <h3 class="text-lg font-semibold text-gray-200 mb-4">得分分布</h3>
                            <div class="relative" style="height: 280px;">
                                <canvas id="barChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 页脚 -->
            <div class="text-center py-8 text-gray-500 text-sm">
                <p>本报告由产品可行性分析智能体 v5.0 自动生成</p>
                <p class="mt-1">生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M')}</p>
            </div>
        </div>
    </main>
    
    <script>
        // 加载动画
        window.addEventListener('load', function() {{
            setTimeout(function() {{
                document.getElementById('loadingOverlay').classList.add('hidden');
            }}, 800);
            
            // 分数动画
            animateScore({score});
            initCharts();
        }});
        
        function animateScore(targetScore) {{
            const circle = document.getElementById('scoreCircle');
            const num = document.getElementById('scoreNum');
            const circumference = 264;
            const offset = circumference - (targetScore / 100) * circumference;
            
            let current = 0;
            const step = targetScore / 50;
            const timer = setInterval(() => {{
                current += step;
                if (current >= targetScore) {{
                    current = targetScore;
                    clearInterval(timer);
                }}
                num.textContent = Math.round(current);
                const curOffset = circumference - (current / 100) * circumference;
                circle.style.strokeDashoffset = curOffset;
            }}, 20);
        }}
        
        function initCharts() {{
            const labels = {json.dumps(score_labels)};
            const values = {json.dumps(score_values)};
            
            // 雷达图
            const radarCtx = document.getElementById('radarChart').getContext('2d');
            new Chart(radarCtx, {{
                type: 'radar',
                data: {{
                    labels: labels,
                    datasets: [{{
                        label: '得分',
                        data: values,
                        backgroundColor: 'rgba(96, 165, 250, 0.2)',
                        borderColor: 'rgba(96, 165, 250, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: '#a78bfa',
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        r: {{
                            beginAtZero: true,
                            max: 100,
                            ticks: {{ color: 'rgba(255,255,255,0.3)', backdropColor: 'transparent', stepSize: 20 }},
                            grid: {{ color: 'rgba(255,255,255,0.1)' }},
                            angleLines: {{ color: 'rgba(255,255,255,0.1)' }},
                            pointLabels: {{ color: '#a1a1aa', font: {{ size: 11 }} }}
                        }}
                    }},
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});
            
            // 柱状图
            const barCtx = document.getElementById('barChart').getContext('2d');
            new Chart(barCtx, {{
                type: 'bar',
                data: {{
                    labels: labels,
                    datasets: [{{
                        label: '得分',
                        data: values,
                        backgroundColor: 'rgba(96, 165, 250, 0.6)',
                        borderColor: 'rgba(96, 165, 250, 1)',
                        borderWidth: 1,
                        borderRadius: 4,
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    indexAxis: 'y',
                    scales: {{
                        x: {{
                            beginAtZero: true,
                            max: 100,
                            ticks: {{ color: 'rgba(255,255,255,0.3)' }},
                            grid: {{ color: 'rgba(255,255,255,0.05)' }}
                        }},
                        y: {{
                            ticks: {{ color: '#a1a1aa', font: {{ size: 11 }} }},
                            grid: {{ display: false }}
                        }}
                    }},
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});
            
            // 成本饼图
            const costCtx = document.getElementById('costChart').getContext('2d');
            new Chart(costCtx, {{
                type: 'doughnut',
                data: {{
                    labels: ['硬件BOM', '制造', '物流', '营销', '运营'],
                    datasets: [{{
                        data: [50, 8, 5, 17, 20],
                        backgroundColor: [
                            'rgba(96, 165, 250, 0.8)',
                            'rgba(167, 139, 250, 0.8)',
                            'rgba(34, 197, 94, 0.8)',
                            'rgba(251, 191, 36, 0.8)',
                            'rgba(249, 115, 22, 0.8)',
                        ],
                        borderWidth: 0,
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'right',
                            labels: {{ color: '#a1a1aa', font: {{ size: 11 }}, padding: 12 }}
                        }}
                    }}
                }}
            }});
        }}
        
        function toggleSection(el) {{
            const content = el.nextElementSibling;
            const chevron = el.querySelector('.chevron');
            content.classList.toggle('open');
            chevron.classList.toggle('rotated');
        }}
        
        function scrollToSection(id) {{
            const el = document.getElementById(id);
            if (el) {{
                el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                
                // 更新导航高亮
                document.querySelectorAll('.nav-item').forEach(item => {{
                    item.classList.remove('active');
                    item.classList.add('text-gray-400');
                    item.classList.remove('text-gray-300');
                }});
                event.target.classList.add('active');
                event.target.classList.remove('text-gray-400');
                event.target.classList.add('text-gray-300');
                
                // 移动端关闭侧边栏
                if (window.innerWidth <= 768) {{
                    document.querySelector('.sidebar').classList.remove('open');
                }}
            }}
        }}
        
        // 滚动监听，自动高亮导航
        window.addEventListener('scroll', function() {{
            const sections = ['section0', 'section1', 'section2', 'section3', 'section4', 'section5', 'section6', 'section7'];
            const scrollPos = window.scrollY + 100;
            
            for (let i = sections.length - 1; i >= 0; i--) {{
                const section = document.getElementById(sections[i]);
                if (section && section.offsetTop <= scrollPos) {{
                    document.querySelectorAll('.nav-item').forEach((item, idx) => {{
                        if (idx === i) {{
                            item.classList.add('active');
                            item.classList.remove('text-gray-400');
                            item.classList.add('text-gray-300');
                        }} else {{
                            item.classList.remove('active');
                            item.classList.add('text-gray-400');
                            item.classList.remove('text-gray-300');
                        }}
                    }});
                    break;
                }}
            }}
        }});
    </script>
</body>
</html>"""
        return html
    
    def _score_tag_class(self, score: float) -> str:
        if score >= 80: return 'tag-excellent'
        if score >= 65: return 'tag-good'
        if score >= 50: return 'tag-normal'
        return 'tag-poor'
    
    def _grade_action(self, grade: str) -> str:
        actions = {
            'A': '可进入正式开发/募资阶段',
            'B': '建议补强后继续推进',
            'C': '需要重新定位用户/场景',
            'D': '暂不建议大量投入'
        }
        return actions.get(grade, '待评估')
    
    def _html_competitor_rows(self, cases: List) -> str:
        if not cases:
            return '<tr><td colspan="5" class="text-center text-gray-500">暂无数据</td></tr>'
        rows = []
        for c in cases[:5]:
            link = c.get('link', '')
            name = c.get('name', '-')
            if link:
                name = f'<a href="{link}" target="_blank" class="text-blue-400 hover:text-blue-300 underline">{name}</a>'
            rows.append(f"""<tr>
                <td class="text-white">{name}</td>
                <td>{c.get('platform', '-')}</td>
                <td class="text-green-400">{c.get('amount_raised', '-')}</td>
                <td>{c.get('backers', '-')}</td>
                <td><span class="tag tag-good">{c.get('success_rate', '-')}</span></td>
            </tr>""")
        return '\n'.join(rows)
    
    def _html_demo_eval_rows(self, dimensions: List) -> str:
        if not dimensions:
            return '<tr><td colspan="3" class="text-center text-gray-500">待评估</td></tr>'
        rows = []
        for d in dimensions[:8]:
            score = d.get('score', 0)
            score_color = 'text-green-400' if score >= 7 else 'text-yellow-400' if score >= 5 else 'text-red-400'
            rows.append(f"""<tr>
                <td class="text-gray-300">{d.get('dimension', '')}</td>
                <td class="text-white">{d.get('item', '')}</td>
                <td class="{score_color} font-medium">{score}</td>
            </tr>""")
        return '\n'.join(rows)
    
    def _html_demo_asset_items(self, assets: List) -> str:
        if not assets:
            return '<div class="text-gray-500 text-sm">待补充素材清单</div>'
        items = []
        for a in assets[:8]:
            priority = a.get('priority', '中')
            tag_class = 'tag-risk' if priority == '高' else 'tag-normal' if priority == '中' else 'tag-good'
            status = a.get('status', '待补充')
            status_color = 'text-red-400' if '待' in status else 'text-green-400'
            items.append(f"""
            <div class="glass-card p-3 flex items-center justify-between">
                <div>
                    <div class="text-sm text-white">{a.get('type', '')}</div>
                    <div class="text-xs text-gray-500 mt-1">{a.get('suggestion', '')}</div>
                </div>
                <div class="flex items-center gap-2">
                    <span class="text-xs {status_color}">{status}</span>
                    <span class="tag {tag_class}">{priority}</span>
                </div>
            </div>""")
        return '\n'.join(items)
    
    def _html_demo_summary(self, demo: Dict) -> str:
        if not demo:
            return '待评估 - 需要补充产品演示素材和评估'
        summary = demo.get('summary', [])
        if not summary:
            return '待评估'
        return '<ul class="list-disc list-inside space-y-1">' + ''.join([f'<li>{s}</li>' for s in summary]) + '</ul>'
    
    def _html_tier_rows(self, tiers: List) -> str:
        if not tiers:
            return '<tr><td colspan="4" class="text-center text-gray-500">待补充档位设计</td></tr>'
        rows = []
        for t in tiers[:6]:
            name = t.get('name', '')
            price = t.get('price', '')
            benefits = t.get('benefits', '')
            limit = t.get('limit', '')
            rows.append(f"""<tr>
                <td class="text-white font-medium">{name}</td>
                <td class="text-green-400">{price}</td>
                <td class="text-gray-300 text-sm">{benefits}</td>
                <td><span class="tag tag-normal">{limit}</span></td>
            </tr>""")
        return '\n'.join(rows)
    
    def _html_preheat_rows(self, timeline: List) -> str:
        if not timeline:
            return '<tr><td colspan="4" class="text-center text-gray-500">待补充预热规划</td></tr>'
        rows = []
        for t in timeline[:5]:
            rows.append(f"""<tr>
                <td class="text-white font-medium">{t.get('stage', '')}</td>
                <td class="text-blue-400">{t.get('time', '')}</td>
                <td class="text-gray-300 text-sm">{t.get('actions', '')}</td>
                <td class="text-green-400 text-sm">{t.get('goal', '')}</td>
            </tr>""")
        return '\n'.join(rows)
    
    def _html_channel_rows(self, channels: List) -> str:
        if not channels:
            return '<tr><td colspan="3" class="text-center text-gray-500">待补充渠道策略</td></tr>'
        rows = []
        for c in channels[:6]:
            rows.append(f"""<tr>
                <td class="text-white">{c.get('type', '')}</td>
                <td class="text-yellow-400">{c.get('budget', '')}</td>
                <td class="text-gray-300 text-sm">{c.get('expected_effect', '')}</td>
            </tr>""")
        return '\n'.join(rows)
    
    def _html_kol_items(self, partners: List) -> str:
        if not partners:
            return '<div class="text-gray-500 text-sm">待补充KOL合作清单</div>'
        items = []
        for p in partners[:6]:
            priority = p.get('priority', '中')
            tag_class = 'tag-risk' if priority == '高' else 'tag-normal' if priority == '中' else 'tag-good'
            items.append(f"""
            <div class="glass-card p-3">
                <div class="flex items-center justify-between mb-1">
                    <span class="text-sm text-white">{p.get('type', '')}</span>
                    <span class="tag {tag_class}">{priority}</span>
                </div>
                <div class="text-xs text-gray-400">{p.get('target', '')}</div>
                <div class="text-xs text-gray-500 mt-1">{p.get('cooperation', '')}</div>
            </div>""")
        return '\n'.join(items)
    
    def _html_crowdfunding_summary(self, strategy: Dict) -> str:
        if not strategy:
            return '待评估 - 需要补充众筹策略规划'
        summary = strategy.get('summary', [])
        if not summary:
            return '待评估'
        return '<ul class="list-disc list-inside space-y-1">' + ''.join([f'<li>{s}</li>' for s in summary]) + '</ul>'
    
    def _html_user_persona_items(self, personas: List) -> str:
        if not personas:
            return '<div class="text-gray-500 text-sm">待补充用户画像</div>'
        items = []
        for p in personas[:4]:
            willingness = p.get('willingness', '')
            tag_class = 'tag-excellent' if '高' in willingness else 'tag-good' if '中' in willingness else 'tag-normal'
            items.append(f"""
            <div class="glass-card p-3">
                <div class="flex items-center justify-between mb-1">
                    <span class="text-sm font-medium text-white">{p.get('type', '')}</span>
                    <span class="tag {tag_class}">{willingness}</span>
                </div>
                <div class="text-xs text-gray-400">{p.get('characteristics', '')}</div>
                <div class="text-xs text-gray-500 mt-1">诉求：{p.get('needs', '')}</div>
            </div>""")
        return '\n'.join(items)
    
    def _html_use_case_items(self, cases: List) -> str:
        if not cases:
            return '<div class="text-gray-500 text-sm">待补充使用场景</div>'
        items = []
        for i, c in enumerate(cases[:5], 1):
            items.append(f"""
            <div class="glass-card p-3">
                <div class="flex items-start gap-2">
                    <span class="text-cyan-400 font-bold text-sm">{i}.</span>
                    <div>
                        <div class="text-sm text-white">{c.get('title', '')}</div>
                        <div class="text-xs text-gray-400 mt-1">{c.get('description', '')}</div>
                    </div>
                </div>
            </div>""")
        return '\n'.join(items)
    
    def _html_user_journey_rows(self, journey: List) -> str:
        if not journey:
            return '<tr><td colspan="4" class="text-center text-gray-500">待补充用户旅程</td></tr>'
        rows = []
        for j in journey[:6]:
            rows.append(f"""<tr>
                <td class="text-white font-medium">{j.get('stage', '')}</td>
                <td class="text-gray-300 text-sm">{j.get('behavior', '')}</td>
                <td class="text-red-400 text-sm">{j.get('pain_points', '')}</td>
                <td class="text-green-400 text-sm">{j.get('opportunities', '')}</td>
            </tr>""")
        return '\n'.join(rows)
    
    def _html_user_insight_summary(self, insights: Dict) -> str:
        if not insights:
            return '待评估 - 需要补充用户调研数据'
        summary = insights.get('summary', [])
        if not summary:
            return '待评估'
        return '<ul class="list-disc list-inside space-y-1">' + ''.join([f'<li>{s}</li>' for s in summary]) + '</ul>'
    
    def _html_moscow_items(self, features: List) -> str:
        if not features:
            return '<div class="text-gray-500 text-sm">待补充功能优先级</div>'
        items = []
        priority_colors = {
            'must': 'border-red-500 bg-red-500/5',
            'should': 'border-yellow-500 bg-yellow-500/5',
            'could': 'border-blue-500 bg-blue-500/5',
            'wont': 'border-gray-500 bg-gray-500/5',
        }
        priority_labels = {
            'must': 'Must',
            'should': 'Should',
            'could': 'Could',
            'wont': "Won't",
        }
        for f in features[:8]:
            priority = f.get('priority', '')
            color_class = priority_colors.get(priority, 'border-gray-500')
            label = priority_labels.get(priority, priority)
            items.append(f"""
            <div class="glass-card p-2 border-l-4 {color_class}">
                <div class="flex items-center justify-between">
                    <span class="text-xs text-white">{f.get('feature', '')}</span>
                    <span class="text-xs text-gray-500">{f.get('module', '')}</span>
                </div>
            </div>""")
        return '\n'.join(items)
    
    def _html_mvp_scope_items(self, scope: Dict) -> str:
        if not scope:
            return '<div class="text-gray-500 text-sm">待补充MVP范围</div>'
        items = []
        core = scope.get('core_features', [])
        enhanced = scope.get('enhanced_features', [])
        cut = scope.get('cut_features', [])
        timeline = scope.get('timeline', '')
        
        if core:
            items.append(f"""
            <div class="glass-card p-3 border-l-4 border-green-500 bg-green-500/5">
                <div class="text-xs text-green-400 mb-1">核心功能 ({len(core)}个)</div>
                <div class="text-sm text-white">{', '.join(core)}</div>
            </div>""")
        if enhanced:
            items.append(f"""
            <div class="glass-card p-3 border-l-4 border-blue-500 bg-blue-500/5">
                <div class="text-xs text-blue-400 mb-1">增强功能 ({len(enhanced)}个)</div>
                <div class="text-sm text-white">{', '.join(enhanced)}</div>
            </div>""")
        if cut:
            items.append(f"""
            <div class="glass-card p-3 border-l-4 border-gray-500 bg-gray-500/5">
                <div class="text-xs text-gray-400 mb-1">砍掉功能 ({len(cut)}个)</div>
                <div class="text-sm text-gray-400">{', '.join(cut)}</div>
            </div>""")
        if timeline:
            items.append(f"""
            <div class="text-center text-sm text-gray-400 mt-2">
                MVP开发周期：<span class="text-white font-medium">{timeline}</span>
            </div>""")
        return '\n'.join(items)
    
    def _html_product_roadmap_rows(self, roadmap: List) -> str:
        if not roadmap:
            return '<tr><td colspan="4" class="text-center text-gray-500">待补充产品路线图</td></tr>'
        rows = []
        for r in roadmap[:4]:
            rows.append(f"""<tr>
                <td class="text-white font-medium">{r.get('stage', '')}</td>
                <td class="text-blue-400">{r.get('time', '')}</td>
                <td class="text-gray-300 text-sm">{r.get('goal', '')}</td>
                <td class="text-gray-400 text-sm">{r.get('features', '')}</td>
            </tr>""")
        return '\n'.join(rows)
    
    def _html_product_definition_summary(self, definition: Dict) -> str:
        if not definition:
            return '待评估 - 需要补充产品定义文档'
        summary = definition.get('summary', [])
        if not summary:
            return '待评估'
        return '<ul class="list-disc list-inside space-y-1">' + ''.join([f'<li>{s}</li>' for s in summary]) + '</ul>'
    
    def _html_score_bars(self, dims: List) -> str:
        if not dims:
            return '<div class="text-gray-500 text-sm">暂无评分数据</div>'
        bars = []
        for d in dims:
            score = d.get('score', 0)
            name = d.get('name', '')
            weight = d.get('weight', 0)
            tag_class = 'tag-excellent' if score >= 70 else 'tag-good' if score >= 50 else 'tag-poor'
            bars.append(f"""
            <div class="dimension-card">
                <div class="flex justify-between items-center mb-2">
                    <span class="text-sm text-gray-300">{name}</span>
                    <div class="flex items-center gap-2">
                        <span class="text-xs text-gray-500">权重{weight}%</span>
                        <span class="tag {tag_class}">{score}分</span>
                    </div>
                </div>
                <div class="dimension-bar">
                    <div class="dimension-fill" style="width: {score}%"></div>
                </div>
            </div>""")
        return '\n'.join(bars)
    
    def _html_success_patterns(self, patterns: Dict) -> str:
        if not patterns:
            return '<div class="text-gray-500 text-sm">暂无成功因子分析数据</div>'
        items = []
        for key, pattern in patterns.items():
            examples = pattern.get('examples', [])
            items.append(f"""
            <div class="glass-card p-4 border-l-4 border-blue-500">
                <div class="text-sm font-semibold text-white mb-2">{pattern.get('title', key)}</div>
                <div class="text-xs text-gray-400 mb-2">{'、'.join(examples)}</div>
                <div class="text-xs text-blue-400"><strong>洞察：</strong>{pattern.get('insight', '')}</div>
            </div>""")
        return '\n'.join(items)


def generate_pdf_from_html(html_path: str, pdf_path: str) -> bool:
    """使用Playwright将HTML转为PDF"""
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f'file:///{html_path}', wait_until='networkidle')
            page.pdf(path=pdf_path, format='A4', print_background=True)
            browser.close()
        return True
    except Exception as e:
        print(f"PDF生成失败（Playwright方式）: {e}")
        return False


if __name__ == '__main__':
    print("Premium Report Generator v5.0 已就绪")
    print("支持格式：Markdown / HTML / PDF")
    print("支持框架：6维度 + 17章节 + 竞品对比 + 风险矩阵 + 数据可视化")
