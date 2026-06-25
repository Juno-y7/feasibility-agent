#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整可行性分析报告生成器
整合项目所有资源：增长飞轮、市场规模、财务模型、数据指标、技术架构、时间规划、退出策略
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any


class FullReportGenerator:
    """完整报告生成器，整合项目所有模板和资源"""
    
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = os.path.dirname(__file__)
        self.base_dir = base_dir
        
        # 加载项目资源
        self.scoring_model = self._load_scoring_model()
        self.growth_flywheel = self._load_growth_flywheel()
        self.metrics_framework = self._load_metrics_framework()
        self.tech_framework = self._load_tech_framework()
        self.timeline_framework = self._load_timeline_framework()
        self.exit_strategy = self._load_exit_strategy()
        self.market_data = self._load_market_data()
        self.category_checks = self._load_category_checks()
        
        # 募资可行性评分模型
        self.crowdfunding_scoring_model = {
            'dimensions': [
                {'name': '产品展示力', 'weight': 20, 'key': 'product_showcase'},
                {'name': '信任证据', 'weight': 20, 'key': 'trust_evidence'},
                {'name': '定价合理性', 'weight': 15, 'key': 'pricing_rationality'},
                {'name': '推广准备度', 'weight': 15, 'key': 'promotion_readiness'},
                {'name': '履约能力', 'weight': 15, 'key': 'fulfillment'},
                {'name': '平台匹配度', 'weight': 15, 'key': 'platform_match'},
            ],
            'grade_levels': {
                'A+': {'min': 85, 'label': '极大可能成功', 'action': '立即上线'},
                'A': {'min': 75, 'label': '大概率成功', 'action': '准备好后上线'},
                'B': {'min': 60, 'label': '有可能成功', 'action': '需要补强后上线'},
                'C': {'min': 45, 'label': '较难成功', 'action': '需要大幅调整'},
                'D': {'min': 0, 'label': '很难成功', 'action': '不建议上线'},
            }
        }
    
    def _load_scoring_model(self) -> Dict:
        """加载评分模型"""
        return {
            'dimensions': [
                {'name': '痛点强度', 'weight': 15, 'key': 'pain_point', 'high': '高频、高价值、用户已在花钱解决', 'low': '只是新鲜有趣、低频、无付费意愿'},
                {'name': '目标用户清晰度', 'weight': 10, 'key': 'user_clarity', 'high': '能明确找到第一批100个用户', 'low': '用户太泛（"所有企业""所有人"）'},
                {'name': '竞争壁垒', 'weight': 10, 'key': 'moat', 'high': '有品牌、专利、网络效应、场景锁定', 'low': '任何人都能复制，无持续优势'},
                {'name': '产品可演示性', 'weight': 10, 'key': 'demo_ability', 'high': '30秒内能看懂价值，有Demo或实物', 'low': '只能靠文字解释概念'},
                {'name': '技术/生产可行性', 'weight': 10, 'key': 'tech_feasibility', 'high': 'MVP路径清楚，技术/供应链成本可控', 'low': '依赖不确定技术、复杂供应链'},
                {'name': '合规与信任', 'weight': 10, 'key': 'compliance', 'high': '隐私、法规、授权、安全机制清楚', 'low': '涉及用户/数据但无合规设计'},
                {'name': '商业模式', 'weight': 10, 'key': 'business_model', 'high': '定价与成本、价值、付费习惯匹配', 'low': '免费用户多但转化路径不清'},
                {'name': '市场推广可行性', 'weight': 10, 'key': 'marketing', 'high': '有冷启动路径、可规模化获客渠道', 'low': '推广计划只有"发社交媒体"'},
                {'name': '团队匹配度', 'weight': 10, 'key': 'team_fit', 'high': '团队背景与目标行业匹配', 'low': '团队能力与产品需求严重错位'},
                {'name': '证据完整度', 'weight': 5, 'key': 'evidence', 'high': '有访谈、原型、试用、付费或案例证据', 'low': '只有想法和主观判断'},
            ],
            'extra_dimensions': [
                {'name': '市场规模潜力', 'weight': 5, 'key': 'market_size', 'high': 'TAM>¥100亿，SAM>¥10亿', 'low': 'TAM<¥1亿'},
                {'name': '财务健康度', 'weight': 5, 'key': 'financial_health', 'high': '毛利率>50%，6个月盈亏平衡', 'low': '毛利率<20%'},
            ],
            'category_weights': {
                'saas': {'pain_point': 15, 'user_clarity': 10, 'moat': 10, 'demo_ability': 10, 'tech_feasibility': 8, 'compliance': 8, 'business_model': 10, 'marketing': 12, 'team_fit': 10, 'evidence': 7},
                'hardware': {'pain_point': 15, 'user_clarity': 10, 'moat': 8, 'demo_ability': 10, 'tech_feasibility': 15, 'compliance': 10, 'business_model': 12, 'marketing': 8, 'team_fit': 7, 'evidence': 5},
                'service': {'pain_point': 12, 'user_clarity': 10, 'moat': 8, 'demo_ability': 8, 'tech_feasibility': 5, 'compliance': 12, 'business_model': 12, 'marketing': 10, 'team_fit': 12, 'evidence': 11},
                'content': {'pain_point': 15, 'user_clarity': 10, 'moat': 8, 'demo_ability': 8, 'tech_feasibility': 5, 'compliance': 15, 'business_model': 8, 'marketing': 10, 'team_fit': 10, 'evidence': 11},
                'b2b': {'pain_point': 10, 'user_clarity': 8, 'moat': 10, 'demo_ability': 8, 'tech_feasibility': 10, 'compliance': 12, 'business_model': 10, 'marketing': 10, 'team_fit': 12, 'evidence': 10},
                'platform': {'pain_point': 12, 'user_clarity': 10, 'moat': 15, 'demo_ability': 8, 'tech_feasibility': 8, 'compliance': 12, 'business_model': 10, 'marketing': 12, 'team_fit': 8, 'evidence': 5},
            },
            'thresholds': {
                'mvp': {'pain_point': 10, 'demo_ability': 6, 'tech_feasibility': 7, 'user_clarity': 7},
                'fundraising': {'demo_ability': 8, 'marketing': 8, 'compliance': 7, 'team_fit': 7},
            },
            'grade_levels': {
                'A': {'min': 80, 'label': '强烈推荐', 'action': '可以进入正式开发/预热/募资阶段'},
                'B': {'min': 65, 'label': '建议补强后继续', 'action': '方向可行，但必须先补强2-3个关键短板'},
                'C': {'min': 50, 'label': '需要重新定位', 'action': '需要重新定义用户、场景或卖点'},
                'D': {'min': 0, 'label': '暂不建议投入', 'action': '暂不建议投入大量资源'},
            }
        }
    
    def _load_growth_flywheel(self) -> Dict:
        """加载增长飞轮模型"""
        return {
            'category_flywheels': {
                'hardware': {
                    'name': '硬件增长飞轮',
                    'cycle': '产品销售 → 口碑传播 → 用户增长 → 规模效应 → 成本降低 → 价格优势 → 更多销售',
                    'key_elements': ['产品质量', '口碑传播', '规模效应'],
                    'bottlenecks': ['首批用户获取', '供应链成本', '售后体系'],
                },
                'saas': {
                    'name': 'SaaS增长飞轮',
                    'cycle': '用户使用 → 数据积累 → 产品智能提升 → 用户粘性增强 → 用户推荐 → 更多用户 → 更多数据',
                    'key_elements': ['数据驱动优化', '用户粘性', '推荐机制'],
                    'bottlenecks': ['免费到付费转化', '用户留存', '竞品切换成本'],
                },
                'service': {
                    'name': '服务增长飞轮',
                    'cycle': '客户服务 → 满意度提升 → 口碑传播 → 新客户获取 → 规模扩大 → 服务能力增强 → 更好服务',
                    'key_elements': ['服务质量', '口碑传播', '规模扩张'],
                    'bottlenecks': ['服务标准化', '人才复制', '客户获取成本'],
                },
                'content': {
                    'name': '内容社群增长飞轮',
                    'cycle': '内容/互动 → 用户参与 → 社区活跃 → 更多内容 → 更多用户 → 更强社区',
                    'key_elements': ['优质内容', '社区活跃', '用户参与'],
                    'bottlenecks': ['内容生产门槛', '冷启动密度', 'UGC治理'],
                },
                'b2b': {
                    'name': 'B2B增长飞轮',
                    'cycle': '客户成功 → 续约与增购 → 口碑与案例 → 新客户获取 → 产品优化 → 更好的客户成功',
                    'key_elements': ['客户成功', '案例积累', '续约增购'],
                    'bottlenecks': ['决策周期长', 'POC转化率', '集成难度'],
                },
                'platform': {
                    'name': '平台增长飞轮',
                    'cycle': '供应方增长 → 交易体验提升 → 需求方增长 → 更多供应 → 更好体验 → 更多需求',
                    'key_elements': ['供需平衡', '交易体验', '网络效应'],
                    'bottlenecks': ['冷启动鸡生蛋', '信任机制', '防作弊'],
                },
            },
            'growth_stages': [
                {'stage': '冷启动', 'users': '0-1000', 'goal': '验证产品价值', 'strategy': '种子用户测试、用户访谈', 'metrics': ['激活率', '留存率', 'NPS']},
                {'stage': '增长期', 'users': '1000-10000', 'goal': '扩大用户规模', 'strategy': '付费广告、内容营销、SEO', 'metrics': ['用户增长', 'CAC']},
                {'stage': '规模化', 'users': '10000+', 'goal': '建立竞争壁垒', 'strategy': '网络效应、品牌建设、专利', 'metrics': ['市场份额', '品牌认知']},
            ],
        }
    
    def _load_metrics_framework(self) -> Dict:
        """加载数据指标框架"""
        return {
            'north_star': {
                'hardware': {'metric': '活跃用户数 × 客单价 × 复购率', 'description': '衡量产品被使用和产生收入的能力'},
                'saas': {'metric': 'MRR（月经常性收入）', 'description': '衡量订阅业务的健康度'},
                'service': {'metric': 'LTV（客户生命周期价值）', 'description': '衡量服务的长期价值'},
                'content': {'metric': 'DAU（日活跃用户数）', 'description': '衡量社区的活跃度和粘性'},
                'b2b': {'metric': 'ACV（年度合同价值）', 'description': '衡量企业客户的价值'},
                'platform': {'metric': 'GMV（商品交易总额）', 'description': '衡量平台的交易规模'},
            },
            'aarrr': {
                'acquisition': {'metrics': ['CAC', '渠道ROI'], 'target': 'LTV/CAC >= 3'},
                'activation': {'metrics': ['首单转化率', '核心功能使用率'], 'target': '-'},
                'retention': {'metrics': ['D1/D7/D30留存率'], 'target': 'D1>=30%, D7>=15%, D30>=5%'},
                'revenue': {'metrics': ['ARPU', '付费转化率', 'LTV'], 'target': '-'},
                'referral': {'metrics': ['NPS', '推荐转化率', '病毒系数'], 'target': '病毒系数 >= 1'},
            },
        }
    
    def _load_tech_framework(self) -> Dict:
        """加载技术架构评估框架"""
        return {
            'dimensions': [
                {'name': '技术栈成熟度', 'high': '技术成熟稳定', 'low': '技术风险高'},
                {'name': '技术复杂度', 'high': '简单可实现', 'low': '极复杂'},
                {'name': '供应链可靠性', 'high': '供应稳定', 'low': '供应风险高'},
                {'name': '安全合规', 'high': '完全合规', 'low': '严重合规问题'},
                {'name': '扩展性', 'high': '扩展性强', 'low': '扩展性差'},
            ],
            'risk_levels': {
                'high': ['核心技术未验证', '供应链单一', '合规问题'],
                'medium': ['技术复杂度高', '依赖第三方服务'],
                'low': ['技术选型保守', '有替代方案'],
            },
        }
    
    def _load_timeline_framework(self) -> Dict:
        """加载时间规划框架"""
        return {
            'stages': [
                {'stage': '验证期', 'time': '0-3个月', 'goal': '验证核心假设', 'tasks': ['用户调研', '竞品分析', 'MVP定义', '原型测试'], 'success': '种子用户验证通过'},
                {'stage': '开发期', 'time': '3-6个月', 'goal': '开发MVP', 'tasks': ['技术架构搭建', '核心功能开发', '测试修复'], 'success': 'MVP完成内部验收'},
                {'stage': '内测期', 'time': '6-9个月', 'goal': '小范围测试', 'tasks': ['内测用户招募', '反馈收集', '迭代优化'], 'success': '内测用户满意度达标'},
                {'stage': '公测期', 'time': '9-12个月', 'goal': '公开测试', 'tasks': ['公测用户扩展', '付费转化测试', '市场推广'], 'success': '商业模式验证通过'},
                {'stage': '规模化期', 'time': '12个月+', 'goal': '快速增长', 'tasks': ['用户规模扩大', '收入模式优化', '团队扩充'], 'success': '建立竞争壁垒'},
            ],
        }
    
    def _load_exit_strategy(self) -> Dict:
        """加载退出策略框架"""
        return {
            'options': [
                {'option': '被收购', 'condition': '有收购意向方', 'timing': '产品有一定规模和用户', 'return': '中等-高', 'risk': '估值不确定'},
                {'option': 'IPO', 'condition': '达到上市标准', 'timing': '公司成熟，财务健康', 'return': '高', 'risk': '周期长，门槛高'},
                {'option': '股权转让', 'condition': '找到接盘方', 'timing': '创始人想退出', 'return': '中等', 'risk': '流动性差'},
                {'option': '停业清算', 'condition': '无法继续运营', 'timing': '资金耗尽，无融资可能', 'return': '低', 'risk': '损失投资'},
            ],
            'stop_loss': [
                {'type': '财务止损', 'indicator': '现金储备', 'threshold': '低于3个月运营成本', 'action': '启动紧急融资或缩减成本'},
                {'type': '财务止损', 'indicator': '收入增长', 'threshold': '连续3个月低于目标50%', 'action': '重新评估商业模式'},
                {'type': '用户止损', 'indicator': 'D7留存率', 'threshold': '低于15%', 'action': '重新评估产品价值'},
                {'type': '用户止损', 'indicator': '付费转化率', 'threshold': '低于1%', 'action': '重新设计定价和价值主张'},
                {'type': '运营止损', 'indicator': '团队流失率', 'threshold': '季度超过30%', 'action': '审查企业文化和薪酬'},
            ],
        }
    
    def _load_market_data(self) -> Dict:
        """加载市场数据"""
        return {
            'ai_hardware': {
                'global_market_2026': '$800亿',
                'china_market_2026': '¥2,000亿',
                'growth_rate': '35%',
                'kickstarter_avg': '$50万-$100万',
                'zeczec_avg': '¥500万-¥1,500万',
            },
            'tam_som_guide': [
                {'level': 10, 'tam': '>¥100亿', 'sam': '>¥10亿', 'som': '>¥1亿'},
                {'level': 8, 'tam': '¥50-100亿', 'sam': '¥5-10亿', 'som': '¥5,000万-1亿'},
                {'level': 6, 'tam': '¥10-50亿', 'sam': '¥1-5亿', 'som': '¥1,000万-5,000万'},
                {'level': 4, 'tam': '¥1-10亿', 'sam': '¥1,000万-1亿', 'som': '¥100万-1,000万'},
                {'level': 2, 'tam': '<¥1亿', 'sam': '<¥1,000万', 'som': '<¥100万'},
            ],
        }
    
    def _load_category_checks(self) -> Dict:
        """加载品类特别检查项"""
        return {
            'hardware': [
                '供应链韧性：关键元器件是否受制于单一供应商？',
                'BOM成本与定价的毛利空间是否合理？',
                '模具/开模周期和首批量产时间表是否现实？',
                '物流、关税、退货处理是否有预案？',
            ],
            'saas': [
                '用户是否有持续使用理由，还是一次性体验？',
                '竞品的切换成本有多高？',
                'API/基础设施依赖风险（如OpenAI、AWS政策变化）？',
                '免费tier到付费的转化路径是否清晰？',
            ],
            'service': [
                '服务是否可标准化，还是只能靠人堆？',
                '单个客户的交付成本与收入是否可持续？',
                '规模化瓶颈在哪里？',
                '客户获取是否依赖个人关系？',
            ],
            'content': [
                '伦理边界：是否涉及情感操控、防沉迷、未成年人保护？',
                '持续使用动机：用户为什么每天都回来？',
                '内容治理：UGC内容审核和风险如何管理？',
                '是否容易引发舆论风险或监管关注？',
            ],
            'b2b': [
                '企业决策链长度和周期是否在可控范围？',
                'POC到付费的转化率预期？',
                '合规认证（ISO、SOC2、信创等）是否必要？',
                '集成难度和客户IT支持能力是否匹配？',
            ],
            'platform': [
                '先发哪一侧？冷启动的"鸡生蛋"问题如何解决？',
                '网络效应拐点在哪里？需要多少用户才能自运转？',
                '平台抽佣和定价机制是否合理？',
                '防止作弊和信任机制如何设计？',
            ],
        }
    
    def generate_full_report(self, analysis_data: Dict) -> str:
        """生成完整的募资可行性分析Markdown报告"""
        sections = []
        
        # 0. 执行摘要（募资视角）
        sections.append(self._generate_executive_summary(analysis_data))
        
        # 1. 项目画像识别
        sections.append(self._generate_project_profile(analysis_data))
        
        # 2. 募资可行性评分（核心章节）
        sections.append(self._generate_crowdfunding_scoring(analysis_data))
        
        # 3. 平台选择与匹配分析
        sections.append(self._generate_crowdfunding_platform_analysis(analysis_data))
        
        # 4. 竞品案例与募资表现
        sections.append(self._generate_competitor_case_study(analysis_data))
        
        # 5. 募资定价策略
        sections.append(self._generate_crowdfunding_pricing(analysis_data))
        
        # 6. 推广策略与时间线
        sections.append(self._generate_crowdfunding_promotion(analysis_data))
        
        # 7. 平台审核准备清单
        sections.append(self._generate_crowdfunding_checklist(analysis_data))
        
        # 8. SWOT分析（募资视角）
        sections.append(self._generate_swot_analysis(analysis_data))
        
        # 9. 财务模型分析（侧重募资收入）
        sections.append(self._generate_financial_model(analysis_data))
        
        # 10. 市场规模估算（参考）
        sections.append(self._generate_market_sizing(analysis_data))
        
        # 11. 市场分析 + PEST（参考）
        sections.append(self._generate_market_analysis(analysis_data))
        
        # 12. 商业模式画布（参考）
        sections.append(self._generate_business_model_canvas(analysis_data))
        
        # 13. 增长飞轮 + 指标 + 技术（参考）
        sections.append(self._generate_growth_flywheel(analysis_data))
        sections.append(self._generate_metrics_framework(analysis_data))
        sections.append(self._generate_tech_architecture(analysis_data))
        
        # 16. 附录（退出策略、时间规划、通用评分）
        sections.append(self._generate_appendix(analysis_data))
        
        # 14. 募资行动建议
        sections.append(self._generate_action_plan(analysis_data))
        
        # 15. 沟通话术
        sections.append(self._generate_communication_script(analysis_data))
        
        return '\n\n'.join(sections)
    
    def _generate_executive_summary(self, data: Dict) -> str:
        """生成执行摘要（募资可行性视角）"""
        product = data.get('product', {})
        scoring = data.get('scoring', {})
        score = scoring.get('total_score', 0)
        
        # 计算募资评分
        cf_score, cf_grade, cf_label, _ = self._calc_crowdfunding_score(data)
        
        grade = 'D'
        for g, info in self.scoring_model['grade_levels'].items():
            if score >= info['min']:
                grade = g
                break
        
        # 募资成功概率判断
        if cf_score >= 75:
            cf_verdict = '大概率可以'
        elif cf_score >= 60:
            cf_verdict = '有可能可以'
        elif cf_score >= 45:
            cf_verdict = '较难'
        else:
            cf_verdict = '很难'
        
        # 推荐平台
        recommended_platform = product.get('platform', 'Kickstarter')
        if recommended_platform in ('zeczec', '啧啧', '嘖嘖'):
            recommended_platform = '嘖嘖'
        
        # 建议目标金额
        target_amount = product.get('target_amount')
        if target_amount:
            if isinstance(target_amount, (int, float)) and target_amount > 1000:
                target_amount_str = "¥" + f"{target_amount:,}"
            else:
                target_amount_str = "¥" + str(target_amount)
        else:
            target_amount_str = '待评估'
        
        # 预计支持者
        financials = data.get('financial_analysis', {})
        backers = financials.get('backers_needed', {}).get('total_backers', 'XX')
        
        # 早鸟定价
        cost = product.get('cost', 500)
        try:
            cost_num = float(str(cost).replace(',', '').replace('¥', '').replace('$', ''))
        except (ValueError, TypeError):
            cost_num = 500
        early_bird = int(cost_num * 1.3)
        
        product_name = product.get('name', '未命名产品')
        category = data.get('category', '未识别')
        value_prop = product.get('value_proposition', '待补充')
        target_users = product.get('target_users', '待补充')
        
        lines = []
        lines.append("# 0. 执行摘要")
        lines.append("")
        lines.append("## 项目概述")
        lines.append("- **产品名称**：" + product_name)
        lines.append("- **品类**：" + str(category))
        lines.append("- **核心价值**：" + str(value_prop))
        lines.append("- **目标用户**：" + str(target_users))
        lines.append("")
        lines.append("### 核心结论")
        lines.append("> 这个项目在募资平台上 **" + cf_verdict + "** 成功募资。")
        lines.append("")
        lines.append("### 关键募资指标")
        lines.append("| 指标 | 数值 | 说明 |")
        lines.append("| --- | --- | --- |")
        lines.append("| 募资可行性评分 | " + str(cf_score) + "/100 | 综合评估 |")
        lines.append("| 推荐平台 | " + str(recommended_platform) + " | 最佳匹配平台 |")
        lines.append("| 建议目标金额 | " + target_amount_str + " | 基于品类平均表现 |")
        lines.append("| 预计支持者 | " + str(backers) + "人 | 基于平均pledge估算 |")
        lines.append("| 早鸟定价 | ¥" + str(early_bird) + " | 基于成本+合理毛利 |")
        lines.append("")
        lines.append("## 最大优势")
        lines.append(self._format_list(data.get('strengths', ['待补充']), '优势'))
        lines.append("")
        lines.append("## 最大风险")
        lines.append(self._format_list(data.get('risks', ['待补充']), '风险'))
        lines.append("")
        lines.append("## 最需要补强")
        lines.append(self._format_list(data.get('need_improve', ['待补充']), '短板'))
        
        return '\n'.join(lines)
    
    def _generate_project_profile(self, data: Dict) -> str:
        """生成项目画像"""
        product = data.get('product', {})
        category = data.get('category', 'default')
        
        profile = f"""# 1. 项目画像识别

## 1.1 品类识别
- **识别品类**：{category}
- **识别依据**：基于产品描述关键词匹配

## 1.2 痛点分析
- **核心痛点**：{product.get('pain_points', '待补充')}
- **痛点强度**：{self._assess_pain_level(product)}
- **现有解决方案**：{product.get('current_alternatives', '待补充')}
- **方案不足**：{product.get('alternative_weakness', '待补充')}

## 1.3 参照项目
| 项目名称 | 品类 | 募集金额 | 支持者 | 达成率 |
| --- | --- | --- | --- | --- |
{self._format_reference_projects(data.get('similar_cases', []))}

## 1.4 品类特别检查项
{self._format_category_checks(category)}"""
        
        return profile
    
    def _generate_market_analysis(self, data: Dict) -> str:
        """生成市场分析"""
        category = data.get('category', 'default')
        market_data = self.market_data.get('ai_hardware', {})
        
        analysis = f"""# 11. 市场分析 + PEST（参考）

## 11.1 PEST分析
| 维度 | 分析 | 影响 |
| --- | --- | --- |
| 政治(P) | AI产业政策支持，数据安全法规趋严 | 中等正面 + 需合规 |
| 经济(E) | AI硬件市场年增长35%，消费升级趋势 | 高正面 |
| 社会(S) | AI工具教育完成，用户接受度高 | 高正面 |
| 技术(T) | AI技术成熟，供应链完善 | 高正面 |

## 11.2 波特五力分析
| 力量 | 分析 | 强度 |
| --- | --- | --- |
| 供应商议价能力 | AI芯片供应商集中，议价能力强 | 高 |
| 购买者议价能力 | 消费者选择多，价格敏感 | 中 |
| 新进入者威胁 | 技术门槛降低，进入者增多 | 高 |
| 替代品威胁 | 手机APP、云端服务替代 | 中 |
| 行业竞争程度 | 同质化严重，竞争激烈 | 高 |

## 11.3 市场趋势
- **全球AI硬件市场**：{market_data.get('global_market_2026', '$800亿')}（{market_data.get('growth_rate', '35%')}年增长）
- **中国AI硬件市场**：{market_data.get('china_market_2026', '¥2,000亿')}
- **募资平台表现**：Kickstarter平均募集{market_data.get('kickstarter_avg', '$50万-$100万')}，啧啧平均募集{market_data.get('zeczec_avg', '¥500万-¥1,500万')}"""
        
        return analysis
    
    def _generate_swot_analysis(self, data: Dict) -> str:
        """生成SWOT分析"""
        swot = data.get('swot', {})
        
        analysis = f"""# 8. SWOT分析（募资视角）

## 8.1 优势(Strengths) - 募资视角
| 条目 | 影响程度 | 证据强度 | 处理建议 |
| --- | --- | --- | --- |
{self._format_swot_items(swot.get('strengths', []))}

## 8.2 劣势(Weaknesses) - 募资视角
| 条目 | 影响程度 | 证据强度 | 处理建议 |
| --- | --- | --- | --- |
{self._format_swot_items(swot.get('weaknesses', []))}

## 8.3 机会(Opportunities) - 募资视角
| 条目 | 影响程度 | 证据强度 | 处理建议 |
| --- | --- | --- | --- |
{self._format_swot_items(swot.get('opportunities', []))}

## 8.4 威胁(Threats) - 募资视角
| 条目 | 影响程度 | 证据强度 | 处理建议 |
| --- | --- | --- | --- |
{self._format_swot_items(swot.get('threats', []))}"""
        
        return analysis
    
    def _generate_business_model_canvas(self, data: Dict) -> str:
        """生成商业模式画布"""
        product = data.get('product', {})
        
        canvas = f"""# 12. 商业模式画布（参考）

| 模块 | 内容 |
| --- | --- |
| **价值主张** | {product.get('value_proposition', '待补充')} |
| **客户细分** | {product.get('target_users', '待补充')} |
| **渠道通路** | {product.get('channels', '募资平台、社交媒体、KOL合作')} |
| **客户关系** | {product.get('customer_relation', '社群运营、用户反馈、持续迭代')} |
| **收入来源** | {product.get('revenue_source', '产品销售、订阅服务')} |
| **核心资源** | {product.get('key_resources', '技术团队、供应链、品牌')} |
| **关键业务** | {product.get('key_activities', '产品研发、生产制造、市场推广')} |
| **重要合作** | {product.get('key_partners', '供应商、分销渠道、技术伙伴')} |
| **成本结构** | {product.get('cost_structure', '硬件成本、研发成本、营销成本')} |"""
        
        return canvas
    
    def _generate_competitor_case_study(self, data: Dict) -> str:
        """生成竞品案例研究"""
        competitors = data.get('competitor_analysis', {}).get('competitors', [])
        real_cases = data.get('competitor_analysis', {}).get('real_cases', [])
        
        study = f"""# 4. 竞品案例与募资表现

## 4.1 直接竞品
| 竞品名称 | 品类 | 核心功能 | 价格 | 与本项目关系 |
| --- | --- | --- | --- | --- |
{self._format_competitors(competitors[:5])}

## 4.2 相似募资成功案例
| 案例名称 | 平台 | 募集金额 | 支持者 | 成功因素 |
| --- | --- | --- | --- | --- |
{self._format_success_cases(real_cases[:5])}

## 4.3 募资成功因素提炼
{self._extract_success_factors(real_cases)}

## 4.4 募资失败风险预警
{self._extract_failure_warnings(real_cases)}"""
        
        return study
    
    def _generate_market_sizing(self, data: Dict) -> str:
        """生成市场规模估算"""
        product = data.get('product', {})
        
        sizing = f"""# 10. 市场规模估算（参考）

## 10.1 TAM/SAM/SOM分析
| 指标 | 定义 | 估算值 | 依据 |
| --- | --- | --- | --- |
| TAM | 总可寻址市场 | {data.get('tam', '¥100亿+')} | 全球AI硬件市场规模 |
| SAM | 可服务市场 | {data.get('sam', '¥10亿')} | 目标地区细分市场 |
| SOM | 可获得市场 | {data.get('som', '¥1亿')} | 预期市场份额 |

## 10.2 市场增长率
- **年增长率**：35%
- **增长驱动因素**：AI技术普及、消费升级、智能家居趋势

## 10.3 市场规模评分
- **得分**：{data.get('market_size_score', 8)}/10
- **依据**：{self._get_market_size_reason(data.get('som', ''))}"""
        
        return sizing
    
    def _generate_financial_model(self, data: Dict) -> str:
        """生成财务模型分析"""
        financials = data.get('financial_analysis', {})
        product = data.get('product', {})
        
        model = f"""# 9. 财务模型分析

## 9.1 收入预测（侧重募资收入）
| 指标 | 数值 | 说明 |
| --- | --- | --- |
| 目标募资金额 | {(product.get('target_amount') or '¥500,000')} | 基于首批生产需求 |
| 预计支持者数量 | {financials.get('backers_needed', {}).get('total_backers', 1000)}人 | 基于平均单价估算 |
| 平均单价 | ¥{financials.get('pricing', {}).get('retail_price', 600)} | 基于成本+毛利 |
| 平台费 | 8% | 嘖嘖平台费率 |
| 支付手续费 | 2-3% | 支付渠道费率 |
| 实际到手收入 | ¥{financials.get('revenue', {}).get('actual_revenue_cny', 450000)} | 扣除费用后 |

## 9.2 成本结构
| 成本类型 | 金额 | 占比 | 说明 |
| --- | --- | --- | --- |
| 硬件/BOM成本 | ¥{product.get('cost') or 300} | 50% | 核心成本 |
| 制造成本 | ¥50 | 8% | 组装、测试 |
| 运输成本 | ¥30 | 5% | 物流、包装 |
| 营销成本 | ¥100 | 17% | 推广、KOL |
| 运营成本 | ¥120 | 20% | 团队、办公 |
| **总成本** | ¥{(product.get('cost') or 300) + 300} | **100%** | |

## 9.3 盈利分析（含平台费）
| 指标 | 数值 | 说明 |
| --- | --- | --- |
| 毛利率 | {financials.get('margin', 50)}% | (售价-成本)/售价 |
| 盈亏平衡点 | {financials.get('breakeven', {}).get('backers_needed', 723)}人 | 固定成本/(售价-可变成本) |
| 回收期 | {data.get('payback_period', '12-18个月')} | 基于月净利润估算 |

## 9.4 财务健康度评分
- **得分**：{data.get('financial_health_score', 7)}/10
- **依据**：毛利率{financials.get('margin', 50)}%，盈亏平衡可行"""
        
        return model
    
    def _generate_growth_flywheel(self, data: Dict) -> str:
        """生成增长飞轮分析"""
        category = data.get('category', 'hardware')
        flywheel = self.growth_flywheel['category_flywheels'].get(category, 
            self.growth_flywheel['category_flywheels']['hardware'])
        
        analysis = f"""# 13. 增长飞轮（参考）

## 13.1 增长飞轮设计
- **飞轮名称**：{flywheel['name']}
- **飞轮结构**：{flywheel['cycle']}
- **关键环节**：{', '.join(flywheel['key_elements'])}
- **自我强化机制**：每个环节的成功推动下一个环节，形成持续增长循环

## 13.2 增长阶段规划
| 阶段 | 用户规模 | 目标 | 策略 | 关键指标 |
| --- | --- | --- | --- | --- |
{self._format_growth_stages()}

## 13.3 增长瓶颈识别
{self._format_list(flywheel['bottlenecks'], '瓶颈')}"""
        
        return analysis
    
    def _generate_metrics_framework(self, data: Dict) -> str:
        """生成数据指标框架"""
        category = data.get('category', 'hardware')
        north_star = self.metrics_framework['north_star'].get(category,
            self.metrics_framework['north_star']['hardware'])
        
        framework = f"""# 13b. 数据指标框架（参考）

## 13b.1 北极星指标
- **指标**：{north_star['metric']}
- **说明**：{north_star['description']}
- **目标值**：{data.get('north_star_target', '待设定')}

## 13b.2 AARRR漏斗指标
| 环节 | 关键指标 | 当前值 | 目标值 |
| --- | --- | --- | --- |
{self._format_aarrr_metrics()}

## 13b.3 品类特定指标
{self._format_category_metrics(category)}"""
        
        return framework
    
    def _generate_tech_architecture(self, data: Dict) -> str:
        """生成技术架构评估"""
        category = data.get('category', 'hardware')
        
        assessment = f"""# 13c. 技术架构（参考）

## 13c.1 技术可行性分析
| 维度 | 评估 | 风险等级 | 应对建议 |
| --- | --- | --- | --- |
{self._format_tech_dimensions()}

## 13c.2 技术风险清单
- **高风险**：{', '.join(self.tech_framework['risk_levels']['high'][:3])}
- **中风险**：{', '.join(self.tech_framework['risk_levels']['medium'][:2])}
- **低风险**：{', '.join(self.tech_framework['risk_levels']['low'][:2])}

## 13c.3 MVP技术方案
- **核心功能范围**：{data.get('mvp_features', '语音交互、情感识别、个性化定制')}
- **技术架构**：{data.get('tech_stack', 'AI模型 + 硬件模块 + 云端服务')}
- **开发周期**：{data.get('dev_cycle', '3-6个月')}"""
        
        return assessment
    
    def _generate_feasibility_scoring(self, data: Dict) -> str:
        """生成可行性评分"""
        scoring = data.get('scoring', {})
        score = scoring.get('total_score', 0)
        
        grade = 'D'
        for g, info in self.scoring_model['grade_levels'].items():
            if score >= info['min']:
                grade = g
                break
        
        grade_info = self.scoring_model['grade_levels'].get(grade, {})
        
        scoring_section = f"""# 11. 可行性评分

## 11.1 评分表
| 维度 | 得分 | 权重 | 加权分 | 说明 |
| --- | ---: | ---: | ---: | --- |
{self._format_scoring_table(scoring)}

## 11.2 评分结论
- **总分**：{score}/100
- **评级**：{grade} - {grade_info.get('label', '未评级')}
- **结论**：{grade_info.get('action', '待评估')}

## 11.3 优势与短板
- **最大优势**：{', '.join(scoring.get('strengths', ['待补充'])[:3])}
- **最大短板**：{', '.join(scoring.get('weaknesses', ['待补充'])[:3])}"""
        
        return scoring_section
    
    def _generate_timeline(self, data: Dict) -> str:
        """生成时间规划"""
        timeline = f"""# 12. 时间规划

## 12.1 项目阶段划分
| 阶段 | 时间 | 目标 | 关键任务 | 成功标准 |
| --- | --- | --- | --- | --- |
{self._format_timeline_stages()}

## 12.2 关键路径
- **最长任务链**：用户调研 → MVP开发 → 内测 → 公测 → 规模化
- **关键任务**：MVP开发、首批用户获取、商业模式验证

## 12.3 资源规划
- **人力配置**：{data.get('team_size', '3-5人核心团队')}
- **预算分配**：{data.get('budget', '研发40%、生产30%、营销20%、运营10%')}"""
        
        return timeline
    
    def _generate_crowdfunding_analysis(self, data: Dict) -> str:
        """生成募资平台专项分析"""
        product = data.get('product', {})
        category = data.get('category', 'hardware')
        product_name = product.get('name', '未命名产品')
        cost_raw = product.get('cost', 300)

        # 安全获取成本数值
        try:
            cost = float(str(cost_raw).replace(',', '').replace('¥', '').replace('NT$', '').replace('$', ''))
        except (ValueError, TypeError):
            cost = 300

        crowdfunding = data.get('crowdfunding', {})

        # 根据品类推荐平台
        platform_map = {
            'hardware': [('Kickstarter', 5, '全球最大，适合硬件/创新产品出海', '5%+3%', '$10万-$100万'),
                         ('嘖嘖', 4, '台湾最大众筹平台，适合中文市场', '5%+3%', '¥500万-¥1500万'),
                         ('Indiegogo', 3, '灵活审核，适合有争议或创新产品', '5%+5%', '$5万-$50万'),
                         ('FlyingV', 3, '台湾本土，适合文创/设计类', '8%+3%', '¥200万-¥800万'),
                         ('摩点', 3, '中国大陆，适合ACG/文创', '5%+3%', '¥100万-¥500万')],
            'ai': [('Kickstarter', 5, '全球最大，适合AI硬件出海', '5%+3%', '$10万-$100万'),
                   ('嘖嘖', 4, '台湾最大众筹平台，适合中文市场', '5%+3%', '¥500万-¥1500万'),
                   ('Indiegogo', 3, '灵活审核，适合有争议或创新产品', '5%+5%', '$5万-$50万'),
                   ('FlyingV', 3, '台湾本土，适合文创/设计类', '8%+3%', '¥200万-¥800万'),
                   ('摩点', 3, '中国大陆，适合ACG/文创', '5%+3%', '¥100万-¥500万')],
            'saas': [('Kickstarter', 5, '全球最大，适合软件工具类', '5%+3%', '$5万-$50万'),
                     ('摩点', 3, '中国大陆，适合软件工具', '5%+3%', '¥100万-¥500万'),
                     ('嘖嘖', 3, '台湾最大众筹平台', '5%+3%', '¥500万-¥1500万'),
                     ('Indiegogo', 3, '灵活审核，适合创新软件', '5%+5%', '$5万-$50万'),
                     ('FlyingV', 2, '台湾本土，适合文创类', '8%+3%', '¥200万-¥800万')],
            'content': [('Patreon', 5, '最适合内容创作者持续募资', '5%-12%', '$1千-$10万'),
                        ('嘖嘖', 4, '台湾最大，适合内容项目', '5%+3%', '¥500万-¥1500万'),
                        ('Kickstarter', 4, '全球最大，适合内容出海', '5%+3%', '$5万-$50万'),
                        ('FlyingV', 3, '台湾本土，适合文创/播客', '8%+3%', '¥200万-¥800万'),
                        ('摩点', 4, '中国大陆，适合ACG/内容', '5%+3%', '¥100万-¥500万')],
            'service': [('嘖嘖', 5, '台湾最大，适合服务类项目', '5%+3%', '¥500万-¥1500万'),
                        ('FlyingV', 4, '台湾本土，适合服务/设计', '8%+3%', '¥200万-¥800万'),
                        ('Kickstarter', 3, '全球最大，适合创新服务', '5%+3%', '$5万-$50万'),
                        ('Indiegogo', 3, '灵活审核', '5%+5%', '$5万-$50万'),
                        ('摩点', 2, '中国大陆', '5%+3%', '¥100万-¥500万')],
            'community': [('嘖嘖', 5, '台湾最大，适合社群类项目', '5%+3%', '¥500万-¥1500万'),
                          ('Patreon', 5, '最适合社群持续运营', '5%-12%', '$1千-$10万'),
                          ('Kickstarter', 3, '全球最大', '5%+3%', '$5万-$50万'),
                          ('FlyingV', 3, '台湾本土', '8%+3%', '¥200万-¥800万'),
                          ('Indiegogo', 2, '灵活审核', '5%+5%', '$5万-$50万')],
            'platform': [('Kickstarter', 5, '全球最大，适合平台类项目', '5%+3%', '$10万-$100万'),
                         ('Indiegogo', 4, '灵活审核，适合创新平台', '5%+5%', '$5万-$50万'),
                         ('嘖嘖', 3, '台湾最大', '5%+3%', '¥500万-¥1500万'),
                         ('FlyingV', 2, '台湾本土', '8%+3%', '¥200万-¥800万'),
                         ('摩点', 2, '中国大陆', '5%+3%', '¥100万-¥500万')],
            'b2b': [('Indiegogo', 5, '灵活审核，适合B2B创新产品', '5%+5%', '$5万-$50万'),
                    ('Kickstarter', 4, '全球最大，适合B2B硬件/工具', '5%+3%', '$10万-$100万'),
                    ('嘖嘖', 3, '台湾最大', '5%+3%', '¥500万-¥1500万'),
                    ('FlyingV', 2, '台湾本土', '8%+3%', '¥200万-¥800万'),
                    ('摩点', 2, '中国大陆', '5%+3%', '¥100万-¥500万')],
        }

        # 如果品类不在映射中，使用默认
        platforms = platform_map.get(category, platform_map['hardware'])

        # 如果crowdfunding数据中有推荐，使用它
        recommended = crowdfunding.get('recommended', platforms[0][0])

        platform_table = "| 平台 | 推荐指数 | 适用理由 | 平台费率 | 平均募集 |\n"
        platform_table += "|---|---|---|---|---|\n"
        for p in platforms:
            stars = '★' * p[1] + '☆' * (5 - p[1])
            platform_table += f"| {p[0]} | {stars} | {p[2]} | {p[3]} | {p[4]} |\n"

        # 定价策略
        early_bird = int(cost * 1.3)
        standard = int(cost * 1.7)
        premium = int(cost * 2.5)

        pricing_table = "| 档位 | 价格 | 数量限制 | 内容 | 预期转化 |\n"
        pricing_table += "|---|---|---|---|---|\n"
        pricing_table += f"| 早鸟档 | ¥{early_bird} | 前100名 | 标准版+感谢信 | 40% |\n"
        pricing_table += f"| 标准档 | ¥{standard} | 500名 | 标准版+配件 | 45% |\n"
        pricing_table += f"| 豪华档 | ¥{premium} | 50名 | 全套+定制+优先发货 | 15% |\n"

        analysis = f"""## 募资平台专项分析

### 平台选择建议
根据 {product_name} 的品类（{category}）和目标市场，推荐平台：

{platform_table}

**推荐平台：{recommended}**

### 募资定价策略
基于成本 ¥{cost:.0f}，建议三档定价：

{pricing_table}

### 推广策略时间线
| 阶段 | 时间 | 核心动作 | 目标 |
|---|---|---|---|
| 预热期 | 上线前30天 | 社群运营、邮件列表、KOL种草 | 积累500+潜在backer |
| 首日冲刺 | Day 1 | 紧迫感营销、亲友支持、社群转发 | 达标30% |
| 持续期 | Day 2-25 | 每日更新、回复留言、KOL评测 | 达标75% |
| 收尾冲刺 | Day 26-30 | 追加福利、限时加价、社交分享 | 达标100%+ |

### 平台审核准备清单
- [ ] 产品名称和一句话介绍（50字内）
- [ ] 项目故事/团队介绍（800字以上）
- [ ] 产品原型/Demo/渲染图（至少5张）
- [ ] 募资视频（1-3分钟）
- [ ] 回报档位设计（至少3档）
- [ ] 风险说明和退换政策
- [ ] 团队背景和执行能力证明
- [ ] 供应链/生产计划（硬件类必填）
- [ ] 预计交付时间和物流方案"""

        return analysis

    def _generate_exit_strategy(self, data: Dict) -> str:
        """生成退出策略"""
        strategy = f"""# 13. 退出策略与止损机制

## 13.1 退出选项评估
| 选项 | 可行性 | 时机 | 预期回报 | 风险 |
| --- | --- | --- | --- | --- |
{self._format_exit_options()}

## 13.2 止损触发条件
| 类型 | 指标 | 阈值 | 触发动作 |
| --- | --- | --- | --- |
{self._format_stop_loss_conditions()}

## 13.3 风险监控体系
- **监控频率**：每周财务复盘、每月用户指标复盘
- **预警线**：现金储备<3个月、D7留存<15%、付费转化<1%
- **责任人**：创始人/CEO"""
        
        return strategy
    
    def _generate_action_plan(self, data: Dict) -> str:
        """生成行动建议"""
        plan = f"""# 14. 募资行动建议

## 14.1 上线前7天验证任务
| 任务 | 目的 | 产出 | 完成标准 |
| --- | --- | --- | --- |
| 用户访谈（5-10人） | 验证痛点真实性和付费意愿 | 访谈记录 | 80%用户认同痛点 |
| 竞品深度分析 | 了解竞品优缺点 | 竞品分析报告 | 覆盖3-5个直接竞品 |
| MVP原型制作 | 验证产品可演示性 | 产品原型/Demo | 30秒内讲清价值 |
| 成本核算 | 确认成本结构 | 成本清单 | 毛利率>=50% |
| 目标用户画像 | 明确第一批用户 | 用户画像文档 | 可执行的获客渠道 |

## 14.2 上线前30天推进计划
| 周期 | 重点 | 产出 |
| --- | --- | --- |
| 第1周 | 产品定义与原型 | MVP功能清单、产品原型 |
| 第2周 | 市场验证与竞品 | 用户访谈报告、竞品分析 |
| 第3周 | 财务与定价 | 财务模型、定价方案 |
| 第4周 | 推广准备 | 预热计划、募资文案草稿 |

## 14.3 需要补强的关键短板
{self._format_list(data.get('need_improve', ['待补充']), '短板')}"""
        
        return plan
    
    def _generate_communication_script(self, data: Dict) -> str:
        """生成沟通话术"""
        product = data.get('product', {})
        scoring = data.get('scoring', {})
        score = scoring.get('total_score', 0)
        
        script = f"""# 15. 沟通话术

## 给投资人
我们正在做一款{product.get('name', '')}，帮用户解决{product.get('description', '')[:50]}的问题。目前已完成初步验证，可行性评分{score}/100，计划通过{product.get('platform', '募资平台')}进行募资，目标金额{(product.get('target_amount') or '')}。核心优势是{', '.join(scoring.get('strengths', ['待补充'])[:2])}，需要补强的是{', '.join(scoring.get('weaknesses', ['待补充'])[:2])}。

## 给合作伙伴
{product.get('name', '')}是一款面向{product.get('target_users', '')}的产品，核心价值在于{product.get('value_proposition', '')}。我们正在寻找{product.get('cooperation', '供应链、渠道')}方面的合作伙伴，共同推动产品落地。

## 给募资平台审核
本项目属于{data.get('category', '')}品类，已有产品原型，团队具备相关经验。目标用户明确，痛点真实存在，商业模式清晰。预计募集{(product.get('target_amount') or '')}，用于首批生产和市场推广。"""
        
        return script
    
    # ============ 募资可行性分析方法 ============

    def _calc_crowdfunding_score(self, data: Dict):
        """计算募资可行性评分，返回 (总分, 评级, 标签)"""
        product = data.get('product', {})
        description = str(product.get('description', '') + ' ' + product.get('value_proposition', '') + ' ' + str(product.get('features', []))).lower()
        text_lower = description
        
        # 1. 产品展示力 (0-100)
        showcase_score = 50
        if any(k in text_lower for k in ['demo', '原型', '视频', '渲染图', '样品', '样机', 'prototype', '实物']):
            showcase_score = 85
        elif any(k in text_lower for k in ['概念', '设计图', '概念图', '设计稿']):
            showcase_score = 60
        elif any(k in text_lower for k in ['硬件', '设备', '实体', '耳机', '机器人', '音箱', '手表']):
            showcase_score = 70
        
        # 2. 信任证据 (0-100)
        trust_score = 50
        if any(k in text_lower for k in ['团队经验', '过往项目', '专利', '合作', '行业资深', '专家', '连续创业']):
            trust_score = 80
        elif any(k in text_lower for k in ['初创', '学生', '新团队']):
            trust_score = 40
        elif any(k in text_lower for k in ['有经验', '有资源', '有背景']):
            trust_score = 75
        
        # 3. 定价合理性 (0-100)
        pricing_score = 60
        cost_raw = product.get('cost')
        target_raw = product.get('target_amount')
        try:
            cost_val = float(str(cost_raw).replace(',', '').replace('¥', '').replace('$', ''))
            target_val = float(str(target_raw).replace(',', '').replace('¥', '').replace('$', ''))
            if cost_val > 0 and target_val > 0:
                ratio = target_val / cost_val
                if 100 <= ratio <= 10000:
                    pricing_score = 70
                elif ratio < 100:
                    pricing_score = 40
                elif ratio > 10000:
                    pricing_score = 45
        except (ValueError, TypeError):
            pricing_score = 50
        
        # 4. 推广准备度 (0-100)
        promo_score = 50
        if any(k in text_lower for k in ['社群', '粉丝', '邮件列表', 'kol', '网红', '自媒体', '频道']):
            promo_score = 80
        elif any(k in text_lower for k in ['社交媒体', '推广', '营销']):
            promo_score = 60
        
        # 5. 履约能力 (0-100)
        fulfill_score = 50
        if any(k in text_lower for k in ['供应链', '工厂', '生产计划', '交期', '量产', '代工']):
            fulfill_score = 80
        elif any(k in text_lower for k in ['制造', '组装', '生产']):
            fulfill_score = 65
        
        # 6. 平台匹配度 (0-100)
        platform_score = 60
        platform = product.get('platform', '')
        if platform and platform not in ('', None):
            platform_score = 80
        elif any(k in text_lower for k in ['硬件', '智能', '设备', '创新', '科技']):
            platform_score = 70
        
        scores_dict = {
            '产品展示力': showcase_score,
            '信任证据': trust_score,
            '定价合理性': pricing_score,
            '推广准备度': promo_score,
            '履约能力': fulfill_score,
            '平台匹配度': platform_score,
        }
        
        # 计算加权总分
        total = 0
        for dim in self.crowdfunding_scoring_model['dimensions']:
            name = dim['name']
            weight = dim['weight']
            score_val = scores_dict.get(name, 50)
            total += score_val * weight // 100
        
        # 评级
        grade = 'D'
        for g, info in self.crowdfunding_scoring_model['grade_levels'].items():
            if total >= info['min']:
                grade = g
                break
        
        label = self.crowdfunding_scoring_model['grade_levels'].get(grade, {}).get('label', '未评级')
        
        return total, grade, label, scores_dict

    def _generate_crowdfunding_scoring(self, data: Dict) -> str:
        """生成募资可行性评分章节"""
        total, grade, label, scores_dict = self._calc_crowdfunding_score(data)
        product = data.get('product', {})
        
        # 募资成功概率判断
        if total >= 75:
            verdict = '大概率可以'
        elif total >= 60:
            verdict = '有可能可以'
        elif total >= 45:
            verdict = '较难'
        else:
            verdict = '很难'
        
        # 评分说明映射
        comment_map = {
            '产品展示力': {85: '有原型/样品/视频等展示素材，展示力强',
                         70: '硬件类产品，实物展示有天然优势',
                         60: '有概念/设计图，需进一步开发原型',
                         50: '信息不足，建议补充产品展示素材',
                         40: '产品展示力薄弱，亟需加强'},
            '信任证据': {80: '团队经验丰富/有专利/有合作背书',
                         75: '有相关经验和资源',
                         50: '信任证据信息不足，建议补充团队背景',
                         40: '初创团队，信任积累有限'},
            '定价合理性': {70: '成本与目标金额比例合理',
                         60: '定价基本合理，可进一步优化档位',
                         50: '定价信息不足，建议详细核算',
                         40: '目标金额与成本不匹配，需调整'},
            '推广准备度': {80: '有社群/KOL/粉丝资源，推广基础好',
                         60: '有推广意识，需具体执行计划',
                         50: '推广资源信息不足，建议提前布局'},
            '履约能力': {80: '有供应链/生产计划，履约能力较强',
                         65: '有制造意识，需补充供应链细节',
                         50: '履约信息不足，硬件类需重点补充'},
            '平台匹配度': {80: '有明确平台选择，匹配度高',
                         70: '产品品类适合主流募资平台',
                         60: '平台信息不明确，需进一步选择'},
        }
        
        def get_comment(name, score):
            options = comment_map.get(name, {})
            best = min(options.keys(), key=lambda x: abs(x - score))
            return options.get(best, '待评估')
        
        # 构建评分表
        score_table_rows = []
        for dim in self.crowdfunding_scoring_model['dimensions']:
            name = dim['name']
            weight = dim['weight']
            s = scores_dict.get(name, 50)
            weighted = s * weight // 100
            comment = get_comment(name, s)
            score_table_rows.append("| " + name + " | " + str(s) + "/100 | " + str(weight) + "% | " + str(weighted) + " | " + comment + " |")
        
        # 募资成功关键因素
        advantages = []
        warnings_list = []
        risks = []
        for dim in self.crowdfunding_scoring_model['dimensions']:
            name = dim['name']
            s = scores_dict.get(name, 50)
            if s >= 70:
                advantages.append((name, s))
            elif s >= 55:
                warnings_list.append((name, s))
            else:
                risks.append((name, s))
        
        factors = []
        for name, s in advantages:
            factors.append("- ✅ " + name + "评分" + str(s) + "分，表现良好")
        for name, s in warnings_list:
            factors.append("- ⚠️ " + name + "评分" + str(s) + "分，需补强")
        for name, s in risks:
            factors.append("- ❌ " + name + "评分" + str(s) + "分，存在明显短板")
        
        # 上线前必须完成的事项
        must_do = []
        for name, s in risks:
            must_do.append("补强【" + name + "】，当前评分偏低，是募资成功的关键障碍")
        for name, s in warnings_list:
            must_do.append("提升【" + name + "】，建议达到70分以上再上线")
        must_do.append("制作高质量募资视频和产品渲染图，展示核心优势")
        must_do.append("准备至少500名潜在支持者的预热列表")
        
        must_do_lines = []
        for i, item in enumerate(must_do[:5], 1):
            must_do_lines.append(str(i) + ". " + item)
        
        # Build output using list join
        lines = []
        lines.append("# 2. 募资可行性评分")
        lines.append("")
        lines.append("### 总分: " + str(total) + "/100 -- 评级: " + grade)
        lines.append("")
        lines.append("> 一句话结论：这个项目在募资平台上" + verdict + "成功。")
        lines.append("")
        lines.append("### 评分明细")
        lines.append("| 维度 | 得分 | 权重 | 加权分 | 说明 |")
        lines.append("|------|------|------|--------|------|")
        lines.extend(score_table_rows)
        lines.append("")
        lines.append("### 募资成功关键因素")
        lines.extend(factors)
        lines.append("")
        lines.append("### 上线前必须完成的事项")
        lines.extend(must_do_lines)
        
        return '\n'.join(lines)

    def _generate_crowdfunding_platform_analysis(self, data: Dict) -> str:
        """生成平台选择与匹配分析"""
        product = data.get('product', {})
        category = data.get('category', 'hardware')
        product_name = product.get('name', '未命名产品')
        crowdfunding = data.get('crowdfunding', {})
        
        platform_map = {
            'hardware': [('Kickstarter', 5, '全球最大，适合硬件/创新产品出海', '5%+3%', '$10万-$100万'),
                         ('嚶嚶', 4, '台湾最大众筹平台，适合中文市场', '5%+3%', '¥500万-¥1500万'),
                         ('Indiegogo', 3, '灵活审核，适合有争议或创新产品', '5%+5%', '$5万-$50万'),
                         ('FlyingV', 3, '台湾本土，适合文创/设计类', '8%+3%', '¥200万-¥800万'),
                         ('摩点', 3, '中国大陆，适合ACG/文创', '5%+3%', '¥100万-¥500万')],
            'saas': [('Kickstarter', 5, '全球最大，适合软件工具类', '5%+3%', '$5万-$50万'),
                     ('摩点', 3, '中国大陆，适合软件工具', '5%+3%', '¥100万-¥500万'),
                     ('嚶嚶', 3, '台湾最大众筹平台', '5%+3%', '¥500万-¥1500万'),
                     ('Indiegogo', 3, '灵活审核，适合创新软件', '5%+5%', '$5万-$50万'),
                     ('FlyingV', 2, '台湾本土，适合文创类', '8%+3%', '¥200万-¥800万')],
            'content': [('Patreon', 5, '最适合内容创作者持续募资', '5%-12%', '$1千-$10万'),
                        ('嚶嚶', 4, '台湾最大，适合内容项目', '5%+3%', '¥500万-¥1500万'),
                        ('Kickstarter', 4, '全球最大，适合内容出海', '5%+3%', '$5万-$50万'),
                        ('FlyingV', 3, '台湾本土，适合文创/播客', '8%+3%', '¥200万-¥800万'),
                        ('摩点', 4, '中国大陆，适合ACG/内容', '5%+3%', '¥100万-¥500万')],
            'service': [('嚶嚶', 5, '台湾最大，适合服务类项目', '5%+3%', '¥500万-¥1500万'),
                        ('FlyingV', 4, '台湾本土，适合服务/设计', '8%+3%', '¥200万-¥800万'),
                        ('Kickstarter', 3, '全球最大，适合创新服务', '5%+3%', '$5万-$50万'),
                        ('Indiegogo', 3, '灵活审核', '5%+5%', '$5万-$50万'),
                        ('摩点', 2, '中国大陆', '5%+3%', '¥100万-¥500万')],
            'community': [('嚶嚶', 5, '台湾最大，适合社群类项目', '5%+3%', '¥500万-¥1500万'),
                          ('Patreon', 5, '最适合社群持续运营', '5%-12%', '$1千-$10万'),
                          ('Kickstarter', 3, '全球最大', '5%+3%', '$5万-$50万'),
                          ('FlyingV', 3, '台湾本土', '8%+3%', '¥200万-¥800万'),
                          ('Indiegogo', 2, '灵活审核', '5%+5%', '$5万-$50万')],
            'platform': [('Kickstarter', 5, '全球最大，适合平台类项目', '5%+3%', '$10万-$100万'),
                         ('Indiegogo', 4, '灵活审核，适合创新平台', '5%+5%', '$5万-$50万'),
                         ('嚶嚶', 3, '台湾最大', '5%+3%', '¥500万-¥1500万'),
                         ('FlyingV', 2, '台湾本土', '8%+3%', '¥200万-¥800万'),
                         ('摩点', 2, '中国大陆', '5%+3%', '¥100万-¥500万')],
            'b2b': [('Indiegogo', 5, '灵活审核，适合B2B创新产品', '5%+5%', '$5万-$50万'),
                    ('Kickstarter', 4, '全球最大，适合B2B硬件/工具', '5%+3%', '$10万-$100万'),
                    ('嚶嚶', 3, '台湾最大', '5%+3%', '¥500万-¥1500万'),
                    ('FlyingV', 2, '台湾本土', '8%+3%', '¥200万-¥800万'),
                    ('摩点', 2, '中国大陆', '5%+3%', '¥100万-¥500万')],
        }
        
        platforms = platform_map.get(category, platform_map['hardware'])
        recommended = crowdfunding.get('recommended', platforms[0][0])
        
        lines = []
        lines.append("# 3. 平台选择与匹配分析")
        lines.append("")
        lines.append("## 3.1 平台推荐")
        lines.append("根据 " + product_name + " 的品类（" + category + "）和目标市场，推荐平台：")
        lines.append("")
        lines.append("| 平台 | 推荐指数 | 适用理由 | 平台费率 | 平均募集 |")
        lines.append("|---|---|---|---|---|")
        for p in platforms:
            stars = '★' * p[1] + '☆' * (5 - p[1])
            lines.append("| " + p[0] + " | " + stars + " | " + p[2] + " | " + p[3] + " | " + p[4] + " |")
        lines.append("")
        lines.append("**推荐平台：" + recommended + "**")
        lines.append("")
        lines.append("## 3.2 平台审核通过率预估")
        lines.append("| 平台 | 预估通过率 | 主要审核点 |")
        lines.append("| --- | --- | --- |")
        lines.append("| " + recommended + " | 70-85% | 产品创新性、团队能力、项目完整性 |")
        
        return '\n'.join(lines)

    def _generate_crowdfunding_pricing(self, data: Dict) -> str:
        """生成募资定价策略"""
        product = data.get('product', {})
        cost_raw = product.get('cost', 300)
        
        try:
            cost = float(str(cost_raw).replace(',', '').replace('¥', '').replace('NT$', '').replace('$', ''))
        except (ValueError, TypeError):
            cost = 300
        
        early_bird = int(cost * 1.3)
        standard = int(cost * 1.7)
        premium = int(cost * 2.5)
        
        lines = []
        lines.append("# 5. 募资定价策略")
        lines.append("")
        lines.append("## 5.1 三档定价方案")
        lines.append("基于成本 ¥" + str(int(cost)) + "，建议三档定价：")
        lines.append("")
        lines.append("| 档位 | 价格 | 数量限制 | 内容 | 预期转化 |")
        lines.append("|---|---|---|---|---|")
        lines.append("| 早鸟档 | ¥" + str(early_bird) + " | 前100名 | 标准版+感谢信 | 40% |")
        lines.append("| 标准档 | ¥" + str(standard) + " | 500名 | 标准版+配件 | 45% |")
        lines.append("| 豪华档 | ¥" + str(premium) + " | 50名 | 全套+定制+优先发货 | 15% |")
        lines.append("")
        lines.append("## 5.2 定价策略说明")
        lines.append("- **早鸟档**：以接近成本的价格吸引首批支持者，快速达成首日目标")
        lines.append("- **标准档**：主力销售档位，兼顾利润和转化率")
        lines.append("- **豪华档**：高净值用户贡献额外收入，提供差异化价值")
        lines.append("")
        lines.append("## 5.3 定价合理性评估")
        lines.append("- 早鸟价毛利率：" + str(round((early_bird - cost) / early_bird * 100)) + "%")
        lines.append("- 标准价毛利率：" + str(round((standard - cost) / standard * 100)) + "%")
        lines.append("- 豪华价毛利率：" + str(round((premium - cost) / premium * 100)) + "%")
        
        return '\n'.join(lines)

    def _generate_crowdfunding_promotion(self, data: Dict) -> str:
        """生成推广策略与时间线"""
        lines = []
        lines.append("# 6. 推广策略与时间线")
        lines.append("")
        lines.append("## 6.1 四阶段推广计划")
        lines.append("| 阶段 | 时间 | 核心动作 | 目标 |")
        lines.append("|---|---|---|---|")
        lines.append("| 预热期 | 上线前30天 | 社群运营、邮件列表、KOL种草 | 积結500+潜在backer |")
        lines.append("| 首日冲刺 | Day 1 | 紧迫感营销、亲友支持、社群转发 | 达标30% |")
        lines.append("| 持续期 | Day 2-25 | 每日更新、回复留言、KOL评测 | 达标75% |")
        lines.append("| 收尾冲刺 | Day 26-30 | 追加福利、限时加价、社交分享 | 达标100%+ |")
        lines.append("")
        lines.append("## 6.2 预热期关键动作")
        lines.append("1. 建立项目社交媒体账号（Facebook/Instagram/微博）")
        lines.append("2. 制作并发布产品预告视频（30秒-1分钟）")
        lines.append("3. 联系3-5个相关领域KOL进行种草")
        lines.append("4. 建立邮件列表，每周发送项目进展")
        lines.append("5. 加入相关社群，自然融入并建立信任")
        lines.append("")
        lines.append("## 6.3 首日冲刺策略")
        lines.append("- 准备亲友支持名单，确保首小时20+支持")
        lines.append("- 设置早鸟档限时限量的紧迫感")
        lines.append("- 同步在所有社交媒体发布上线消息")
        lines.append("- 实时回复评论区，保持热度")
        
        return '\n'.join(lines)

    def _generate_crowdfunding_checklist(self, data: Dict) -> str:
        """生成平台审核准备清单"""
        lines = []
        lines.append("# 7. 平台审核准备清单")
        lines.append("")
        lines.append("## 7.1 必备材料")
        lines.append("- [ ] 产品名称和一句话介绍（50字内）")
        lines.append("- [ ] 项目故事/团队介绍（800字以上）")
        lines.append("- [ ] 产品原型/Demo/渲染图（至少5张）")
        lines.append("- [ ] 募资视频（1-3分钟）")
        lines.append("- [ ] 回报档位设计（至少3档）")
        lines.append("- [ ] 风险说明和退换政策")
        lines.append("- [ ] 团队背景和执行能力证明")
        lines.append("- [ ] 供应链/生产计划（硬件类必填）")
        lines.append("- [ ] 预计交付时间和物流方案")
        lines.append("")
        lines.append("## 7.2 加分材料")
        lines.append("- [ ] 用户调研/访谈记录")
        lines.append("- [ ] 专利或技术认证文件")
        lines.append("- [ ] 媒体报道或行业背书")
        lines.append("- [ ] 合作伙伴意向书")
        lines.append("")
        lines.append("## 7.3 审核常见驳回原因")
        lines.append("1. 项目描述过于模糊，无法理解产品价值")
        lines.append("2. 缺少实物原型或演示视频")
        lines.append("3. 回报档位设计不合理")
        lines.append("4. 团队背景与项目不匹配")
        lines.append("5. 交付计划不切实际")
        
        return '\n'.join(lines)

    def _generate_appendix(self, data: Dict) -> str:
        """生成附录（退出策略、时间规划、通用评分等辅助内容）"""
        parts = []
        
        # 附录A：产品通用可行性评分
        scoring = data.get('scoring', {})
        score = scoring.get('total_score', 0)
        grade = 'D'
        for g, info in self.scoring_model['grade_levels'].items():
            if score >= info['min']:
                grade = g
                break
        grade_info = self.scoring_model['grade_levels'].get(grade, {})
        
        scoring_lines = []
        scoring_lines.append("## 附录A：产品通用可行性评分")
        scoring_lines.append("")
        scoring_lines.append("| 维度 | 得分 | 权重 | 加权分 | 说明 |")
        scoring_lines.append("| --- | --- | --- | --- | --- |")
        scoring_lines.append(self._format_scoring_table(scoring))
        scoring_lines.append("")
        scoring_lines.append("- **总分**：" + str(score) + "/100")
        scoring_lines.append("- **评级**：" + grade + " - " + grade_info.get('label', '未评级'))
        scoring_lines.append("- **结论**：" + grade_info.get('action', '待评估'))
        parts.append('\n'.join(scoring_lines))
        
        # 附录B：时间规划
        timeline_lines = []
        timeline_lines.append("## 附录B：时间规划")
        timeline_lines.append("")
        timeline_lines.append("| 阶段 | 时间 | 目标 | 关键任务 | 成功标准 |")
        timeline_lines.append("| --- | --- | --- | --- | --- |")
        timeline_lines.append(self._format_timeline_stages())
        timeline_lines.append("")
        timeline_lines.append("- **关键路径**：用户调研 -> MVP开发 -> 内测 -> 公测 -> 规模化")
        timeline_lines.append("- **人力配置**：" + data.get('team_size', '3-5人核心团队'))
        timeline_lines.append("- **预算分配**：" + data.get('budget', '研发40%、生产30%、营销20%、运营10%'))
        parts.append('\n'.join(timeline_lines))
        
        # 附录C：退出策略
        exit_lines = []
        exit_lines.append("## 附录C：退出策略与止损机制")
        exit_lines.append("")
        exit_lines.append("| 选项 | 可行性 | 时机 | 预期回报 | 风险 |")
        exit_lines.append("| --- | --- | --- | --- | --- |")
        exit_lines.append(self._format_exit_options())
        exit_lines.append("")
        exit_lines.append("| 类型 | 指标 | 阈值 | 触发动作 |")
        exit_lines.append("| --- | --- | --- | --- |")
        exit_lines.append(self._format_stop_loss_conditions())
        parts.append('\n'.join(exit_lines))
        
        return "# 16. 附录\n\n" + "\n\n".join(parts)

    # ============ End crowdfunding methods ============

    # 辅助格式化方法
    def _format_list(self, items: List, prefix: str) -> str:
        if not items:
            return f"**{prefix}**：待补充"
        return '\n'.join([f"- {item}" for item in items[:5]])
    
    def _assess_pain_level(self, product: Dict) -> str:
        desc = product.get('description', '')
        if any(w in desc for w in ['刚需', '高频', '痛点', '解决']):
            return '高'
        return '中'
    
    def _format_reference_projects(self, cases: List) -> str:
        if not cases:
            return "| 待补充 | - | - | - | - |\n"
        lines = []
        for case in cases[:5]:
            lines.append(f"| {case.get('name', '')} | {case.get('category', '')} | {case.get('amount_raised', '')} | {case.get('backers', '')} | {case.get('success_rate', '')} |")
        return '\n'.join(lines)
    
    def _format_category_checks(self, category: str) -> str:
        checks = self.category_checks.get(category, [])
        if not checks:
            return "无特别检查项"
        return '\n'.join([f"- {check}" for check in checks])
    
    def _format_swot_items(self, items: List) -> str:
        if not items:
            return "| 待补充 | - | - | - |\n"
        lines = []
        for item in items[:5]:
            if isinstance(item, dict):
                lines.append(f"| {item.get('item', '')} | {item.get('impact', '中')} | {item.get('evidence', '中')} | {item.get('suggestion', '')} |")
            else:
                lines.append(f"| {item} | 中 | 中 | 需验证 |")
        return '\n'.join(lines)
    
    def _format_competitors(self, competitors: List) -> str:
        if not competitors:
            return "| 待补充 | - | - | - | - |\n"
        lines = []
        for comp in competitors[:5]:
            lines.append(f"| {comp.get('name', '')} | {comp.get('category', '')} | {comp.get('features', '')} | {comp.get('price', '')} | {comp.get('relation', '')} |")
        return '\n'.join(lines)
    
    def _format_success_cases(self, cases: List) -> str:
        if not cases:
            return "| 待补充 | - | - | - | - |\n"
        lines = []
        for case in cases[:5]:
            factors = ', '.join(case.get('success_factors', [])[:2]) if case.get('success_factors') else ''
            lines.append(f"| {case.get('name', '')} | {case.get('platform', '')} | {case.get('amount_raised', '')} | {case.get('backers', '')} | {factors} |")
        return '\n'.join(lines)
    
    def _extract_success_factors(self, cases: List) -> str:
        if not cases:
            return "- 待补充"
        all_factors = []
        for case in cases:
            all_factors.extend(case.get('success_factors', []))
        unique_factors = list(set(all_factors))[:5]
        return '\n'.join([f"- {f}" for f in unique_factors]) if unique_factors else "- 待补充"
    
    def _extract_failure_warnings(self, cases: List) -> str:
        return "- 痛点模糊、产品过于复杂、价格过高、团队缺乏经验、履约风险"
    
    def _get_market_size_reason(self, som: str) -> str:
        if not som:
            return "待估算"
        return f"基于SOM估算{som}"
    
    def _format_growth_stages(self) -> str:
        lines = []
        for stage in self.growth_flywheel['growth_stages']:
            metrics = ', '.join(stage['metrics'])
            lines.append(f"| {stage['stage']} | {stage['users']} | {stage['goal']} | {stage['strategy']} | {metrics} |")
        return '\n'.join(lines)
    
    def _format_aarrr_metrics(self) -> str:
        lines = []
        for stage, info in self.metrics_framework['aarrr'].items():
            metrics = ', '.join(info['metrics'])
            lines.append(f"| {stage} | {metrics} | 待测 | {info['target']} |")
        return '\n'.join(lines)
    
    def _format_category_metrics(self, category: str) -> str:
        if category == 'hardware':
            return "- 复购率、用户满意度、售后响应时间"
        return "- 待补充品类特定指标"
    
    def _format_tech_dimensions(self) -> str:
        lines = []
        for dim in self.tech_framework['dimensions']:
            lines.append(f"| {dim['name']} | 待评估 | 中 | 需详细评估 |")
        return '\n'.join(lines)
    
    def _format_scoring_table(self, scoring: Dict) -> str:
        scores = scoring.get('scores', {})
        if not scores:
            return "| 待补充 | - | - | - | - |\n"
        lines = []
        for dim, info in scores.items():
            lines.append(f"| {dim} | {info.get('score', 0)} | {info.get('weight', 0)} | {round(info.get('score', 0) * info.get('weight', 0) / 100, 2)} | {info.get('comment', '')} |")
        return '\n'.join(lines)
    
    def _format_timeline_stages(self) -> str:
        lines = []
        for stage in self.timeline_framework['stages']:
            tasks = ', '.join(stage['tasks'][:3])
            lines.append(f"| {stage['stage']} | {stage['time']} | {stage['goal']} | {tasks} | {stage['success']} |")
        return '\n'.join(lines)
    
    def _format_exit_options(self) -> str:
        lines = []
        for opt in self.exit_strategy['options']:
            lines.append(f"| {opt['option']} | 待评估 | {opt['timing']} | {opt['return']} | {opt['risk']} |")
        return '\n'.join(lines)
    
    def _format_stop_loss_conditions(self) -> str:
        lines = []
        for cond in self.exit_strategy['stop_loss']:
            lines.append(f"| {cond['type']} | {cond['indicator']} | {cond['threshold']} | {cond['action']} |")
        return '\n'.join(lines)


class FullHTMLReportGenerator:
    """完整HTML报告生成器，包含所有15个章节，深色主题+玻璃拟态风格"""

    def __init__(self):
        self.scoring_model = self._load_scoring_model()
        self.growth_flywheel = self._load_growth_flywheel()
        self.metrics_framework = self._load_metrics_framework()
        self.tech_framework = self._load_tech_framework()
        self.timeline_framework = self._load_timeline_framework()
        self.exit_strategy = self._load_exit_strategy()
        self.market_data = self._load_market_data()
        self.category_checks = self._load_category_checks()
        self.crowdfunding_scoring_model = {
            'dimensions': [
                {'name': '产品展示力', 'weight': 20, 'key': 'product_showcase'},
                {'name': '信任证据', 'weight': 20, 'key': 'trust_evidence'},
                {'name': '定价合理性', 'weight': 15, 'key': 'pricing_rationality'},
                {'name': '推广准备度', 'weight': 15, 'key': 'promotion_readiness'},
                {'name': '履约能力', 'weight': 15, 'key': 'fulfillment'},
                {'name': '平台匹配度', 'weight': 15, 'key': 'platform_match'},
            ],
            'grade_levels': {
                'A+': {'min': 85, 'label': '极大可能成功', 'action': '立即上线'},
                'A': {'min': 75, 'label': '大概率成功', 'action': '准备好后上线'},
                'B': {'min': 60, 'label': '有可能成功', 'action': '需要补强后上线'},
                'C': {'min': 45, 'label': '较难成功', 'action': '需要大幅调整'},
                'D': {'min': 0, 'label': '很难成功', 'action': '不建议上线'},
            }
        }

    def _load_scoring_model(self) -> Dict:
        return {
            'dimensions': [
                {'name': '痛点强度', 'weight': 15, 'key': 'pain_point'},
                {'name': '目标用户清晰度', 'weight': 10, 'key': 'user_clarity'},
                {'name': '竞争壁垒', 'weight': 10, 'key': 'moat'},
                {'name': '产品可演示性', 'weight': 10, 'key': 'demo_ability'},
                {'name': '技术/生产可行性', 'weight': 10, 'key': 'tech_feasibility'},
                {'name': '合规与信任', 'weight': 10, 'key': 'compliance'},
                {'name': '商业模式', 'weight': 10, 'key': 'business_model'},
                {'name': '市场推广可行性', 'weight': 10, 'key': 'marketing'},
                {'name': '团队匹配度', 'weight': 10, 'key': 'team_fit'},
                {'name': '证据完整度', 'weight': 5, 'key': 'evidence'},
            ],
            'grade_levels': {
                'A': {'min': 80, 'label': '强烈推荐', 'action': '可以进入正式开发/预热/募资阶段'},
                'B': {'min': 65, 'label': '建议补强后继续', 'action': '方向可行，但必须先补强2-3个关键短板'},
                'C': {'min': 50, 'label': '需要重新定位', 'action': '需要重新定义用户、场景或卖点'},
                'D': {'min': 0, 'label': '暂不建议投入', 'action': '暂不建议投入大量资源'},
            }
        }

    def _load_growth_flywheel(self) -> Dict:
        return {
            'category_flywheels': {
                'hardware': {
                    'name': '硬件增长飞轮',
                    'cycle': '产品销售 -> 口碑传播 -> 用户增长 -> 规模效应 -> 成本降低 -> 价格优势 -> 更多销售',
                    'key_elements': ['产品质量', '口碑传播', '规模效应'],
                    'bottlenecks': ['首批用户获取', '供应链成本', '售后体系'],
                },
                'saas': {
                    'name': 'SaaS增长飞轮',
                    'cycle': '用户使用 -> 数据积累 -> 产品智能提升 -> 用户粘性增强 -> 用户推荐 -> 更多用户 -> 更多数据',
                    'key_elements': ['数据驱动优化', '用户粘性', '推荐机制'],
                    'bottlenecks': ['免费到付费转化', '用户留存', '竞品切换成本'],
                },
                'service': {
                    'name': '服务增长飞轮',
                    'cycle': '客户服务 -> 满意度提升 -> 口碑传播 -> 新客户获取 -> 规模扩大 -> 服务能力增强 -> 更好服务',
                    'key_elements': ['服务质量', '口碑传播', '规模扩张'],
                    'bottlenecks': ['服务标准化', '人才复制', '客户获取成本'],
                },
                'content': {
                    'name': '内容社群增长飞轮',
                    'cycle': '内容/互动 -> 用户参与 -> 社区活跃 -> 更多内容 -> 更多用户 -> 更强社区',
                    'key_elements': ['优质内容', '社区活跃', '用户参与'],
                    'bottlenecks': ['内容生产门槛', '冷启动密度', 'UGC治理'],
                },
                'b2b': {
                    'name': 'B2B增长飞轮',
                    'cycle': '客户成功 -> 续约与增购 -> 口碑与案例 -> 新客户获取 -> 产品优化 -> 更好的客户成功',
                    'key_elements': ['客户成功', '案例积累', '续约增购'],
                    'bottlenecks': ['决策周期长', 'POC转化率', '集成难度'],
                },
                'platform': {
                    'name': '平台增长飞轮',
                    'cycle': '供应方增长 -> 交易体验提升 -> 需求方增长 -> 更多供应 -> 更好体验 -> 更多需求',
                    'key_elements': ['供需平衡', '交易体验', '网络效应'],
                    'bottlenecks': ['冷启动鸡生蛋', '信任机制', '防作弊'],
                },
            },
            'growth_stages': [
                {'stage': '冷启动', 'users': '0-1000', 'goal': '验证产品价值', 'strategy': '种子用户测试、用户访谈', 'metrics': ['激活率', '留存率', 'NPS']},
                {'stage': '增长期', 'users': '1000-10000', 'goal': '扩大用户规模', 'strategy': '付费广告、内容营销、SEO', 'metrics': ['用户增长', 'CAC']},
                {'stage': '规模化', 'users': '10000+', 'goal': '建立竞争壁垒', 'strategy': '网络效应、品牌建设、专利', 'metrics': ['市场份额', '品牌认知']},
            ],
        }

    def _load_metrics_framework(self) -> Dict:
        return {
            'north_star': {
                'hardware': {'metric': '活跃用户数 x 客单价 x 复购率', 'description': '衡量产品被使用和产生收入的能力'},
                'saas': {'metric': 'MRR（月经常性收入）', 'description': '衡量订阅业务的健康度'},
                'service': {'metric': 'LTV（客户生命周期价值）', 'description': '衡量服务的长期价值'},
                'content': {'metric': 'DAU（日活跃用户数）', 'description': '衡量社区的活跃度和粘性'},
                'b2b': {'metric': 'ACV（年度合同价值）', 'description': '衡量企业客户的价值'},
                'platform': {'metric': 'GMV（商品交易总额）', 'description': '衡量平台的交易规模'},
            },
            'aarrr': {
                'acquisition': {'metrics': ['CAC', '渠道ROI'], 'target': 'LTV/CAC >= 3'},
                'activation': {'metrics': ['首单转化率', '核心功能使用率'], 'target': '-'},
                'retention': {'metrics': ['D1/D7/D30留存率'], 'target': 'D1>=30%, D7>=15%, D30>=5%'},
                'revenue': {'metrics': ['ARPU', '付费转化率', 'LTV'], 'target': '-'},
                'referral': {'metrics': ['NPS', '推荐转化率', '病毒系数'], 'target': '病毒系数 >= 1'},
            },
        }

    def _load_tech_framework(self) -> Dict:
        return {
            'dimensions': [
                {'name': '技术栈成熟度', 'high': '技术成熟稳定', 'low': '技术风险高'},
                {'name': '技术复杂度', 'high': '简单可实现', 'low': '极复杂'},
                {'name': '供应链可靠性', 'high': '供应稳定', 'low': '供应风险高'},
                {'name': '安全合规', 'high': '完全合规', 'low': '严重合规问题'},
                {'name': '扩展性', 'high': '扩展性强', 'low': '扩展性差'},
            ],
            'risk_levels': {
                'high': ['核心技术未验证', '供应链单一', '合规问题'],
                'medium': ['技术复杂度高', '依赖第三方服务'],
                'low': ['技术选型保守', '有替代方案'],
            },
        }

    def _load_timeline_framework(self) -> Dict:
        return {
            'stages': [
                {'stage': '验证期', 'time': '0-3个月', 'goal': '验证核心假设', 'tasks': ['用户调研', '竞品分析', 'MVP定义', '原型测试'], 'success': '种子用户验证通过'},
                {'stage': '开发期', 'time': '3-6个月', 'goal': '开发MVP', 'tasks': ['技术架构搭建', '核心功能开发', '测试修复'], 'success': 'MVP完成内部验收'},
                {'stage': '内测期', 'time': '6-9个月', 'goal': '小范围测试', 'tasks': ['内测用户招募', '反馈收集', '迭代优化'], 'success': '内测用户满意度达标'},
                {'stage': '公测期', 'time': '9-12个月', 'goal': '公开测试', 'tasks': ['公测用户扩展', '付费转化测试', '市场推广'], 'success': '商业模式验证通过'},
                {'stage': '规模化期', 'time': '12个月+', 'goal': '快速增长', 'tasks': ['用户规模扩大', '收入模式优化', '团队扩充'], 'success': '建立竞争壁垒'},
            ],
        }

    def _load_exit_strategy(self) -> Dict:
        return {
            'options': [
                {'option': '被收购', 'condition': '有收购意向方', 'timing': '产品有一定规模和用户', 'return': '中等-高', 'risk': '估值不确定'},
                {'option': 'IPO', 'condition': '达到上市标准', 'timing': '公司成熟，财务健康', 'return': '高', 'risk': '周期长，门槛高'},
                {'option': '股权转让', 'condition': '找到接盘方', 'timing': '创始人想退出', 'return': '中等', 'risk': '流动性差'},
                {'option': '停业清算', 'condition': '无法继续运营', 'timing': '资金耗尽，无融资可能', 'return': '低', 'risk': '损失投资'},
            ],
            'stop_loss': [
                {'type': '财务止损', 'indicator': '现金储备', 'threshold': '低于3个月运营成本', 'action': '启动紧急融资或缩减成本'},
                {'type': '财务止损', 'indicator': '收入增长', 'threshold': '连续3个月低于目标50%', 'action': '重新评估商业模式'},
                {'type': '用户止损', 'indicator': 'D7留存率', 'threshold': '低于15%', 'action': '重新评估产品价值'},
                {'type': '用户止损', 'indicator': '付费转化率', 'threshold': '低于1%', 'action': '重新设计定价和价值主张'},
                {'type': '运营止损', 'indicator': '团队流失率', 'threshold': '季度超过30%', 'action': '审查企业文化和薪酬'},
            ],
        }

    def _load_market_data(self) -> Dict:
        return {
            'ai_hardware': {
                'global_market_2026': '$800亿',
                'china_market_2026': '¥2,000亿',
                'growth_rate': '35%',
                'kickstarter_avg': '$50万-$100万',
                'zeczec_avg': '¥500万-¥1,500万',
            },
            'tam_som_guide': [
                {'level': 10, 'tam': '>¥100亿', 'sam': '>¥10亿', 'som': '>¥1亿'},
                {'level': 8, 'tam': '¥50-100亿', 'sam': '¥5-10亿', 'som': '¥5,000万-1亿'},
                {'level': 6, 'tam': '¥10-50亿', 'sam': '¥1-5亿', 'som': '¥1,000万-5,000万'},
                {'level': 4, 'tam': '¥1-10亿', 'sam': '¥1,000万-1亿', 'som': '¥100万-1,000万'},
                {'level': 2, 'tam': '<¥1亿', 'sam': '<¥1,000万', 'som': '<¥100万'},
            ],
        }

    def _load_category_checks(self) -> Dict:
        return {
            'hardware': [
                '供应链韧性：关键元器件是否受制于单一供应商？',
                'BOM成本与定价的毛利空间是否合理？',
                '模具/开模周期和首批量产时间表是否现实？',
                '物流、关税、退货处理是否有预案？',
            ],
            'saas': [
                '用户是否有持续使用理由，还是一次性体验？',
                '竞品的切换成本有多高？',
                'API/基础设施依赖风险（如OpenAI、AWS政策变化）？',
                '免费tier到付费的转化路径是否清晰？',
            ],
            'service': [
                '服务是否可标准化，还是只能靠人堆？',
                '单个客户的交付成本与收入是否可持续？',
                '规模化瓶颈在哪里？',
                '客户获取是否依赖个人关系？',
            ],
            'content': [
                '伦理边界：是否涉及情感操控、防沉迷、未成年人保护？',
                '持续使用动机：用户为什么每天都回来？',
                '内容治理：UGC内容审核和风险如何管理？',
                '是否容易引发舆论风险或监管关注？',
            ],
            'b2b': [
                '企业决策链长度和周期是否在可控范围？',
                'POC到付费的转化率预期？',
                '合规认证（ISO、SOC2、信创等）是否必要？',
                '集成难度和客户IT支持能力是否匹配？',
            ],
            'platform': [
                '先发哪一侧？冷启动的"鸡生蛋"问题如何解决？',
                '网络效应拐点在哪里？需要多少用户才能自运转？',
                '平台抽佣和定价机制是否合理？',
                '防止作弊和信任机制如何设计？',
            ],
        }

    def _get_grade(self, score: int) -> str:
        for g, info in self.scoring_model['grade_levels'].items():
            if score >= info['min']:
                return g
        return 'D'

    def _grade_label(self, grade: str) -> str:
        return self.scoring_model['grade_levels'].get(grade, {}).get('label', '未评级')

    def _grade_action(self, grade: str) -> str:
        return self.scoring_model['grade_levels'].get(grade, {}).get('action', '待评估')

    def _esc(self, text: Any) -> str:
        """HTML转义"""
        if text is None:
            return ''
        s = str(text)
        return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

    def _tag(self, label: str, level: str = 'normal') -> str:
        """生成标签"""
        classes = {
            'excellent': 'tag-excellent',
            'good': 'tag-good',
            'normal': 'tag-normal',
            'poor': 'tag-poor',
            'risk': 'tag-risk',
        }
        cls = classes.get(level, 'tag-normal')
        return f'<span class="tag {cls}">{self._esc(label)}</span>'

    def _safe_get(self, data: Dict, key: str, default: str = '待补充') -> str:
        val = data.get(key)
        return str(val) if val is not None and val != '' else default

    def generate_full_html(self, analysis_data: Dict) -> str:
        """生成完整15章节HTML报告"""
        product = analysis_data.get('product', {})
        scoring = analysis_data.get('scoring', {})
        score = scoring.get('total_score', 0)
        grade = self._get_grade(score)
        category = analysis_data.get('category', 'hardware')

        nav_items = [
            ('section0', '0. 执行摘要'),
            ('section1', '1. 项目画像识别'),
            ('section2', '2. 募资可行性评分'),
            ('section3', '3. 平台选择与匹配'),
            ('section4', '4. 竞品案例与募资表现'),
            ('section5', '5. 募资定价策略'),
            ('section6', '6. 推广策略与时间线'),
            ('section7', '7. 平台审核准备清单'),
            ('section8', '8. SWOT分析'),
            ('section9', '9. 财务模型分析'),
            ('section10', '10. 市场规模估算'),
            ('section11', '11. 市场分析+PEST'),
            ('section12', '12. 商业模式+波特五力'),
            ('section13', '13. 增长飞轮+技术架构'),
            ('section14', '附录'),
            ('section15', '14. 募资行动建议'),
            ('section16', '15. 沟通话术'),
        ]

        nav_items_html = ''.join([
            '<div onclick="scrollToSection(\'' + nid + '\')" class="nav-item w-full text-left px-4 py-3 rounded-lg text-sm font-medium text-gray-400' + (' active' if i == 0 else '') + '">' + label + '</div>'
            for i, (nid, label) in enumerate(nav_items)
        ])
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self._esc(product.get('name', '未命名产品'))} - 募资可行性分析报告</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Noto Sans SC', sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            min-height: 100vh;
            color: #e4e4e7;
        }}
        .glass-card {{
            background: rgba(30, 30, 46, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
        }}
        .gradient-text {{
            background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .nav-item {{
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        .nav-item:hover {{
            background: rgba(96, 165, 250, 0.15);
            transform: translateX(4px);
        }}
        .nav-item.active {{
            background: rgba(96, 165, 250, 0.2);
            border-left: 3px solid #60a5fa;
        }}
        .section-header {{
            position: relative;
        }}
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
        .table-cell {{
            background: rgba(255, 255, 255, 0.03);
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }}
        .tag {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
            display: inline-block;
        }}
        .tag-excellent {{ background: rgba(34, 197, 94, 0.2); color: #4ade80; }}
        .tag-good {{ background: rgba(96, 165, 250, 0.2); color: #93c5fd; }}
        .tag-normal {{ background: rgba(251, 191, 36, 0.2); color: #fcd34d; }}
        .tag-poor {{ background: rgba(249, 115, 22, 0.2); color: #fdba74; }}
        .tag-risk {{ background: rgba(239, 68, 68, 0.2); color: #fca5a5; }}
        .canvas-section {{ position: relative; height: 280px; width: 100%; }}
        .canvas-section-small {{ position: relative; height: 200px; width: 100%; }}
        .scrollbar-hide::-webkit-scrollbar {{ display: none; }}
        .scrollbar-hide {{ -ms-overflow-style: none; scrollbar-width: none; }}
        .link-card {{
            transition: all 0.3s ease;
            cursor: pointer;
            text-decoration: none;
            color: inherit;
            display: block;
        }}
        .link-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 40px rgba(96, 165, 250, 0.2);
        }}
        .business-model-box {{
            background: rgba(96, 165, 250, 0.08);
            border: 1px solid rgba(96, 165, 250, 0.2);
            border-radius: 12px;
            padding: 16px;
        }}
        .pest-item {{
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 16px;
            border-left: 4px solid;
        }}
        .pest-political {{ border-color: #ef4444; }}
        .pest-economic {{ border-color: #3b82f6; }}
        .pest-social {{ border-color: #10b981; }}
        .pest-technological {{ border-color: #8b5cf6; }}
        .five-forces-item {{
            position: relative;
            padding: 12px 16px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 8px;
            margin-bottom: 8px;
        }}
        .force-bar {{
            height: 4px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 2px;
            margin-top: 8px;
            overflow: hidden;
        }}
        .force-fill {{
            height: 100%;
            border-radius: 2px;
            transition: width 1s ease;
        }}
        .swot-cell {{
            padding: 16px;
            border-radius: 12px;
        }}
        .swot-strength {{ background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.2); }}
        .swot-weakness {{ background: rgba(249, 115, 22, 0.1); border: 1px solid rgba(249, 115, 22, 0.2); }}
        .swot-opportunity {{ background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2); }}
        .swot-threat {{ background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); }}
        .priority-high {{ border-left: 4px solid #ef4444; }}
        .priority-medium {{ border-left: 4px solid #f59e0b; }}
        .priority-low {{ border-left: 4px solid #10b981; }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .fade-in {{ animation: fadeIn 0.5s ease forwards; }}
        @media (max-width: 1024px) {{
            .sidebar {{ display: none; }}
            .main-content {{ margin-left: 0 !important; }}
        }}
    </style>
</head>
<body class="flex">
    <!-- 左侧导航栏 -->
    <aside class="sidebar w-72 fixed left-0 top-0 h-screen bg-[#16162a]/90 backdrop-blur-xl border-r border-white/5 flex flex-col z-50">
        <div class="p-6 border-b border-white/5">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <path d="M12 6v6l4 2"></path>
                    </svg>
                </div>
                <div>
                    <h1 class="text-lg font-semibold text-white">募资可行性分析</h1>
                    <p class="text-xs text-gray-400">Crowdfunding Feasibility</p>
                </div>
            </div>
        </div>

        <div class="p-4 mx-4 mt-4 glass-card">
            <div class="flex items-center justify-center relative">
                <svg width="100" height="100" viewBox="0 0 100 100">
                    <defs>
                        <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#60a5fa" />
                            <stop offset="100%" stop-color="#a78bfa" />
                        </linearGradient>
                    </defs>
                    <circle cx="50" cy="50" r="45" fill="none" stroke-width="8" stroke="rgba(255,255,255,0.1)" />
                    <circle cx="50" cy="50" r="45" fill="none" stroke-width="8" stroke="url(#scoreGradient)"
                            stroke-linecap="round" stroke-dasharray="283" stroke-dashoffset="{283 * (1 - score/100):.0f}" />
                </svg>
                <div class="absolute inset-0 flex flex-col items-center justify-center">
                    <span class="text-3xl font-bold gradient-text">{score}</span>
                    <span class="text-xs text-gray-400">总分/100</span>
                </div>
            </div>
            <div class="text-center mt-3">
                <span class="tag tag-{'good' if score >= 65 else 'normal' if score >= 50 else 'poor'}">{self._grade_label(grade)}</span>
                <p class="text-xs text-gray-400 mt-1">{self._grade_action(grade)}</p>
            </div>
        </div>

        <nav class="flex-1 overflow-y-auto p-4 scrollbar-hide">
            <div class="space-y-1">
                {nav_items_html}
            </div>
        </nav>

        <div class="p-4 border-t border-white/5">
            <p class="text-xs text-gray-500 text-center">
                生成时间：{datetime.now().strftime('%Y年%m月%d日')}<br>
                版本：v3.0.0
            </p>
        </div>
    </aside>

    <main class="main-content ml-72 min-h-screen p-8 flex-1">
        <div class="max-w-5xl mx-auto space-y-8">
            {self._section_executive_summary(analysis_data)}
            {self._section_project_profile(analysis_data)}
            {self._section_crowdfunding_scoring(analysis_data)}
            {self._section_crowdfunding_platform(analysis_data)}
            {self._section_competitors(analysis_data)}
            {self._section_crowdfunding_pricing(analysis_data)}
            {self._section_crowdfunding_promotion(analysis_data)}
            {self._section_crowdfunding_checklist(analysis_data)}
            {self._section_swot(analysis_data)}
            {self._section_financial(analysis_data)}
            {self._section_market_sizing(analysis_data)}
            {self._section_market_analysis(analysis_data)}
            {self._section_pest(analysis_data)}
            {self._section_porter_forces(analysis_data)}
            {self._section_business_model(analysis_data)}
            {self._section_growth_flywheel(analysis_data)}
            {self._section_tech(analysis_data)}
            {self._section_scoring(analysis_data)}
            {self._section_appendix(analysis_data)}
            {self._section_action_plan(analysis_data)}
            {self._section_communication(analysis_data)}
        </div>
    </main>

    <script>
        function scrollToSection(id) {{
            const element = document.getElementById(id);
            if (element) {{
                element.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}
            document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
            event.target.classList.add('active');
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            const sections = document.querySelectorAll('main > div > div[id^="section"]');
            window.addEventListener('scroll', () => {{
                let current = '';
                sections.forEach(section => {{
                    const sectionTop = section.offsetTop - 200;
                    const sectionHeight = section.offsetHeight;
                    if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {{
                        current = section.getAttribute('id');
                    }}
                }});
                document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
                document.querySelectorAll('.nav-item').forEach(button => {{
                    const onclick = button.getAttribute('onclick');
                    if (onclick && onclick.includes(current)) {{
                        button.classList.add('active');
                    }}
                }});
            }});

            {self._chart_js_code(analysis_data)}
        }});
    </script>
</body>
</html>'''
        return html

    # ===================== 各章节生成方法 =====================

    def _section_executive_summary(self, data: Dict) -> str:
        product = data.get('product', {})
        scoring = data.get('scoring', {})
        score = scoring.get('total_score', 0)
        grade = self._get_grade(score)
        strengths = scoring.get('strengths', ['待补充'])
        weaknesses = scoring.get('weaknesses', ['待补充'])

        return f'''<div id="section0" class="glass-card p-8 fade-in">
    <h2 class="section-header text-2xl font-bold text-white mb-6">执行摘要</h2>
    <div class="grid grid-cols-2 gap-6">
        <div>
            <h3 class="text-lg font-semibold text-gray-200 mb-3">项目概述</h3>
            <p class="text-gray-400 leading-relaxed">{self._esc(product.get('description', '暂无描述'))}</p>
            <div class="mt-4 flex flex-wrap gap-2">
                <span class="tag tag-good">{self._esc(data.get('category', '未识别'))}</span>
                <span class="tag tag-normal">{self._esc(product.get('platform', '募资平台'))}</span>
            </div>
        </div>
        <div>
            <h3 class="text-lg font-semibold text-gray-200 mb-3">核心结论</h3>
            <ul class="space-y-2 text-gray-400">
                <li class="flex items-center gap-2">
                    <svg class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                    可行性评分 <strong>{score}/100</strong>，评级：{self._grade_label(grade)}
                </li>
                <li class="flex items-center gap-2">
                    <svg class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                    {self._grade_action(grade)}
                </li>
                <li class="flex items-center gap-2">
                    <svg class="w-4 h-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                    主要风险：{self._esc(weaknesses[0] if weaknesses else '待补充')}
                </li>
            </ul>
        </div>
    </div>
    <div class="grid grid-cols-4 gap-4 mt-8">
        <div class="bg-white/5 rounded-xl p-4 text-center">
            <div class="text-2xl font-bold gradient-text">{score}/100</div>
            <div class="text-xs text-gray-400 mt-1">综合评分</div>
        </div>
        <div class="bg-white/5 rounded-xl p-4 text-center">
            <div class="text-2xl font-bold text-blue-400">{self._esc(data.get('tam', '待估算'))}</div>
            <div class="text-xs text-gray-400 mt-1">TAM总市场</div>
        </div>
        <div class="bg-white/5 rounded-xl p-4 text-center">
            <div class="text-2xl font-bold text-green-400">{self._esc(data.get('margin_expectation', '待估算'))}</div>
            <div class="text-xs text-gray-400 mt-1">毛利率预期</div>
        </div>
        <div class="bg-white/5 rounded-xl p-4 text-center">
            <div class="text-2xl font-bold text-purple-400">{self._esc(data.get('payback_period', '待估算'))}</div>
            <div class="text-xs text-gray-400 mt-1">回收期预期</div>
        </div>
    </div>
</div>'''


    def _section_crowdfunding_scoring(self, data: Dict) -> str:
        """募资可行性评分 HTML"""
        product = data.get('product', {})
        description = str(product.get('description', '') + ' ' + product.get('value_proposition', '') + ' ' + str(product.get('features', []))).lower()
        text_lower = description

        def calc_scores():
            scores = {}
            if any(k in text_lower for k in ['demo', '原型', '视频', '渲染图', '样品', '样机', 'prototype', '实物']):
                scores['产品展示力'] = 85
            elif any(k in text_lower for k in ['概念', '设计图', '概念图', '设计稿']):
                scores['产品展示力'] = 60
            elif any(k in text_lower for k in ['硬件', '设备', '实体', '耳机', '机器人', '音箱', '手表']):
                scores['产品展示力'] = 70
            else:
                scores['产品展示力'] = 50

            if any(k in text_lower for k in ['团队经验', '过往项目', '专利', '合作', '行业资深', '专家', '连续创业']):
                scores['信任证据'] = 80
            elif any(k in text_lower for k in ['初创', '学生', '新团队']):
                scores['信任证据'] = 40
            elif any(k in text_lower for k in ['有经验', '有资源', '有背景']):
                scores['信任证据'] = 75
            else:
                scores['信任证据'] = 50

            s = 60
            cost_raw = product.get('cost')
            target_raw = product.get('target_amount')
            try:
                cost_val = float(str(cost_raw).replace(',', '').replace('¥', '').replace('$', ''))
                target_val = float(str(target_raw).replace(',', '').replace('¥', '').replace('$', ''))
                if cost_val > 0 and target_val > 0:
                    ratio = target_val / cost_val
                    if 100 <= ratio <= 10000: s = 70
                    elif ratio < 100: s = 40
                    elif ratio > 10000: s = 45
            except: pass
            scores['定价合理性'] = s

            if any(k in text_lower for k in ['社群', '粉丝', '邮件列表', 'kol', '网红', '自媒体', '频道']):
                scores['推广准备度'] = 80
            elif any(k in text_lower for k in ['社交媒体', '推广', '营销']):
                scores['推广准备度'] = 60
            else:
                scores['推广准备度'] = 50

            if any(k in text_lower for k in ['供应链', '工厂', '生产计划', '交期', '量产', '代工']):
                scores['履约能力'] = 80
            elif any(k in text_lower for k in ['制造', '组装', '生产']):
                scores['履约能力'] = 65
            else:
                scores['履约能力'] = 50

            platform = product.get('platform', '')
            if platform and platform not in ('', None):
                scores['平台匹配度'] = 80
            elif any(k in text_lower for k in ['硬件', '智能', '设备', '创新', '科技']):
                scores['平台匹配度'] = 70
            else:
                scores['平台匹配度'] = 60
            return scores

        scores = calc_scores()
        total = 0
        for dim in self.crowdfunding_scoring_model['dimensions']:
            name = dim['name']
            weight = dim['weight']
            s = scores.get(name, 50)
            total += s * weight // 100

        cf_grade = 'D'
        for g, info in self.crowdfunding_scoring_model['grade_levels'].items():
            if total >= info['min']:
                cf_grade = g
                break

        if total >= 75: verdict = '大概率可以'
        elif total >= 60: verdict = '有可能可以'
        elif total >= 45: verdict = '较难'
        else: verdict = '很难'

        grade_color = 'green' if total >= 75 else 'blue' if total >= 60 else 'yellow' if total >= 45 else 'red'

        dim_rows = ''
        for dim in self.crowdfunding_scoring_model['dimensions']:
            name = dim['name']
            weight = dim['weight']
            s = scores.get(name, 50)
            weighted = s * weight // 100
            level = 'good' if s >= 70 else 'normal' if s >= 55 else 'poor'
            bar_color = '#4ade80' if s >= 70 else '#fcd34d' if s >= 55 else '#f87171'
            dim_rows += '<tr><td class="table-cell py-3 text-gray-200">' + self._esc(name) + '</td><td class="table-cell py-3"><span class="tag tag-' + level + '">' + str(s) + '/100</span></td><td class="table-cell py-3">' + str(weight) + '%</td><td class="table-cell py-3">' + str(weighted) + '</td><td class="table-cell py-3 w-40"><div class="force-bar"><div class="force-fill" style="width: ' + str(s) + '%; background: ' + bar_color + '"></div></div></td></tr>'

        advantages = [(n, s) for n, s in scores.items() if s >= 70]
        warnings_list = [(n, s) for n, s in scores.items() if 55 <= s < 70]
        risks = [(n, s) for n, s in scores.items() if s < 55]

        factors_html = ''
        for n, s in advantages:
            factors_html += '<div class="flex items-center gap-2 text-green-300"><span class="tag tag-excellent">' + str(s) + '分</span><span class="text-sm">' + self._esc(n) + '</span></div>'
        for n, s in warnings_list:
            factors_html += '<div class="flex items-center gap-2 text-yellow-300"><span class="tag tag-normal">' + str(s) + '分</span><span class="text-sm">' + self._esc(n) + '</span></div>'
        for n, s in risks:
            factors_html += '<div class="flex items-center gap-2 text-red-300"><span class="tag tag-poor">' + str(s) + '分</span><span class="text-sm">' + self._esc(n) + '</span></div>'

        html = '<div id="section2" class="glass-card p-8 fade-in">'
        html += '<h2 class="section-header text-2xl font-bold text-white mb-6">二、募资可行性评分</h2>'
        html += '<div class="flex items-center gap-6 mb-8">'
        html += '<div class="flex items-center justify-center relative">'
        html += '<svg width="120" height="120" viewBox="0 0 120 120"><defs><linearGradient id="cfScoreGradient" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#60a5fa"/><stop offset="100%" stop-color="#a78bfa"/></linearGradient></defs>'
        html += '<circle cx="60" cy="60" r="52" fill="none" stroke-width="8" stroke="rgba(255,255,255,0.1)"/>'
        html += '<circle cx="60" cy="60" r="52" fill="none" stroke-width="8" stroke="url(#cfScoreGradient)" stroke-linecap="round" stroke-dasharray="327" stroke-dashoffset="' + str(327 - int(327 * total / 100)) + '"/>'
        html += '</svg>'
        html += '<div class="absolute inset-0 flex flex-col items-center justify-center"><span class="text-4xl font-bold gradient-text">' + str(total) + '</span><span class="text-xs text-gray-400">募资评分</span></div>'
        html += '</div>'
        html += '<div><div class="text-lg font-semibold text-white mb-2">评级：' + self._esc(cf_grade) + '</div>'
        html += '<div class="bg-green-500/10 rounded-lg px-4 py-2 border border-green-500/20"><p class="text-green-300 text-sm">这个项目在募资平台上<strong>' + self._esc(verdict) + '</strong>成功募资。</p></div></div>'
        html += '</div>'
        html += '<div class="overflow-x-auto mb-6"><table class="w-full"><thead><tr class="text-left text-sm text-gray-400"><th class="pb-3 font-medium">维度</th><th class="pb-3 font-medium">得分</th><th class="pb-3 font-medium">权重</th><th class="pb-3 font-medium">加权分</th><th class="pb-3 font-medium">评分</th></tr></thead><tbody>'
        html += dim_rows
        html += '<tr class="border-t border-white/20"><td class="table-cell py-3 font-medium text-white">总分</td><td class="table-cell py-3"></td><td class="table-cell py-3 font-medium">100%</td><td class="table-cell py-3 font-bold text-white">' + str(total) + '</td><td class="table-cell py-3"></td></tr>'
        html += '</tbody></table></div>'
        html += '<div class="grid grid-cols-2 gap-4">'
        html += '<div class="bg-white/5 rounded-xl p-4"><h4 class="font-medium text-white mb-3">募资成功关键因素</h4><div class="space-y-2">' + factors_html + '</div></div>'
        html += '<div class="bg-white/5 rounded-xl p-4"><h4 class="font-medium text-white mb-3">评级标准</h4><div class="space-y-2 text-sm text-gray-400">'
        html += '<div class="flex justify-between"><span>A+</span><span>85-100 极大可能成功</span></div>'
        html += '<div class="flex justify-between"><span>A</span><span>75-84 大概率成功</span></div>'
        html += '<div class="flex justify-between"><span>B</span><span>60-74 有可能成功</span></div>'
        html += '<div class="flex justify-between"><span>C</span><span>45-59 较难成功</span></div>'
        html += '<div class="flex justify-between"><span>D</span><span>0-44 很难成功</span></div>'
        html += '</div></div></div></div>'
        return html

    def _section_crowdfunding_platform(self, data: Dict) -> str:
        """平台选择与匹配 HTML - reuse crowdfunding section"""
        result = self._section_crowdfunding(data)
        result = result.replace('id="section12b"', 'id="section3"')
        result = result.replace('募资平台专项分析', '三、平台选择与匹配分析')
        return result

    def _section_crowdfunding_pricing(self, data: Dict) -> str:
        """募资定价策略 HTML"""
        product = data.get('product', {})
        cost_raw = product.get('cost', 300)
        try:
            cost = float(str(cost_raw).replace(',', '').replace('¥', '').replace('NT$', '').replace('$', ''))
        except (ValueError, TypeError):
            cost = 300
        early_bird = int(cost * 1.3)
        standard = int(cost * 1.7)
        premium = int(cost * 2.5)

        html = '<div id="section5" class="glass-card p-8 fade-in">'
        html += '<h2 class="section-header text-2xl font-bold text-white mb-6">五、募资定价策略</h2>'
        html += '<div class="overflow-x-auto"><table class="w-full"><thead><tr class="text-left text-sm text-gray-400">'
        html += '<th class="pb-3 font-medium">档位</th><th class="pb-3 font-medium">价格</th><th class="pb-3 font-medium">数量限制</th><th class="pb-3 font-medium">内容</th><th class="pb-3 font-medium">预期转化</th>'
        html += '</tr></thead><tbody>'
        html += '<tr class="border-b border-white/5"><td class="table-cell py-3 text-green-400 font-medium">早鸟档</td><td class="table-cell py-3 text-white font-semibold">¥' + str(early_bird) + '</td><td class="table-cell py-3 text-gray-300">前100名</td><td class="table-cell py-3 text-gray-300">标准版+感谢信</td><td class="table-cell py-3 text-gray-300">40%</td></tr>'
        html += '<tr class="border-b border-white/5"><td class="table-cell py-3 text-blue-400 font-medium">标准档</td><td class="table-cell py-3 text-white font-semibold">¥' + str(standard) + '</td><td class="table-cell py-3 text-gray-300">500名</td><td class="table-cell py-3 text-gray-300">标准版+配件</td><td class="table-cell py-3 text-gray-300">45%</td></tr>'
        html += '<tr><td class="table-cell py-3 text-purple-400 font-medium">豪华档</td><td class="table-cell py-3 text-white font-semibold">¥' + str(premium) + '</td><td class="table-cell py-3 text-gray-300">50名</td><td class="table-cell py-3 text-gray-300">全套+定制+优先发货</td><td class="table-cell py-3 text-gray-300">15%</td></tr>'
        html += '</tbody></table></div>'
        html += '<div class="grid grid-cols-3 gap-4 mt-6">'
        html += '<div class="bg-white/5 rounded-xl p-4 text-center"><div class="text-2xl font-bold text-green-400">' + str(round((early_bird - cost) / early_bird * 100)) + '%</div><div class="text-xs text-gray-400 mt-1">早鸟档毛利率</div></div>'
        html += '<div class="bg-white/5 rounded-xl p-4 text-center"><div class="text-2xl font-bold text-blue-400">' + str(round((standard - cost) / standard * 100)) + '%</div><div class="text-xs text-gray-400 mt-1">标准档毛利率</div></div>'
        html += '<div class="bg-white/5 rounded-xl p-4 text-center"><div class="text-2xl font-bold text-purple-400">' + str(round((premium - cost) / premium * 100)) + '%</div><div class="text-xs text-gray-400 mt-1">豪华档毛利率</div></div>'
        html += '</div></div>'
        return html

    def _section_crowdfunding_promotion(self, data: Dict) -> str:
        """推广策略与时间线 HTML"""
        html = '<div id="section6" class="glass-card p-8 fade-in">'
        html += '<h2 class="section-header text-2xl font-bold text-white mb-6">六、推广策略与时间线</h2>'
        html += '<div class="grid grid-cols-1 md:grid-cols-2 gap-4">'
        stages = [
            ('预热期', '上线前30天', '社群运营、邮件列表、KOL种草', '积累500+潜在backer', 'from-blue-500/20 to-blue-600/10', 'border-blue-500/30', '#3b82f6'),
            ('首日冲刺', 'Day 1', '紧迫感营销、亲友支持、社群转发', '达标30%', 'from-green-500/20 to-green-600/10', 'border-green-500/30', '#10b981'),
            ('持续期', 'Day 2-25', '每日更新、回复留言、KOL评测', '达标75%', 'from-yellow-500/20 to-yellow-600/10', 'border-yellow-500/30', '#f59e0b'),
            ('收尾冲刺', 'Day 26-30', '追加福利、限时加价、社交分享', '达标100%+', 'from-red-500/20 to-red-600/10', 'border-red-500/30', '#ef4444'),
        ]
        for stage_name, stage_time, stage_action, stage_goal, bg_class, border_class, color in stages:
            html += '<div class="bg-gradient-to-r ' + bg_class + ' rounded-xl p-4 border ' + border_class + '">'
            html += '<div class="flex items-center gap-2 mb-2"><div class="w-2 h-2 rounded-full" style="background: ' + color + '"></div>'
            html += '<span class="font-semibold text-white">' + self._esc(stage_name) + '</span>'
            html += '<span class="text-xs text-gray-400 ml-auto">' + self._esc(stage_time) + '</span></div>'
            html += '<div class="text-sm text-gray-300">核心动作：' + self._esc(stage_action) + '</div>'
            html += '<div class="text-sm text-gray-400 mt-1">目标：' + self._esc(stage_goal) + '</div></div>'
        html += '</div></div>'
        return html

    def _section_crowdfunding_checklist(self, data: Dict) -> str:
        """平台审核准备清单 HTML"""
        items = ['产品名称和一句话介绍（50字内）', '项目故事/团队介绍（800字以上）', '产品原型/Demo/渲染图（至少5张）', '募资视频（1-3分钟）', '回报档位设计（至少3档）', '风险说明和退换政策', '团队背景和执行能力证明', '供应链/生产计划（硬件类必填）', '预计交付时间和物流方案']
        html = '<div id="section7" class="glass-card p-8 fade-in">'
        html += '<h2 class="section-header text-2xl font-bold text-white mb-6">七、平台审核准备清单</h2>'
        for item in items:
            html += '<div class="flex items-center gap-3 py-2 border-b border-white/5 last:border-0"><div class="w-5 h-5 rounded border border-gray-500 flex items-center justify-center flex-shrink-0"></div><span class="text-sm text-gray-300">' + self._esc(item) + '</span></div>'
        html += '</div>'
        return html

    def _section_appendix(self, data: Dict) -> str:
        """附录 HTML"""
        scoring = data.get('scoring', {})
        score = scoring.get('total_score', 0)
        html = '<div id="section14" class="glass-card p-8 fade-in">'
        html += '<h2 class="section-header text-2xl font-bold text-white mb-6">附录</h2>'
        html += '<div class="glass-card rounded-xl p-6 mb-6" style="background: rgba(30, 30, 46, 0.5);">'
        html += '<h3 class="text-lg font-semibold text-white mb-4">附录A：产品通用可行性评分</h3>'
        html += '<div class="flex items-center gap-4 mb-4"><span class="text-3xl font-bold gradient-text">' + str(score) + '/100</span><span class="text-gray-400">（10维度加权评分，仅供参考）</span></div>'
        html += '</div>'
        html += '<div class="glass-card rounded-xl p-6 mb-6" style="background: rgba(30, 30, 46, 0.5);">'
        html += '<h3 class="text-lg font-semibold text-white mb-4">附录B：时间规划</h3>'
        html += '<p class="text-sm text-gray-400">验证期(0-3月) -> 开发期(3-6月) -> 内测期(6-9月) -> 公测期(9-12月) -> 规模化期(12月+)</p></div>'
        html += '<div class="glass-card rounded-xl p-6" style="background: rgba(30, 30, 46, 0.5);">'
        html += '<h3 class="text-lg font-semibold text-white mb-4">附录C：退出策略与止损机制</h3>'
        html += '<p class="text-sm text-gray-400">退出选项：被收购 / IPO / 股权转让 / 停业清算</p>'
        html += '<p class="text-sm text-gray-400 mt-2">止损线：现金储备&lt;3月运营成本、D7留存&lt;15%、付费转化&lt;1%</p></div></div>'
        return html

    def _section_project_profile(self, data: Dict) -> str:
        product = data.get('product', {})
        category = data.get('category', 'default')
        similar_cases = data.get('similar_cases', [])
        checks = self.category_checks.get(category, [])

        cases_html = ''
        if similar_cases:
            for case in similar_cases[:5]:
                cases_html += f'''<tr>
                    <td class="table-cell py-3">{self._esc(case.get('name', '-'))}</td>
                    <td class="table-cell py-3">{self._esc(case.get('category', '-'))}</td>
                    <td class="table-cell py-3">{self._esc(case.get('amount_raised', '-'))}</td>
                    <td class="table-cell py-3">{self._esc(case.get('backers', '-'))}</td>
                    <td class="table-cell py-3">{self._esc(case.get('success_rate', '-'))}</td>
                </tr>'''
        else:
            cases_html = '<tr><td class="table-cell py-3" colspan="5">暂无参照项目</td></tr>'

        checks_html = ''
        if checks:
            for check in checks:
                checks_html += f'<li class="text-sm text-gray-400">• {self._esc(check)}</li>'
        else:
            checks_html = '<li class="text-sm text-gray-400">无特别检查项</li>'

        return f'''<div id="section1" class="glass-card p-8 fade-in">
    <h2 class="section-header text-2xl font-bold text-white mb-6">一、项目画像识别</h2>
    <div class="grid grid-cols-3 gap-6">
        <div class="col-span-2">
            <h3 class="text-lg font-semibold text-gray-200 mb-3">产品定位</h3>
            <p class="text-gray-400 leading-relaxed">{self._esc(product.get('value_proposition', '待补充'))}</p>
            <div class="mt-4 flex flex-wrap gap-2">
                <span class="tag tag-good">{self._esc(category)}</span>
                <span class="tag tag-normal">{self._esc(product.get('target_users', '待补充'))}</span>
            </div>
        </div>
        <div>
            <h3 class="text-lg font-semibold text-gray-200 mb-3">核心信息</h3>
            <div class="space-y-2 text-sm">
                <div class="flex justify-between"><span class="text-gray-500">产品名称</span><span class="text-white">{self._esc(product.get('name', '-'))}</span></div>
                <div class="flex justify-between"><span class="text-gray-500">目标用户</span><span class="text-white">{self._esc(product.get('target_users', '-'))}</span></div>
                <div class="flex justify-between"><span class="text-gray-500">平台</span><span class="text-white">{self._esc(product.get('platform', '-'))}</span></div>
                <div class="flex justify-between"><span class="text-gray-500">目标金额</span><span class="text-white">{self._esc((product.get('target_amount') or '-'))}</span></div>
            </div>
        </div>
    </div>
    <div class="mt-8">
        <h3 class="text-lg font-semibold text-gray-200 mb-3">参照项目</h3>
        <div class="overflow-x-auto">
            <table class="w-full">
                <thead><tr class="text-left text-sm text-gray-400">
                    <th class="pb-3 font-medium">项目名称</th>
                    <th class="pb-3 font-medium">品类</th>
                    <th class="pb-3 font-medium">募集金额</th>
                    <th class="pb-3 font-medium">支持者</th>
                    <th class="pb-3 font-medium">达成率</th>
                </tr></thead>
                <tbody>{cases_html}</tbody>
            </table>
        </div>
    </div>
    <div class="mt-8">
        <h3 class="text-lg font-semibold text-gray-200 mb-3">品类特别检查项</h3>
        <ul class="space-y-2">{checks_html}</ul>
    </div>
</div>'''

    def _section_market_analysis(self, data: Dict) -> str:
        market_data = self.market_data.get('ai_hardware', {})
        return f'''<div id="section11" class="glass-card p-8 fade-in">
    <h2 class="section-header text-2xl font-bold text-white mb-6">十一、市场分析+PEST</h2>
    <div class="grid grid-cols-2 gap-6">
        <div class="canvas-section">
            <h3 class="text-sm text-gray-400 mb-2">AI硬件市场规模趋势</h3>
            <canvas id="marketTrendChart"></canvas>
        </div>
        <div>
            <h3 class="text-sm text-gray-400 mb-2">市场趋势分析</h3>
            <div class="space-y-3">
                <div class="bg-white/5 rounded-xl p-4">
                    <div class="flex items-center gap-2 mb-1">
                        <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
                        <span class="font-medium text-white">老龄化加剧</span>
                    </div>
                    <p class="text-sm text-gray-400">中国60岁以上人口超2.8亿，空巢老人1.2亿，情感陪伴需求巨大</p>
                </div>
                <div class="bg-white/5 rounded-xl p-4">
                    <div class="flex items-center gap-2 mb-1">
                        <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
                        <span class="font-medium text-white">AI技术成熟</span>
                    </div>
                    <p class="text-sm text-gray-400">语音合成、3D建模、大语言模型技术日趋成熟，成本下降</p>
                </div>
                <div class="bg-white/5 rounded-xl p-4">
                    <div class="flex items-center gap-2 mb-1">
                        <svg class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
                        <span class="font-medium text-white">消费升级</span>
                    </div>
                    <p class="text-sm text-gray-400">家庭愿意为情感陪伴、健康关怀类产品支付溢价</p>
                </div>
            </div>
        </div>
    </div>
    <div class="mt-6 grid grid-cols-2 gap-4">
        <div class="bg-white/5 rounded-xl p-4">
            <div class="text-xs text-gray-400">全球AI硬件市场</div>
            <div class="text-xl font-bold text-blue-400">{self._esc(market_data.get('global_market_2026', '$800亿'))}</div>
        </div>
        <div class="bg-white/5 rounded-xl p-4">
            <div class="text-xs text-gray-400">年增长率</div>
            <div class="text-xl font-bold text-green-400">{self._esc(market_data.get('growth_rate', '35%'))}</div>
        </div>
    </div>
</div>'''

    def _section_pest(self, data: Dict) -> str:
        pest_data = data.get('pest', {})
        political = pest_data.get('political', ['AI产业政策支持，数据安全法规趋严'])
        economic = pest_data.get('economic', ['AI硬件市场年增长35%，消费升级趋势'])
        social = pest_data.get('social', ['AI工具教育完成，用户接受度高'])
        technological = pest_data.get('technological', ['AI技术成熟，供应链完善'])

        def pest_list(items):
            return ''.join([f'<li>• {self._esc(item)}</li>' for item in items if item])

        return f'''<div id="section11a" class="glass-card p-8 fade-in">
    <h2 class="section-header text-2xl font-bold text-white mb-6">PEST分析</h2>
    <div class="grid grid-cols-2 gap-6">
        <div class="pest-item pest-political">
            <div class="flex items-center gap-2 mb-2">
                <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 21l1.65-3.8a9 9 0 113.4 2.9L3 21"></path></svg>
                <span class="font-medium text-white">政治因素</span>
            </div>
            <ul class="text-sm text-gray-400 space-y-1">{pest_list(political)}</ul>
        </div>
        <div class="pest-item pest-economic">
            <div class="flex items-center gap-2 mb-2">
                <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span class="font-medium text-white">经济因素</span>
            </div>
            <ul class="text-sm text-gray-400 space-y-1">{pest_list(economic)}</ul>
        </div>
        <div class="pest-item pest-social">
            <div class="flex items-center gap-2 mb-2">
                <svg class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
                <span class="font-medium text-white">社会因素</span>
            </div>
            <ul class="text-sm text-gray-400 space-y-1">{pest_list(social)}</ul>
        </div>
        <div class="pest-item pest-technological">
            <div class="flex items-center gap-2 mb-2">
                <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                <span class="font-medium text-white">技术因素</span>
            </div>
            <ul class="text-sm text-gray-400 space-y-1">{pest_list(technological)}</ul>
        </div>
    </div>
</div>'''

    def _section_porter_forces(self, data: Dict) -> str:
        forces = data.get('porter_forces', [
            {'name': '现有竞争者威胁', 'level': '中高', 'width': 75, 'color': 'bg-orange-500', 'desc': 'AI硬件赛道竞争激烈，同质化严重'},
            {'name': '潜在进入者威胁', 'level': '中等', 'width': 55, 'color': 'bg-yellow-500', 'desc': '技术门槛降低，进入者增多'},
            {'name': '替代品威胁', 'level': '中低', 'width': 40, 'color': 'bg-blue-500', 'desc': '手机APP、云端服务可部分替代'},
            {'name': '供应商议价能力', 'level': '中等', 'width': 50, 'color': 'bg-yellow-500', 'desc': '芯片供应商集中，议价能力强'},
            {'name': '购买者议价能力', 'level': '中高', 'width': 70, 'color': 'bg-orange-500', 'desc': '消费者选择多，价格敏感'},
        ])
        forces_html = ''
        for f in forces:
            forces_html += f'''<div class="five-forces-item">
    <div class="flex justify-between items-center">
        <span class="font-medium text-white">{self._esc(f.get('name', ''))}</span>
        <span class="tag tag-{'poor' if f.get('width', 0) >= 70 else 'normal' if f.get('width', 0) >= 50 else 'good'}">{self._esc(f.get('level', '中'))}</span>
    </div>
    <div class="force-bar"><div class="force-fill {f.get('color', 'bg-blue-500')}" style="width: {f.get('width', 50)}%"></div></div>
    <p class="text-xs text-gray-500 mt-2">{self._esc(f.get('desc', ''))}</p>
</div>'''
        return f'''<div id="section12a" class="glass-card p-8 fade-in">
    <h2 class="section-header text-2xl font-bold text-white mb-6">波特五力分析</h2>
    <div class="space-y-4">{forces_html}</div>
    <div class="mt-6 bg-white/5 rounded-xl p-4">
        <h4 class="font-medium text-white mb-2">竞争战略建议</h4>
        <ul class="text-sm text-gray-400 space-y-1">
            <li>• 通过差异化定位避开直接价格竞争</li>
            <li>• 建立品牌信任和用户口碑形成护城河</li>
            <li>• 通过规模化降低成本，提升价格竞争力</li>
        </ul>
    </div>
</div>'''

    def _section_swot(self, data: Dict) -> str:
        swot = data.get('swot', {})
        strengths = swot.get('strengths', ['产品已成型，有实体样机', '情感陪伴痛点真实', '技术路线成熟可行'])
        weaknesses = swot.get('weaknesses', ['品牌知名度低', '定价策略待优化', '用户案例积累不足'])
        opportunities = swot.get('opportunities', ['老龄化社会带来刚需', '情感陪伴赛道竞争较少', '实体化产品适合募资展示'])
        threats = swot.get('threats', ['数据隐私合规风险', '硬件交付周期待验证', '大厂可能进入赛道'])

        def swot_list(items, icon, color):
            return ''.join([f'<li class="flex items-start gap-2"><span class="{color} mt-0.5">{icon}</span><span class="text-sm text-gray-300">{self._esc(item)}</span></li>' for item in items if item])

        return f'''<div id="section8" class="glass-card p-8 fade-in">
    <h2 class="section-header text-2xl font-bold text-white mb-6">八、SWOT分析（募资视角）</h2>
    <div class="grid grid-cols-2 gap-4">
        <div class="swot-cell swot-strength">
            <div class="flex items-center gap-2 mb-3">
                <svg class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                <span class="font-bold text-green-400">优势 (Strengths)</span>
            </div>
            <ul class="space-y-2">{swot_list(strengths, '&#10003;', 'text-green-400')}</ul>
        </div>
        <div class="swot-cell swot-weakness">
            <div class="flex items-center gap-2 mb-3">
                <svg class="w-5 h-5 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                <span class="font-bold text-orange-400">劣势 (Weaknesses)</span>
            </div>
            <ul class="space-y-2">{swot_list(weaknesses, '&#10007;', 'text-orange-400')}</ul>
        </div>
        <div class="swot-cell swot-opportunity">
            <div class="flex items-center gap-2 mb-3">
                <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                <span class="font-bold text-blue-400">机会 (Opportunities)</span>
            </div>
            <ul class="space-y-2">{swot_list(opportunities, '&#10003;', 'text-blue-400')}</ul>
        </div>
        <div class="swot-cell swot-threat">
            <div class="flex items-center gap-2 mb-3">
                <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                <span class="font-bold text-red-400">威胁 (Threats)</span>
            </div>
            <ul class="space-y-2">{swot_list(threats, '&#10007;', 'text-red-400')}</ul>
        </div>
    </div>
</div>'''

    def _section_business_model(self, data: Dict) -> str:
        product = data.get('product', {})
        fields = [
            ('关键伙伴', product.get('key_partners', '3D打印服务商、AI技术供应商、募资平台')),
            ('关键活动', product.get('key_activities', '产品研发、用户数据处理、供应链管理与营销推广')),
            ('关键资源', product.get('key_resources', 'AI技术团队、产品设计能力、供应链资源')),
            ('价值主张', product.get('value_proposition', '实体化情感陪伴、个性化声音与形象、家庭记忆传承')),
            ('客户关系', product.get('customer_relation', '一对一客服、用户社区运营、定期产品更新')),
            ('渠道通路', product.get('channels', '募资平台首发、电商平台、社交媒体、线下体验')),
            ('客户细分', product.get('target_users', '空巢老人/成年子女/礼品购买者/Z世代')),
            ('成本结构', product.get('cost_structure', '硬件/BOM成本(40%)、制造(25%)、营销(20%)、运营(15%)')),
            ('收入来源', product.get('revenue_source', '硬件产品销售、订阅服务、定制化服务费、增值服务')),
        ]
        boxes = ''.join([f'''<div class="business-model-box">
    <div class="text-blue-400 font-bold mb-2">{self._esc(label)}</div>
    <div class="text-sm text-gray-400">{self._esc(value)}</div>
</div>''' for label, value in fields])
        return f'''<div id="section12" class="glass-card p-8 fade-in">
    <h2 class="section-header text-2xl font-bold text-white mb-6">十二、商业模式画布</h2>
    <div class="grid grid-cols-3 gap-4">{boxes}</div>
</div>'''

    def _section_competitors(self, data: Dict) -> str:
        competitors = data.get('competitor_analysis', {}).get('competitors', [])
        real_cases = data.get('competitor_analysis', {}).get('real_cases', [])

        comp_rows = ''
        if competitors:
            for c in competitors[:5]:
                comp_rows += f'''<tr>
                    <td class="table-cell py-3">{self._esc(c.get('name', '-'))}</td>
                    <td class="table-cell py-3">{self._esc(c.get('category', '-'))}</td>
                    <td class="table-cell py-3">{self._esc(c.get('features', '-'))}</td>
                    <td class="table-cell py-3">{self._esc(c.get('price', '-'))}</td>
                    <td class="table-cell py-3">{self._esc(c.get('relation', '-'))}</td>
                </tr>'''
        else:
            comp_rows = '<tr><td class="table-cell py-3" colspan="5">暂无直接竞品数据</td></tr>'

        case_cards = ''
        if real_cases:
            for case in real_cases[:6]:
                url = case.get('url', '#')
                case_cards += f'''<a href="{self._esc(url)}" target="_blank" class="link-card bg-white/5 rounded-xl p-4 border border-white/10">
    <div class="flex items-center justify-between mb-2">
        <span class="font-bold text-white">{self._esc(case.get('name', '-'))}</span>
        <span class="tag tag-excellent">成功</span>
    </div>
    <div class="text-xs text-gray-400 mb-2">{self._esc(case.get('platform', '-'))} · {self._esc(case.get('date', '-'))}</div>
    <div class="text-sm text-gray-300 mb-2">{self._esc(case.get('description', '-'))}</div>
    <div class="flex justify-between text-xs">
        <span class="text-blue-400">{self._esc(case.get('amount_raised', '-'))}</span>
        <span class="text-gray-500">{self._esc(case.get('backers', '-'))}支持者</span>
    </div>
</a>'''
        else:
            case_cards = '<div class="col-span-2 text-gray-400">暂无相似成功案例</div>'

        return f'''<div id="section4" class="glass-card p-8 fade-in">
    <h2 class="section-header text-2xl font-bold text-white mb-6">四、竞品案例与募资表现</h2>
    <h3 class="text-lg font-semibold text-gray-200 mb-3">直接竞品</h3>
    <div class="overflow-x-auto">
        <table class="w-full">
            <thead><tr class="text-left text-sm text-gray-400">
                <th class="pb-3 font-medium">竞品名称</th>
                <th class="pb-3 font-medium">品类</th>
                <th class="pb-3 font-medium">核心功能</th>
                <th class="pb-3 font-medium">价格</th>
                <th class="pb-3 font-medium">与本项目关系</th>
            </tr></thead>
            <tbody>{comp_rows}</tbody>
        </table>
    </div>
    <h3 class="text-lg font-semibold text-gray-200 mt-6 mb-3">相似成功案例（点击可查看详情）</h3>
    <div class="grid grid-cols-2 gap-4">{case_cards}</div>
</div>'''

    def _section_market_sizing(self, data: Dict) -> str:
        tam = data.get('tam', '$800亿')
        sam = data.get('sam', '¥2,000亿')
        som = data.get('som', '¥50亿')
        tam_num = self._extract_number(tam) or 8000
        sam_num = self._extract_number(sam) or 2000
        som_num = self._extract_number(som) or 50
        return f'''<div id="section10" class="glass-card p-8 fade-in">
    <h2 class="section-header text-2xl font-bold text-white mb-6">十、市场规模估算（参考）</h2>
    <div class="grid grid-cols-3 gap-4 mb-6">
        <div class="bg-gradient-to-br from-blue-500/20 to-blue-600/10 rounded-xl p-6 border border-blue-500/20">
            <div class="text-xs text-gray-400 mb-1">TAM</div>
            <div class="text-2xl font-bold text-blue-400">{self._esc(tam)}</div>
            <div class="text-xs text-gray-500 mt-1">总可寻址市场</div>
        </div>
        <div class="bg-gradient-to-br from-purple-500/20 to-purple-600/10 rounded-xl p-6 border border-purple-500/20">
            <div class="text-xs text-gray-400 mb-1">SAM</div>
            <div class="text-2xl font-bold text-purple-400">{self._esc(sam)}</div>
            <div class="text-xs text-gray-500 mt-1">可服务市场</div>
        </div>
        <div class="bg-gradient-to-br from-green-500/20 to-green-600/10 rounded-xl p-6 border border-green-500/20">
            <div class="text-xs text-gray-400 mb-1">SOM</div>
            <div class="text-2xl font-bold text-green-400">{self._esc(som)}</div>
            <div class="text-xs text-gray-500 mt-1">可获得市场</div>
        </div>
    </div>
    <div class="canvas-section">
        <h3 class="text-sm text-gray-400 mb-2">TAM/SAM/SOM市场规模对比</h3>
        <canvas id="marketSizingChart"></canvas>
    </div>
    <div class="mt-6">
        <h3 class="text-lg font-semibold text-gray-200 mb-3">市场规模评分</h3>
        <div class="flex items-center gap-4">
            <span class="text-gray-400">得分：</span>
            <span class="tag tag-good">{self._safe_get(data, 'market_size_score', '-')}/10</span>
            <span class="text-gray-400">{self._safe_get(data, 'market_size_reason', '市场增长空间大')}</span>
        </div>
    </div>
    <script type="application/json" id="marketSizingData">{{"tam": {tam_num}, "sam": {sam_num}, "som": {som_num}}}</script>
</div>'''

    def _section_financial(self, data: Dict) -> str:
        financials = data.get('financial_analysis', {})
        product = data.get('product', {})
        pricing = financials.get('pricing', {})
        revenue = financials.get('revenue', {})
        margin = financials.get('margin', 50)
        backers = financials.get('backers_needed', {}).get('total_backers', 1000)
        actual = revenue.get('actual_revenue_cny', 450000)
        retail = pricing.get('retail_price', 600)
        cost = product.get('cost') or 300
        breakeven = financials.get('breakeven', {}).get('backers_needed', 723)

        cost_items = [
            ('硬件/BOM成本', cost, f'{(cost/(cost+300)*100):.0f}%'),
            ('制造成本', 50, '8%'),
            ('运输成本', 30, '5%'),
            ('营销成本', 100, '17%'),
            ('运营成本', 120, '20%'),
        ]
        cost_rows = ''.join([f'''<tr>
            <td class="table-cell py-3">{self._esc(label)}</td>
            <td class="table-cell py-3">¥{val}</td>
            <td class="table-cell py-3">{pct}</td>
            <td class="table-cell py-3 text-gray-400">-</td>
        </tr>''' for label, val, pct in cost_items])

        return f'''<div id="section9" class="glass-card p-8 fade-in">
    <h2 class="section-header text-2xl font-bold text-white mb-6">九、财务模型分析（募资视角）</h2>
    <div class="grid grid-cols-2 gap-6">
        <div>
            <h3 class="text-lg font-semibold text-gray-200 mb-3">收入预测</h3>
            <div class="space-y-3">
                <div class="flex justify-between"><span class="text-gray-400">目标募资金额</span><span class="text-white font-medium">{self._esc((product.get('target_amount') or '¥500,000'))}</span></div>
                <div class="flex justify-between"><span class="text-gray-400">预计支持者数量</span><span class="text-white font-medium">{backers}人</span></div>
                <div class="flex justify-between"><span class="text-gray-400">平均单价</span><span class="text-white font-medium">¥{retail}</span></div>
                <div class="flex justify-between"><span class="text-gray-400">平台费 + 支付手续费</span><span class="text-white font-medium">10%</span></div>
                <div class="border-t border-white/10 pt-3 flex justify-between"><span class="text-gray-300 font-medium">实际到手收入</span><span class="text-green-400 font-bold">¥{actual:,}</span></div>
            </div>
        </div>
        <div>
            <h3 class="text-lg font-semibold text-gray-200 mb-3">成本结构</h3>
            <div class="canvas-section-small"><canvas id="costStructureChart"></canvas></div>
        </div>
    </div>
    <div class="mt-6">
        <h3 class="text-lg font-semibold text-gray-200 mb-3">成本明细</h3>
        <div class="overflow-x-auto">
            <table class="w-full">
                <thead><tr class="text-left text-sm text-gray-400">
                    <th class="pb-3 font-medium">成本类型</th><th class="pb-3 font-medium">金额</th><th class="pb-3 font-medium">占比</th><th class="pb-3 font-medium">说明</th>
                </tr></thead>
                <tbody>{cost_rows}</tbody>
            </table>
        </div>
    </div>
    <div class="grid grid-cols-3 gap-4 mt-6">
        <div class="bg-white/5 rounded-xl p-4 text-center">
            <div class="text-2xl font-bold text-green-400">{margin}%</div>
            <div class="text-xs text-gray-400 mt-1">毛利率</div>
        </div>
        <div class="bg-white/5 rounded-xl p-4 text-center">
            <div class="text-2xl font-bold text-blue-400">{breakeven}件</div>
            <div class="text-xs text-gray-400 mt-1">盈亏平衡点</div>
        </div>
        <div class="bg-white/5 rounded-xl p-4 text-center">
            <div class="text-2xl font-bold text-purple-400">{self._safe_get(data, 'payback_period', '12-18个月')}</div>
            <div class="text-xs text-gray-400 mt-1">投资回收期</div>
        </div>
    </div>
    <div class="mt-6 bg-white/5 rounded-xl p-4">
        <h4 class="font-medium text-white mb-2">财务健康度评分</h4>
        <div class="flex items-center gap-4">
            <span class="text-gray-400">得分：</span>
            <span class="tag tag-good">{self._safe_get(data, 'financial_health_score', '-')}/10</span>
            <span class="text-gray-400">毛利率{margin}%，盈亏平衡可行</span>
        </div>
    </div>
</div>'''

    def _section_growth_flywheel(self, data: Dict) -> str:
        category = data.get('category', 'hardware')
        flywheel = self.growth_flywheel['category_flywheels'].get(category, self.growth_flywheel['category_flywheels']['hardware'])
        stages = self.growth_flywheel['growth_stages']
        stages_html = ''
        colors = ['blue', 'purple', 'green']
        for i, s in enumerate(stages):
            c = colors[i % len(colors)]
            stages_html += f'''<div class="bg-white/5 rounded-xl p-4">
    <div class="text-{c}-400 font-bold mb-2">{self._esc(s['stage'])}</div>
    <div class="text-xs text-gray-400 mb-2">{self._esc(s['users'])}用户</div>
    <div class="text-sm text-gray-300">{self._esc(s['goal'])}</div>
    <div class="text-xs text-gray-500 mt-2">策略：{self._esc(s['strategy'])}</div>
</div>'''
        bottlenecks_html = ''.join([f'<li class="text-sm text-gray-400">• {self._esc(b)}</li>' for b in flywheel['bottlenecks']])
        return f'''<div id="section13a" class="glass-card p-8 fade-in">
    <h2 class="section-header text-2xl font-bold text-white mb-6">十三、增长飞轮+技术架构</h2>
    <div class="relative bg-gradient-to-br from-blue-500/10 to-purple-500/10 rounded-2xl p-8 border border-blue-500/20 mb-6">
        <h3 class="text-lg font-semibold text-white mb-6 text-center">{self._esc(flywheel['name'])}</h3>
        <div class="flex justify-center">
            <div class="relative w-80 h-80">
                <svg class="w-full h-full" viewBox="0 0 200 200">
                    <defs>
                        <linearGradient id="flywheelGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#60a5fa" stop-opacity="0.3" />
                            <stop offset="100%" stop-color="#a78bfa" stop-opacity="0.3" />
                        </linearGradient>
                    </defs>
                    <circle cx="100" cy="100" r="80" fill="url(#flywheelGradient)" stroke="rgba(96,165,250,0.5)" stroke-width="2" />
                    <circle cx="100" cy="100" r="60" fill="none" stroke="rgba(96,165,250,0.3)" stroke-width="1" />
                    <circle cx="100" cy="100" r="40" fill="none" stroke="rgba(96,165,250,0.3)" stroke-width="1" />
                    <circle cx="100" cy="100" r="5" fill="#60a5fa" />
                    <path d="M100 20 L100 40 M100 160 L100 180 M20 100 L40 100 M160 100 L180 100" stroke="rgba(96,165,250,0.5)" stroke-width="2" />
                </svg>
                <div class="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-full">
                    <div class="bg-white/10 rounded-xl px-4 py-2 text-center"><div class="text-sm font-medium text-gray-200">口碑传播</div></div>
                </div>
                <div class="absolute bottom-0 left-1/2 -translate-x-1/2 translate-y-full">
                    <div class="bg-white/10 rounded-xl px-4 py-2 text-center"><div class="text-sm font-medium text-gray-200">用户增长</div></div>
                </div>
                <div class="absolute top-1/2 right-0 -translate-y-1/2 translate-x-full">
                    <div class="bg-white/10 rounded-xl px-4 py-2 text-center"><div class="text-sm font-medium text-gray-200">数据积累</div></div>
                </div>
                <div class="absolute top-1/2 left-0 -translate-y-1/2 -translate-x-full">
                    <div class="bg-white/10 rounded-xl px-4 py-2 text-center"><div class="text-sm font-medium text-gray-200">模型优化</div></div>
                </div>
                <div class="absolute inset-0 flex items-center justify-center">
                    <div class="text-center"><div class="text-xl font-bold text-blue-400">产品销售</div><div class="text-xs text-gray-400 mt-1">核心驱动</div></div>
                </div>
            </div>
        </div>
    </div>
    <h3 class="text-lg font-semibold text-gray-200 mb-3">增长阶段规划</h3>
    <div class="grid grid-cols-3 gap-4">{stages_html}</div>
    <div class="mt-6">
        <h3 class="text-lg font-semibold text-gray-200 mb-3">增长瓶颈</h3>
        <ul class="space-y-2">{bottlenecks_html}</ul>
    </div>
</div>'''

    def _section_tech(self, data: Dict) -> str:
        category = data.get('category', 'hardware')
        tech_dims = self.tech_framework['dimensions']
        dim_html = ''
        tag_map = {'high': 'poor', 'medium': 'normal', 'low': 'good'}
        for dim in tech_dims:
            level = data.get('tech_levels', {}).get(dim['name'], 'medium')
            dim_html += f'''<div class="flex justify-between items-center py-2 border-b border-white/5">
    <span class="text-gray-400">{self._esc(dim['name'])}</span>
    <span class="tag tag-{tag_map.get(level, 'normal')}">{self._esc({'high':'高','medium':'中','low':'低'}.get(level, '中'))}</span>
</div>'''
        risks = self.tech_framework['risk_levels']
        risk_html = ''
        for r in risks['high']:
            risk_html += f'''<div class="flex items-center gap-2 text-red-300">
    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
    <span class="text-sm">{self._esc(r)}</span>
</div>'''
        for r in risks['medium']:
            risk_html += f'''<div class="flex items-center gap-2 text-orange-300">
    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
    <span class="text-sm">{self._esc(r)}</span>
</div>'''
        return f'''<div id="section13b" class="glass-card p-8 fade-in">
    <h2 class="section-header text-2xl font-bold text-white mb-6">技术架构评估</h2>
    <div class="grid grid-cols-2 gap-6">
        <div>
            <h3 class="text-lg font-semibold text-gray-200 mb-3">技术可行性</h3>
            <div class="space-y-1">{dim_html}</div>
        </div>
        <div>
            <h3 class="text-lg font-semibold text-gray-200 mb-3">技术风险清单</h3>
            <div class="space-y-2">{risk_html}</div>
        </div>
    </div>
    <div class="mt-6 bg-white/5 rounded-xl p-4">
        <h4 class="font-medium text-white mb-2">MVP技术方案</h4>
        <ul class="text-sm text-gray-400 space-y-1">
            <li>• 核心功能范围：{self._esc(data.get('mvp_features', '语音交互、情感识别、个性化定制'))}</li>
            <li>• 技术架构：{self._esc(data.get('tech_stack', 'AI模型 + 硬件模块 + 云端服务'))}</li>
            <li>• 开发周期：{self._esc(data.get('dev_cycle', '3-6个月'))}</li>
        </ul>
    </div>
</div>'''

    def _section_scoring(self, data: Dict) -> str:
        scoring = data.get('scoring', {})
        score = scoring.get('total_score', 0)
        grade = self._get_grade(score)
        scores = scoring.get('scores', {})
        if not scores:
            scores = {d['name']: {'score': 0, 'weight': d['weight'], 'comment': '待评估'} for d in self.scoring_model['dimensions']}

        rows = ''
        radar_labels = []
        radar_data = []
        for dim_info in self.scoring_model['dimensions']:
            name = dim_info['name']
            info = scores.get(name, {'score': 0, 'weight': dim_info['weight'], 'comment': '待评估'})
            s = info.get('score', 0)
            w = info.get('weight', dim_info['weight'])
            weighted = round(s * w / 100, 2)
            level = 'good' if s >= 70 else 'normal' if s >= 50 else 'poor'
            rows += f'''<tr>
                <td class="table-cell py-3">{self._esc(name)}</td>
                <td class="table-cell py-3"><span class="tag tag-{level}">{s}/{w}</span></td>
                <td class="table-cell py-3">{w}</td>
                <td class="table-cell py-3">{weighted}</td>
                <td class="table-cell py-3 text-gray-400">{self._esc(info.get('comment', ''))}</td>
            </tr>'''
            radar_labels.append(name)
            radar_data.append(s)

        strengths = scoring.get('strengths', ['待补充'])
        weaknesses = scoring.get('weaknesses', ['待补充'])

        return f'''<div id="section13c" class="glass-card p-8 fade-in">
    <h2 class="section-header text-2xl font-bold text-white mb-6">附录：通用可行性评分</h2>
    <div class="canvas-section">
        <h3 class="text-sm text-gray-400 mb-2">各维度评分雷达图</h3>
        <canvas id="scoringRadarChart"></canvas>
    </div>
    <div class="mt-6 overflow-x-auto">
        <table class="w-full">
            <thead><tr class="text-left text-sm text-gray-400">
                <th class="pb-3 font-medium">评估维度</th>
                <th class="pb-3 font-medium">得分</th>
                <th class="pb-3 font-medium">权重</th>
                <th class="pb-3 font-medium">加权分</th>
                <th class="pb-3 font-medium">说明</th>
            </tr></thead>
            <tbody>{rows}
                <tr class="border-t border-white/20">
                    <td class="table-cell py-3 font-medium text-white">总分</td>
                    <td class="table-cell py-3"></td>
                    <td class="table-cell py-3 font-medium">100</td>
                    <td class="table-cell py-3 font-bold text-white">{score}</td>
                    <td class="table-cell py-3"></td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="mt-6 grid grid-cols-2 gap-4">
        <div class="bg-green-500/10 rounded-xl p-4 border border-green-500/20">
            <h4 class="font-medium text-green-300 mb-2">最大优势</h4>
            <ul class="text-sm text-gray-400 space-y-1">{''.join([f'<li>• {self._esc(s)}</li>' for s in strengths[:3]])}</ul>
        </div>
        <div class="bg-red-500/10 rounded-xl p-4 border border-red-500/20">
            <h4 class="font-medium text-red-300 mb-2">最大短板</h4>
            <ul class="text-sm text-gray-400 space-y-1">{''.join([f'<li>• {self._esc(w)}</li>' for w in weaknesses[:3]])}</ul>
        </div>
    </div>
    <script type="application/json" id="radarChartData">{{"labels": {json.dumps(radar_labels, ensure_ascii=False)}, "data": {json.dumps(radar_data)}}}</script>
</div>'''

    def _section_crowdfunding(self, data: Dict) -> str:
        """募资平台专项分析 HTML 章节"""
        product = data.get('product', {})
        category = data.get('category', 'hardware')
        product_name = product.get('name', '未命名产品')
        cost_raw = product.get('cost', 300)

        try:
            cost = float(str(cost_raw).replace(',', '').replace('¥', '').replace('NT$', '').replace('$', ''))
        except (ValueError, TypeError):
            cost = 300

        crowdfunding = data.get('crowdfunding', {})

        platform_map = {
            'hardware': [('Kickstarter', 5, '全球最大，适合硬件/创新产品出海', '5%+3%', '$10万-$100万'),
                         ('嘖嘖', 4, '台湾最大众筹平台，适合中文市场', '5%+3%', '¥500万-¥1500万'),
                         ('Indiegogo', 3, '灵活审核，适合有争议或创新产品', '5%+5%', '$5万-$50万'),
                         ('FlyingV', 3, '台湾本土，适合文创/设计类', '8%+3%', '¥200万-¥800万'),
                         ('摩点', 3, '中国大陆，适合ACG/文创', '5%+3%', '¥100万-¥500万')],
            'ai': [('Kickstarter', 5, '全球最大，适合AI硬件出海', '5%+3%', '$10万-$100万'),
                   ('嘖嘖', 4, '台湾最大众筹平台，适合中文市场', '5%+3%', '¥500万-¥1500万'),
                   ('Indiegogo', 3, '灵活审核，适合有争议或创新产品', '5%+5%', '$5万-$50万'),
                   ('FlyingV', 3, '台湾本土，适合文创/设计类', '8%+3%', '¥200万-¥800万'),
                   ('摩点', 3, '中国大陆，适合ACG/文创', '5%+3%', '¥100万-¥500万')],
            'saas': [('Kickstarter', 5, '全球最大，适合软件工具类', '5%+3%', '$5万-$50万'),
                     ('摩点', 3, '中国大陆，适合软件工具', '5%+3%', '¥100万-¥500万'),
                     ('嘖嘖', 3, '台湾最大众筹平台', '5%+3%', '¥500万-¥1500万'),
                     ('Indiegogo', 3, '灵活审核，适合创新软件', '5%+5%', '$5万-$50万'),
                     ('FlyingV', 2, '台湾本土，适合文创类', '8%+3%', '¥200万-¥800万')],
            'content': [('Patreon', 5, '最适合内容创作者持续募资', '5%-12%', '$1千-$10万'),
                        ('嘖嘖', 4, '台湾最大，适合内容项目', '5%+3%', '¥500万-¥1500万'),
                        ('Kickstarter', 4, '全球最大，适合内容出海', '5%+3%', '$5万-$50万'),
                        ('FlyingV', 3, '台湾本土，适合文创/播客', '8%+3%', '¥200万-¥800万'),
                        ('摩点', 4, '中国大陆，适合ACG/内容', '5%+3%', '¥100万-¥500万')],
            'service': [('嘖嘖', 5, '台湾最大，适合服务类项目', '5%+3%', '¥500万-¥1500万'),
                        ('FlyingV', 4, '台湾本土，适合服务/设计', '8%+3%', '¥200万-¥800万'),
                        ('Kickstarter', 3, '全球最大，适合创新服务', '5%+3%', '$5万-$50万'),
                        ('Indiegogo', 3, '灵活审核', '5%+5%', '$5万-$50万'),
                        ('摩点', 2, '中国大陆', '5%+3%', '¥100万-¥500万')],
            'community': [('嘖嘖', 5, '台湾最大，适合社群类项目', '5%+3%', '¥500万-¥1500万'),
                          ('Patreon', 5, '最适合社群持续运营', '5%-12%', '$1千-$10万'),
                          ('Kickstarter', 3, '全球最大', '5%+3%', '$5万-$50万'),
                          ('FlyingV', 3, '台湾本土', '8%+3%', '¥200万-¥800万'),
                          ('Indiegogo', 2, '灵活审核', '5%+5%', '$5万-$50万')],
            'platform': [('Kickstarter', 5, '全球最大，适合平台类项目', '5%+3%', '$10万-$100万'),
                         ('Indiegogo', 4, '灵活审核，适合创新平台', '5%+5%', '$5万-$50万'),
                         ('嘖嘖', 3, '台湾最大', '5%+3%', '¥500万-¥1500万'),
                         ('FlyingV', 2, '台湾本土', '8%+3%', '¥200万-¥800万'),
                         ('摩点', 2, '中国大陆', '5%+3%', '¥100万-¥500万')],
            'b2b': [('Indiegogo', 5, '灵活审核，适合B2B创新产品', '5%+5%', '$5万-$50万'),
                    ('Kickstarter', 4, '全球最大，适合B2B硬件/工具', '5%+3%', '$10万-$100万'),
                    ('嘖嘖', 3, '台湾最大', '5%+3%', '¥500万-¥1500万'),
                    ('FlyingV', 2, '台湾本土', '8%+3%', '¥200万-¥800万'),
                    ('摩点', 2, '中国大陆', '5%+3%', '¥100万-¥500万')],
        }

        platforms = platform_map.get(category, platform_map['hardware'])
        recommended = crowdfunding.get('recommended', platforms[0][0])

        early_bird = int(cost * 1.3)
        standard = int(cost * 1.7)
        premium = int(cost * 2.5)

        # 平台卡片
        platform_cards = ''
        for p in platforms:
            stars = '★' * p[1] + '☆' * (5 - p[1])
            is_top = 'border-blue-500/30' if p[1] == 5 else 'border-white/10'
            platform_cards += f'''<div class="bg-white/5 rounded-lg p-4 border {is_top}">
                <div class="text-lg font-medium text-white">{self._esc(p[0])}</div>
                <div class="text-sm text-gray-400 mt-1">推荐指数: {self._esc(stars)}</div>
                <div class="text-sm text-gray-300 mt-1">费率: {self._esc(p[3])}</div>
                <div class="text-sm text-gray-400 mt-1">平均募集: {self._esc(p[4])}</div>
                <div class="text-sm text-gray-400 mt-2">{self._esc(p[2])}</div>
            </div>'''

        # 推广阶段卡片
        promo_stages = [
            ('预热期', '上线前30天', '社群运营、邮件列表、KOL种草', '积累500+潜在backer',
             'from-blue-500/20 to-blue-600/10', 'border-blue-500/30', '#3b82f6'),
            ('首日冲刺', 'Day 1', '紧迫感营销、亲友支持、社群转发', '达标30%',
             'from-green-500/20 to-green-600/10', 'border-green-500/30', '#10b981'),
            ('持续期', 'Day 2-25', '每日更新、回复留言、KOL评测', '达标75%',
             'from-yellow-500/20 to-yellow-600/10', 'border-yellow-500/30', '#f59e0b'),
            ('收尾冲刺', 'Day 26-30', '追加福利、限时加价、社交分享', '达标100%+',
             'from-red-500/20 to-red-600/10', 'border-red-500/30', '#ef4444'),
        ]

        promo_cards = ''
        for stage_name, stage_time, stage_action, stage_goal, bg_class, border_class, color in promo_stages:
            promo_cards += f'''<div class="bg-gradient-to-r {bg_class} rounded-xl p-4 border {border_class}">
                <div class="flex items-center gap-2 mb-2">
                    <div class="w-2 h-2 rounded-full" style="background: {color}"></div>
                    <span class="font-semibold text-white">{self._esc(stage_name)}</span>
                    <span class="text-xs text-gray-400 ml-auto">{self._esc(stage_time)}</span>
                </div>
                <div class="text-sm text-gray-300">核心动作：{self._esc(stage_action)}</div>
                <div class="text-sm text-gray-400 mt-1">目标：{self._esc(stage_goal)}</div>
            </div>'''

        # 审核清单
        checklist_items = [
            '产品名称和一句话介绍（50字内）',
            '项目故事/团队介绍（800字以上）',
            '产品原型/Demo/渲染图（至少5张）',
            '募资视频（1-3分钟）',
            '回报档位设计（至少3档）',
            '风险说明和退换政策',
            '团队背景和执行能力证明',
            '供应链/生产计划（硬件类必填）',
            '预计交付时间和物流方案',
        ]

        checklist_html = ''
        for item in checklist_items:
            checklist_html += f'''<div class="flex items-center gap-3 py-2 border-b border-white/5 last:border-0">
                <div class="w-5 h-5 rounded border border-gray-500 flex items-center justify-center flex-shrink-0">
                </div>
                <span class="text-sm text-gray-300">{self._esc(item)}</span>
            </div>'''

        return f'''<div id="section12b" class="glass-card p-8 fade-in mb-12">
    <h2 class="section-header text-2xl font-bold text-white mb-6">募资平台专项分析</h2>

    <!-- 平台选择建议 -->
    <div class="glass-card rounded-xl p-6 mb-6" style="background: rgba(30, 30, 46, 0.5);">
        <h3 class="text-lg font-semibold text-white mb-4">平台选择建议</h3>
        <p class="text-sm text-gray-400 mb-4">根据 <span class="text-blue-400">{self._esc(product_name)}</span> 的品类（<span class="text-blue-400">{self._esc(category)}</span>）和目标市场，推荐平台：</p>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {platform_cards}
        </div>
        <div class="mt-4 p-3 bg-blue-500/10 rounded-lg border border-blue-500/20">
            <span class="text-sm font-medium text-blue-300">推荐平台：</span>
            <span class="text-sm text-white">{self._esc(recommended)}</span>
        </div>
    </div>

    <!-- 募资定价策略 -->
    <div class="glass-card rounded-xl p-6 mb-6" style="background: rgba(30, 30, 46, 0.5);">
        <h3 class="text-lg font-semibold text-white mb-4">募资定价策略</h3>
        <p class="text-sm text-gray-400 mb-4">基于成本 ¥{cost:.0f}，建议三档定价：</p>
        <div class="overflow-x-auto">
            <table class="w-full text-sm">
                <thead>
                    <tr class="border-b border-white/10">
                        <th class="text-left py-3 px-4 text-gray-400 font-medium">档位</th>
                        <th class="text-left py-3 px-4 text-gray-400 font-medium">价格</th>
                        <th class="text-left py-3 px-4 text-gray-400 font-medium">数量限制</th>
                        <th class="text-left py-3 px-4 text-gray-400 font-medium">内容</th>
                        <th class="text-left py-3 px-4 text-gray-400 font-medium">预期转化</th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="border-b border-white/5">
                        <td class="py-3 px-4 text-green-400 font-medium">早鸟档</td>
                        <td class="py-3 px-4 text-white font-semibold">¥{early_bird}</td>
                        <td class="py-3 px-4 text-gray-300">前100名</td>
                        <td class="py-3 px-4 text-gray-300">标准版+感谢信</td>
                        <td class="py-3 px-4 text-gray-300">40%</td>
                    </tr>
                    <tr class="border-b border-white/5">
                        <td class="py-3 px-4 text-blue-400 font-medium">标准档</td>
                        <td class="py-3 px-4 text-white font-semibold">¥{standard}</td>
                        <td class="py-3 px-4 text-gray-300">500名</td>
                        <td class="py-3 px-4 text-gray-300">标准版+配件</td>
                        <td class="py-3 px-4 text-gray-300">45%</td>
                    </tr>
                    <tr>
                        <td class="py-3 px-4 text-purple-400 font-medium">豪华档</td>
                        <td class="py-3 px-4 text-white font-semibold">¥{premium}</td>
                        <td class="py-3 px-4 text-gray-300">50名</td>
                        <td class="py-3 px-4 text-gray-300">全套+定制+优先发货</td>
                        <td class="py-3 px-4 text-gray-300">15%</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- 推广策略时间线 -->
    <div class="glass-card rounded-xl p-6 mb-6" style="background: rgba(30, 30, 46, 0.5);">
        <h3 class="text-lg font-semibold text-white mb-4">推广策略时间线</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            {promo_cards}
        </div>
    </div>

    <!-- 审核准备清单 -->
    <div class="glass-card rounded-xl p-6" style="background: rgba(30, 30, 46, 0.5);">
        <h3 class="text-lg font-semibold text-white mb-4">平台审核准备清单</h3>
        {checklist_html}
    </div>
</div>'''

    def _section_action_plan(self, data: Dict) -> str:
        tasks = [
            ('制作产品展示与试用案例视频', '展示产品效果，记录真实用户试用反馈', '产品团队', '第3天', 'high'),
            ('制定定价套餐', 'A/B/C/D款价格和服务期限，参考竞品定价', '商业团队', '第5天', 'high'),
            ('准备数据授权协议', '授权书、删除机制、数据使用边界', '法务团队', '第7天', 'medium'),
            ('完成竞品深度分析', '覆盖3-5个直接竞品，提炼差异化策略', '市场团队', '第4天', 'medium'),
            ('完成用户访谈5-10人', '验证痛点真实性和付费意愿', '产品团队', '第7天', 'high'),
        ]
        tasks_html = ''
        for i, (name, desc, owner, deadline, level) in enumerate(tasks, 1):
            tasks_html += f'''<div class="priority-{level} bg-{'red' if level=='high' else 'yellow'}-500/5 rounded-xl p-4">
    <div class="flex items-start gap-3">
        <div class="w-8 h-8 rounded-full bg-{'red' if level=='high' else 'yellow'}-500/20 flex items-center justify-center flex-shrink-0">
            <span class="text-{'red' if level=='high' else 'yellow'}-400 font-bold">{i}</span>
        </div>
        <div>
            <div class="font-medium text-white">{self._esc(name)}</div>
            <div class="text-sm text-gray-400 mt-1">{self._esc(desc)}</div>
            <div class="text-xs text-gray-500 mt-2">负责人：{self._esc(owner)} | 截止：{self._esc(deadline)}</div>
        </div>
    </div>
</div>'''

        weaknesses = data.get('scoring', {}).get('weaknesses', ['待补充'])
        weaknesses_html = ''
        for i, w in enumerate(weaknesses[:3]):
            level = 'risk' if i == 0 else 'poor' if i == 1 else 'normal'
            weaknesses_html += f'''<div class="bg-{'red' if i==0 else 'orange' if i==1 else 'yellow'}-500/10 rounded-xl p-4">
    <div class="flex items-center justify-between mb-2">
        <span class="font-medium text-{'red' if i==0 else 'orange' if i==1 else 'yellow'}-300">{self._esc(w)}</span>
        <span class="tag tag-{level}">{'高' if i==0 else '中'}优先级</span>
    </div>
    <p class="text-sm text-gray-400">需要尽快补强的关键短板</p>
</div>'''

        plan30 = [
            '完成产品展示视频和用户案例素材制作',
            '完成A/B/C/D款定价策略和价值包装',
            '完成数据授权协议和隐私政策文档',
            '完成3-5个家庭试用并收集反馈',
            '完成供应链评估和生产计划',
        ]
        plan_html = ''.join([f'''<li class="flex items-center gap-2">
    <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
    <span class="text-sm text-gray-400">{self._esc(item)}</span>
</li>''' for item in plan30])

        return f'''<div id="section15" class="glass-card p-8 fade-in">
    <h2 class="section-header text-2xl font-bold text-white mb-6">十四、募资行动建议</h2>
    <div class="grid grid-cols-2 gap-6">
        <div>
            <h3 class="text-lg font-semibold text-gray-200 mb-3">7天验证任务</h3>
            <div class="space-y-3">{tasks_html}</div>
        </div>
        <div>
            <h3 class="text-lg font-semibold text-gray-200 mb-3">关键补强短板</h3>
            <div class="space-y-3">{weaknesses_html}</div>
            <div class="mt-6">
                <h3 class="text-lg font-semibold text-gray-200 mb-3">30天推进计划</h3>
                <ul class="space-y-2">{plan_html}</ul>
            </div>
        </div>
    </div>
</div>'''

    def _section_communication(self, data: Dict) -> str:
        product = data.get('product', {})
        scoring = data.get('scoring', {})
        score = scoring.get('total_score', 0)
        strengths = scoring.get('strengths', ['待补充'])
        weaknesses = scoring.get('weaknesses', ['待补充'])
        name = product.get('name', '本产品')
        desc = product.get('description', '')
        value = product.get('value_proposition', '待补充')
        target = product.get('target_users', '待补充')
        platform = product.get('platform', '募资平台')
        amount = (product.get('target_amount') or '待确定')
        category = data.get('category', '')

        investor = f"""我们正在做一款{name}，{desc[:80] if desc else '帮用户解决核心痛点'}。目前已完成初步验证，可行性评分{score}/100，计划通过{platform}进行募资，目标金额{amount}。核心优势是{strengths[0] if strengths else '待补充'}，需要补强的是{weaknesses[0] if weaknesses else '待补充'}。"""

        partner = f"""{name}是一款面向{target}的产品，核心价值在于{value}。我们正在寻找供应链、渠道方面的合作伙伴，共同推动产品落地。"""

        platform_pitch = f"""本项目属于{category}品类，已有产品原型，团队具备相关经验。目标用户明确，痛点真实存在，商业模式清晰。预计募集{amount}，用于首批生产和市场推广。"""

        return f'''<div id="section16" class="glass-card p-8 fade-in">
    <h2 class="section-header text-2xl font-bold text-white mb-6">十五、沟通话术</h2>
    <div class="space-y-6">
        <div class="bg-gradient-to-r from-purple-500/10 to-blue-500/10 rounded-xl p-6 border border-purple-500/20">
            <h3 class="text-lg font-semibold text-white mb-4">投资人汇报话术</h3>
            <p class="text-gray-300 leading-relaxed">{self._esc(investor)}</p>
        </div>
        <div class="bg-gradient-to-r from-blue-500/10 to-green-500/10 rounded-xl p-6 border border-blue-500/20">
            <h3 class="text-lg font-semibold text-white mb-4">募资平台文案话术</h3>
            <p class="text-gray-300 leading-relaxed">{self._esc(platform_pitch)}</p>
        </div>
        <div class="bg-gradient-to-r from-green-500/10 to-orange-500/10 rounded-xl p-6 border border-green-500/20">
            <h3 class="text-lg font-semibold text-white mb-4">合作伙伴沟通话术</h3>
            <p class="text-gray-300 leading-relaxed">{self._esc(partner)}</p>
        </div>
    </div>
</div>'''

    def _chart_js_code(self, data: Dict) -> str:
        scoring = data.get('scoring', {})
        scores = scoring.get('scores', {})
        radar_labels = []
        radar_data = []
        for dim_info in self.scoring_model['dimensions']:
            name = dim_info['name']
            info = scores.get(name, {'score': 0})
            radar_labels.append(name)
            radar_data.append(info.get('score', 0))

        tam_num = self._extract_number(data.get('tam', '8000')) or 8000
        sam_num = self._extract_number(data.get('sam', '2000')) or 2000
        som_num = self._extract_number(data.get('som', '50')) or 50

        cost_data = [40, 25, 20, 15]
        cost_labels = ['硬件/BOM', '制造', '营销', '运营']

        return f'''
            // 雷达图
            const radarCtx = document.getElementById('scoringRadarChart');
            if (radarCtx) {{
                new Chart(radarCtx.getContext('2d'), {{
                    type: 'radar',
                    data: {{
                        labels: {json.dumps(radar_labels, ensure_ascii=False)},
                        datasets: [{{
                            label: '得分',
                            data: {json.dumps(radar_data)},
                            borderColor: '#60a5fa',
                            backgroundColor: 'rgba(96, 165, 250, 0.2)',
                            pointBackgroundColor: '#60a5fa'
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{ legend: {{ display: false }} }},
                        scales: {{
                            r: {{
                                angleLines: {{ color: 'rgba(255,255,255,0.1)' }},
                                grid: {{ color: 'rgba(255,255,255,0.1)' }},
                                pointLabels: {{ color: '#9ca3af', font: {{ size: 11 }} }},
                                ticks: {{ display: false }},
                                suggestedMin: 0,
                                suggestedMax: 100
                            }}
                        }}
                    }}
                }});
            }}

            // 市场规模柱状图
            const barCtx = document.getElementById('marketSizingChart');
            if (barCtx) {{
                new Chart(barCtx.getContext('2d'), {{
                    type: 'bar',
                    data: {{
                        labels: ['TAM', 'SAM', 'SOM'],
                        datasets: [{{
                            label: '市场规模',
                            data: [{tam_num}, {sam_num}, {som_num}],
                            backgroundColor: ['#60a5fa', '#a78bfa', '#34d399'],
                            borderRadius: 8
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{ legend: {{ display: false }} }},
                        scales: {{
                            x: {{ grid: {{ display: false }}, ticks: {{ color: '#9ca3af' }} }},
                            y: {{ grid: {{ color: 'rgba(255,255,255,0.1)' }}, ticks: {{ color: '#9ca3af' }} }}
                        }}
                    }}
                }});
            }}

            // 成本结构饼图
            const pieCtx = document.getElementById('costStructureChart');
            if (pieCtx) {{
                new Chart(pieCtx.getContext('2d'), {{
                    type: 'doughnut',
                    data: {{
                        labels: {json.dumps(cost_labels, ensure_ascii=False)},
                        datasets: [{{
                            data: {json.dumps(cost_data)},
                            backgroundColor: ['#60a5fa', '#a78bfa', '#fbbf24', '#34d399'],
                            borderWidth: 0
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{ position: 'right', labels: {{ color: '#9ca3af', padding: 10 }} }}
                        }}
                    }}
                }});
            }}

            // 市场趋势折线图
            const lineCtx = document.getElementById('marketTrendChart');
            if (lineCtx) {{
                new Chart(lineCtx.getContext('2d'), {{
                    type: 'line',
                    data: {{
                        labels: ['2022', '2023', '2024', '2025', '2026E', '2027E'],
                        datasets: [{{
                            label: '全球AI硬件市场(亿美元)',
                            data: [280, 380, 520, 680, 800, 980],
                            borderColor: '#60a5fa',
                            backgroundColor: 'rgba(96, 165, 250, 0.1)',
                            fill: true,
                            tension: 0.4
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{ legend: {{ display: false }} }},
                        scales: {{
                            x: {{ grid: {{ color: 'rgba(255,255,255,0.1)' }}, ticks: {{ color: '#9ca3af' }} }},
                            y: {{ grid: {{ color: 'rgba(255,255,255,0.1)' }}, ticks: {{ color: '#9ca3af' }} }}
                        }}
                    }}
                }});
            }}
        '''

    def _extract_number(self, text: str) -> int:
        """从文本中提取数字"""
        if not text:
            return 0
        import re
        nums = re.findall(r'[\d,]+', str(text))
        if nums:
            try:
                return int(nums[0].replace(',', ''))
            except ValueError:
                return 0
        return 0

    def save_html(self, content: str, filename: str, reports_dir: str = None) -> str:
        if reports_dir is None:
            reports_dir = os.path.join(os.path.dirname(__file__), '../reports')
        os.makedirs(reports_dir, exist_ok=True)
        safe_name = ''.join(c for c in filename if c.isalnum() or c in ('-', '_', ' ')).strip().replace(' ', '-')
        if not safe_name.endswith('.html'):
            safe_name += '-完整可行性分析.html'
        filepath = os.path.join(reports_dir, safe_name)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath


if __name__ == '__main__':
    generator = FullReportGenerator()
    html_gen = FullHTMLReportGenerator()

    test_data = {
        'product': {
            'name': 'AI智能陪伴机器人',
            'description': '一款基于AI技术的情感陪伴机器人，通过3D打印模型接入AI技术，支持真人形象复刻及虚拟人物定制。',
            'target_users': '独居老人、儿童、情感需求人群',
            'value_proposition': '24小时陪伴，情感交流，个性化服务',
            'platform': '啧啧',
            'target_amount': '¥500,000',
            'cost': 300,
            'pain_points': '空巢老人情感孤独，子女无法长期陪伴',
            'current_alternatives': '智能音箱、视频通话',
            'alternative_weakness': '缺乏实体存在感和情感温度',
            'channels': '募资平台、社交媒体、KOL合作',
            'customer_relation': '社群运营、用户反馈、持续迭代',
            'revenue_source': '产品销售、订阅服务',
            'key_resources': '技术团队、供应链、品牌',
            'key_activities': '产品研发、生产制造、市场推广',
            'key_partners': '供应商、分销渠道、技术伙伴',
            'cost_structure': '硬件成本、研发成本、营销成本',
        },
        'category': 'hardware',
        'scoring': {
            'total_score': 72,
            'scores': {
                '痛点强度': {'weight': 15, 'score': 80, 'comment': '情感陪伴需求真实存在'},
                '目标用户清晰度': {'weight': 10, 'score': 70, 'comment': '用户群体明确'},
                '竞争壁垒': {'weight': 10, 'score': 50, 'comment': '技术壁垒一般'},
                '产品可演示性': {'weight': 10, 'score': 80, 'comment': 'Demo直观'},
                '技术/生产可行性': {'weight': 10, 'score': 60, 'comment': 'AI技术成熟'},
                '合规与信任': {'weight': 10, 'score': 70, 'comment': '需关注隐私合规'},
                '商业模式': {'weight': 10, 'score': 70, 'comment': '定价合理'},
                '市场推广可行性': {'weight': 10, 'score': 60, 'comment': '需要精准获客'},
                '团队匹配度': {'weight': 10, 'score': 70, 'comment': '团队有相关经验'},
                '证据完整度': {'weight': 5, 'score': 40, 'comment': '需要更多用户验证'},
            },
            'strengths': ['痛点真实明确', '产品演示性强', '定价合理'],
            'weaknesses': ['竞争壁垒不足', '获客难度较大', '隐私合规风险'],
        },
        'financial_analysis': {
            'pricing': {'retail_price': 600},
            'margin': 50,
            'backers_needed': {'total_backers': 1000},
            'revenue': {'actual_revenue_cny': 450000},
            'breakeven': {'backers_needed': 723},
        },
        'similar_cases': [
            {'name': 'AI陪伴机器人X1', 'category': '机器人', 'amount_raised': '¥240万', 'backers': '2890', 'success_rate': '240%'},
        ],
        'tam': '$800亿',
        'sam': '¥2,000亿',
        'som': '¥50亿',
        'market_size_score': 8,
        'market_size_reason': '老龄化市场增长空间大',
        'margin_expectation': '50%',
        'payback_period': '12-18个月',
        'financial_health_score': 7,
        'swot': {
            'strengths': ['产品已成型', '情感陪伴痛点真实', '四款产品分层清晰'],
            'weaknesses': ['品牌知名度低', '定价策略待优化', '交付周期待明确'],
            'opportunities': ['老龄化社会刚需', '情感陪伴赛道竞争少', '实体化产品适合募资'],
            'threats': ['数据隐私合规风险', '大厂可能进入赛道', '用户接受度不确定'],
        },
        'pest': {
            'political': ['国家支持银发经济发展', '数据隐私保护法规严格'],
            'economic': ['AI硬件市场年增长35%', '消费升级趋势明显'],
            'social': ['老龄化社会加剧', '空巢老人情感需求突出'],
            'technological': ['语音合成技术成熟', '3D打印成本下降'],
        },
        'porter_forces': [
            {'name': '现有竞争者威胁', 'level': '中高', 'width': 75, 'color': 'bg-orange-500', 'desc': 'AI硬件赛道竞争激烈'},
            {'name': '潜在进入者威胁', 'level': '中等', 'width': 55, 'color': 'bg-yellow-500', 'desc': '技术门槛降低'},
            {'name': '替代品威胁', 'level': '中低', 'width': 40, 'color': 'bg-blue-500', 'desc': '实体化体验难以替代'},
            {'name': '供应商议价能力', 'level': '中等', 'width': 50, 'color': 'bg-yellow-500', 'desc': '芯片供应商集中'},
            {'name': '购买者议价能力', 'level': '中高', 'width': 70, 'color': 'bg-orange-500', 'desc': '消费者价格敏感'},
        ],
        'competitor_analysis': {
            'competitors': [
                {'name': '小爱音箱', 'category': '智能音箱', 'features': '语音交互', 'price': '¥299', 'relation': '间接竞品'},
            ],
            'real_cases': [
                {'name': 'Eiliko AI Charm Bot', 'platform': 'Kickstarter', 'date': '2025年', 'description': '情感陪伴定位的可穿戴机器人', 'amount_raised': '$38万', 'backers': '3,000+', 'url': 'https://www.kickstarter.com/projects/eiliko/eiliko-ai-charm-bot'},
            ],
        },
        'mvp_features': '语音交互、情感识别、个性化定制',
        'tech_stack': 'AI模型 + 硬件模块 + 云端服务',
        'dev_cycle': '3-6个月',
    }

    md_report = generator.generate_full_report(test_data)
    print("Markdown报告生成完成")

    html_report = html_gen.generate_full_html(test_data)
    html_path = html_gen.save_html(html_report, 'AI智能陪伴机器人')
    print(f"HTML报告已保存: {html_path}")
