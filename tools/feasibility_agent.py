#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
产品可行性分析智能体 - 完整版
整合项目所有资源：增长飞轮、市场规模、财务模型、数据指标、技术架构、时间规划、退出策略、迭代引擎
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(__file__))

from competitor_analysis import CompetitorDatabase, CompetitorAnalyzer
from analysis_tool import FeasibilityAnalyzer, CrowdfundingCalculator
from full_report_generator import FullReportGenerator, FullHTMLReportGenerator
from llm_analyzer import LLMAnalyzer
from agent_iteration_engine import AgentIterationEngine, CaseLibraryGenerator

import re


class RuleBasedExtractor:
    """基于规则的产品信息提取器，无需LLM API即可从产品描述中提取结构化信息"""

    @staticmethod
    def extract(raw_text: str) -> Dict:
        text = raw_text.strip()

        result = {
            'name': RuleBasedExtractor._extract_name(text),
            'description': RuleBasedExtractor._extract_description(text),
            'target_users': RuleBasedExtractor._extract_target_users(text),
            'value_proposition': RuleBasedExtractor._extract_value_proposition(text),
            'features': RuleBasedExtractor._extract_features(text),
            'business_model': RuleBasedExtractor._extract_business_model(text),
            'cost': RuleBasedExtractor._extract_cost(text),
            'target_amount': RuleBasedExtractor._extract_target_amount(text),
            'platform': RuleBasedExtractor._extract_platform(text),
            'avg_pledge': RuleBasedExtractor._extract_avg_pledge(text),
            'category': RuleBasedExtractor._identify_category(text),
            'suggested_scores': RuleBasedExtractor.generate_suggested_scores(text),
            'pain_points': RuleBasedExtractor._extract_pain_points(text),
        }

        if result['avg_pledge'] is None:
            result['avg_pledge'] = 500

        return result

    @staticmethod
    def _extract_name(text: str) -> str:
        patterns = [
            r'产品名称[：:]\s*([^\n，。]+)',
            r'产品名[：:]\s*([^\n，。]+)',
            r'名称[：:]\s*([^\n，。]+)',
            r'项目[：:]\s*([^\n，。]+)',
        ]
        for p in patterns:
            m = re.search(p, text)
            if m:
                return m.group(1).strip()
        return ''

    @staticmethod
    def _extract_description(text: str) -> str:
        patterns = [
            r'(?:产品)?描述[：:]\s*([^\n]+(?:\n[^\n]*){0,2})',
            r'介绍[：:]\s*([^\n]+(?:\n[^\n]*){0,2})',
            r'核心价值[：:]\s*([^\n]+)',
            r'产品简介[：:]\s*([^\n]+(?:\n[^\n]*){0,2})',
        ]
        for p in patterns:
            m = re.search(p, text)
            if m:
                desc = m.group(1).strip()
                if len(desc) > 5:
                    return desc[:300]
        return text[:300].strip()

    @staticmethod
    def _extract_target_users(text: str) -> str:
        patterns = [
            r'目标用户[：:]\s*([^\n，。]+)',
            r'用户[：:]\s*([^\n，。]+)',
            r'面向[：:]\s*([^\n，。]+)',
            r'受众[：:]\s*([^\n，。]+)',
        ]
        for p in patterns:
            m = re.search(p, text)
            if m:
                return m.group(1).strip()
        return ''

    @staticmethod
    def _extract_value_proposition(text: str) -> str:
        patterns = [
            r'核心价值[：:]\s*([^\n]+)',
            r'价值主张[：:]\s*([^\n]+)',
            r'卖点[：:]\s*([^\n]+)',
            r'优势[：:]\s*([^\n]+)',
        ]
        for p in patterns:
            m = re.search(p, text)
            if m:
                return m.group(1).strip()
        return ''

    @staticmethod
    def _extract_features(text: str) -> List[str]:
        patterns = [
            r'功能[：:]\s*([^\n]+)',
            r'(?:核心)?特性[：:]\s*([^\n]+)',
            r'功能列表[：:]\s*([^\n]+)',
        ]
        for p in patterns:
            m = re.search(p, text)
            if m:
                content = m.group(1)
                items = re.split(r'[,，、;；\n]+', content)
                return [i.strip() for i in items if i.strip() and len(i.strip()) > 1]
        return []

    @staticmethod
    def _extract_business_model(text: str) -> str:
        keywords = {
            '订阅': 'subscription',
            '月费': 'subscription',
            '年费': 'subscription',
            '会员': 'subscription',
            'SaaS': 'saas',
            '一次性': 'one-time',
            '买断': 'one-time',
            '零售': 'one-time',
            '广告': 'advertising',
            '平台抽成': 'platform-commission',
            '佣金': 'commission',
            '抽成': 'commission',
            '撮合': 'platform-commission',
            '服务费': 'service-fee',
        }
        for kw, model in keywords.items():
            if kw in text:
                return model
        return ''

    @staticmethod
    def _extract_cost(text: str) -> Optional[float]:
        patterns = [
            r'成本[：:]\s*约?\s*([\d,\.]+)\s*[元¥$]',
            r'(?:硬件)?成本[：:]\s*约?\s*([\d,\.]+)\s*[元¥$]',
            r'价格[：:]\s*([\d,\.]+)\s*[元¥$]',
            r'售价[：:]\s*([\d,\.]+)\s*[元¥$]',
        ]
        for p in patterns:
            m = re.search(p, text)
            if m:
                num_str = m.group(1).replace(',', '')
                try:
                    return float(num_str)
                except ValueError:
                    continue
        return None

    @staticmethod
    def _extract_target_amount(text: str) -> Optional[float]:
        # 先匹配带"万"的金额
        wan_patterns = [
            r'目标金额[：:]\s*([\d,\.]+)\s*万',
            r'募资[：:]\s*([\d,\.]+)\s*万',
            r'众筹[：:]\s*([\d,\.]+)\s*万',
            r'目标[：:]\s*([\d,\.]+)\s*万',
        ]
        for p in wan_patterns:
            m = re.search(p, text)
            if m:
                num_str = m.group(1).replace(',', '')
                try:
                    return float(num_str) * 10000
                except ValueError:
                    continue

        # 再匹配不带"万"的金额
        patterns = [
            r'目标金额[：:]\s*([\d,\.]+)',
            r'募资[：:]\s*([\d,\.]+)',
            r'众筹[：:]\s*([\d,\.]+)',
            r'目标[：:]\s*([\d,\.]+)',
        ]
        for p in patterns:
            m = re.search(p, text)
            if m:
                num_str = m.group(1).replace(',', '')
                try:
                    val = float(num_str)
                    # 简单启发：小于1000且上下文有"元"则保持原值
                    # 大于1000且没有"万"也保持原值
                    return val
                except ValueError:
                    continue
        return None

    @staticmethod
    def _extract_platform(text: str) -> str:
        m = re.search(r'平台[：:]\s*([^\n，。]+)', text)
        if m:
            plat = m.group(1).strip()
            if '啧' in plat or 'zeczec' in plat.lower():
                return 'zeczec'
            if 'kickstarter' in plat.lower():
                return 'kickstarter'
            if 'indiegogo' in plat.lower():
                return 'indiegogo'
            if '摩点' in plat:
                return 'modian'
            return plat
        if '啧啧' in text or 'zeczec' in text.lower():
            return 'zeczec'
        if 'kickstarter' in text.lower():
            return 'kickstarter'
        if 'indiegogo' in text.lower():
            return 'indiegogo'
        if '摩点' in text:
            return 'modian'
        return 'zeczec'

    @staticmethod
    def _extract_avg_pledge(text: str) -> Optional[float]:
        cost = RuleBasedExtractor._extract_cost(text)
        if cost:
            return cost * 1.5

        m = re.search(r'客单价[：:]\s*([\d,\.]+)', text)
        if m:
            try:
                return float(m.group(1).replace(',', ''))
            except ValueError:
                pass
        return None

    @staticmethod
    def _identify_category(text: str) -> str:
        text_lower = text.lower()
        if any(k in text_lower for k in ['app', '应用', '软件', 'saas', '订阅']):
            return 'saas'
        if any(k in text_lower for k in ['服务', '咨询', '培训', '代运营']):
            return 'service'
        if any(k in text_lower for k in ['内容', '文章', '视频', '播客', '课程']):
            return 'content'
        if any(k in text_lower for k in ['社群', '社区', '会员', '俱乐部']):
            return 'community'
        if any(k in text_lower for k in ['平台', 'marketplace', '撮合', '连接']):
            return 'platform'
        if any(k in text_lower for k in ['b2b', '企业', '商家', '批发', '供应链']):
            return 'b2b'
        return 'hardware'

    @staticmethod
    def _extract_pain_points(text: str) -> List[str]:
        patterns = [
            r'痛点[：:]\s*([^\n]+)',
            r'问题[：:]\s*([^\n]+)',
        ]
        for p in patterns:
            m = re.search(p, text)
            if m:
                items = re.split(r'[,，、;；\n]+', m.group(1))
                return [i.strip() for i in items if i.strip() and len(i.strip()) > 1]
        return []

    @staticmethod
    def generate_suggested_scores(text: str) -> Dict[str, int]:
        text_lower = text.lower()
        scores = {}

        # 1. 痛点强度
        if any(k in text_lower for k in ['痛点', '刚需', '急需', '必须', '困扰', '难题']):
            scores['痛点强度'] = 8
        elif any(k in text_lower for k in ['痒点', '改善', '优化']):
            scores['痛点强度'] = 6
        else:
            scores['痛点强度'] = 5

        # 2. 目标用户清晰度
        if any(k in text_lower for k in ['目标用户', '面向', '受众', '人群', '画像']):
            scores['目标用户清晰度'] = 8
        elif any(k in text_lower for k in ['所有人', '每个', '全部']):
            scores['目标用户清晰度'] = 3
        else:
            scores['目标用户清晰度'] = 5

        # 3. 竞争壁垒
        if any(k in text_lower for k in ['专利', '独家', '唯一', '首创', '自主研发', '核心算法', '技术壁垒']):
            scores['竞争壁垒'] = 8
        elif any(k in text_lower for k in ['独特', '创新', '差异化', '优势']):
            scores['竞争壁垒'] = 7
        elif any(k in text_lower for k in ['同质化', '竞争激烈', '红海', '模仿']):
            scores['竞争壁垒'] = 4
        else:
            scores['竞争壁垒'] = 5

        # 4. 产品可演示性
        if any(k in text_lower for k in ['硬件', '实体', '设备', '原型', '样品', 'demo']):
            scores['产品可演示性'] = 8
        elif any(k in text_lower for k in ['软件', 'app', '平台', '工具']):
            scores['产品可演示性'] = 7
        elif any(k in text_lower for k in ['概念', '想法', '策划']):
            scores['产品可演示性'] = 3
        else:
            scores['产品可演示性'] = 5

        # 5. 技术可行性
        if any(k in text_lower for k in ['技术成熟', '已验证', '原型', '量产', '现成技术']):
            scores['技术可行性'] = 8
        elif any(k in text_lower for k in ['前沿技术', '实验室', '理论', '突破', '首创']):
            scores['技术可行性'] = 4
        else:
            scores['技术可行性'] = 5

        # 6. 合规与信任
        if any(k in text_lower for k in ['合规', '认证', '标准', '安全', '隐私保护']):
            scores['合规与信任'] = 8
        elif any(k in text_lower for k in ['监管', '政策风险', '法律', '资质']):
            scores['合规与信任'] = 4
        else:
            scores['合规与信任'] = 5

        # 7. 商业模式
        if any(k in text_lower for k in ['盈利模式', '变现', '收入', '订阅', '付费', '广告']):
            scores['商业模式'] = 8
        elif any(k in text_lower for k in ['探索中', '未确定', '免费', '补贴']):
            scores['商业模式'] = 4
        else:
            scores['商业模式'] = 5

        # 8. 市场推广
        if any(k in text_lower for k in ['大市场', '高增长', '蓝海', '风口', '趋势', '红利']):
            scores['市场推广'] = 8
        elif any(k in text_lower for k in ['小众', '细分', '利基', '天花板']):
            scores['市场推广'] = 6
        else:
            scores['市场推广'] = 5

        # 9. 团队匹配度
        if any(k in text_lower for k in ['有经验', '有资源', '有背景', '行业资深', '专家', '连续创业者']):
            scores['团队匹配度'] = 8
        elif any(k in text_lower for k in ['缺乏经验', '新手', '跨界']):
            scores['团队匹配度'] = 4
        else:
            scores['团队匹配度'] = 5

        # 10. 证据完整度
        if any(k in text_lower for k in ['已有用户', '已验证', 'mvp', '付费用户', '种子用户', '数据验证']):
            scores['证据完整度'] = 8
        elif any(k in text_lower for k in ['概念', '想法', '调研', '计划']):
            scores['证据完整度'] = 4
        else:
            scores['证据完整度'] = 5

        # ============ 募资维度评分（0-10分制） ============

        # 11. 产品展示力（募资维度）
        if any(k in text_lower for k in ['demo', '原型', '视频', '渲染图', '样品', '样机', 'prototype', '实物']):
            scores['cf_产品展示力'] = 9
        elif any(k in text_lower for k in ['概念', '设计图', '概念图', '设计稿']):
            scores['cf_产品展示力'] = 6
        elif any(k in text_lower for k in ['硬件', '设备', '实体', '耳机', '机器人', '音箱', '手表']):
            scores['cf_产品展示力'] = 7
        else:
            scores['cf_产品展示力'] = 4

        # 12. 信任证据（募资维度）
        if any(k in text_lower for k in ['团队经验', '过往项目', '专利', '合作', '行业资深', '专家', '连续创业']):
            scores['cf_信任证据'] = 9
        elif any(k in text_lower for k in ['有经验', '有资源', '有背景', '有认证']):
            scores['cf_信任证据'] = 7
        elif any(k in text_lower for k in ['初创', '学生', '新手']):
            scores['cf_信任证据'] = 4
        else:
            scores['cf_信任证据'] = 3

        # 13. 定价合理性（募资维度）
        cost = RuleBasedExtractor._extract_cost(text)
        target = RuleBasedExtractor._extract_target_amount(text)
        if cost and target and cost > 0:
            ratio = target / cost
            if 100 <= ratio <= 10000:
                scores['cf_定价合理性'] = 7
            elif ratio < 100 or ratio > 10000:
                scores['cf_定价合理性'] = 4
            else:
                scores['cf_定价合理性'] = 5
        else:
            scores['cf_定价合理性'] = 5

        # 14. 推广准备度（募资维度）
        if any(k in text_lower for k in ['社群', '粉丝', '邮件列表', 'kol', '网红', '自媒体', '频道']):
            scores['cf_推广准备度'] = 9
        elif any(k in text_lower for k in ['社交媒体', '推广', '营销']):
            scores['cf_推广准备度'] = 7
        else:
            scores['cf_推广准备度'] = 3

        # 15. 履约能力（募资维度）
        if any(k in text_lower for k in ['供应链', '工厂', '生产计划', '交期', '量产', '代工']):
            scores['cf_履约能力'] = 9
        elif any(k in text_lower for k in ['制造', '组装', '生产']):
            scores['cf_履约能力'] = 7
        else:
            scores['cf_履约能力'] = 3

        # 16. 平台匹配度（募资维度）
        platform = RuleBasedExtractor._extract_platform(text)
        if platform and platform not in ('', 'zeczec'):
            scores['cf_平台匹配度'] = 8
        elif any(k in text_lower for k in ['硬件', '智能', '设备', '创新', '科技']):
            scores['cf_平台匹配度'] = 6
        else:
            scores['cf_平台匹配度'] = 5

        return scores


class FeasibilityAgent:
    """完整可行性分析智能体"""
    
    def __init__(self, base_dir: str = None, llm_provider: str = "auto"):
        if base_dir is None:
            base_dir = os.path.dirname(__file__)
        
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, 'data')
        self.templates_dir = os.path.join(base_dir, '..', 'templates')
        self.reports_dir = os.path.join(base_dir, '..', 'reports')
        
        for d in [self.data_dir, self.reports_dir]:
            if not os.path.exists(d):
                os.makedirs(d)
        
        # 初始化所有组件
        self.competitor_db = CompetitorDatabase(self.data_dir)
        self.competitor_analyzer = CompetitorAnalyzer(self.competitor_db)
        self.feasibility_analyzer = FeasibilityAnalyzer()
        self.crowdfunding_calculator = CrowdfundingCalculator()
        self.report_generator = FullReportGenerator(base_dir)
        self.html_generator = FullHTMLReportGenerator()
        self.llm_analyzer = LLMAnalyzer(llm_provider)
        
        # 初始化迭代引擎
        self.iteration_engine = AgentIterationEngine(base_dir)
        self.case_library = CaseLibraryGenerator(self.iteration_engine)
        
        # 加载项目资源
        self.real_cases = self._load_real_cases()
        self.scoring_model = self.report_generator.scoring_model
        self.growth_flywheel = self.report_generator.growth_flywheel
        self.metrics_framework = self.report_generator.metrics_framework
        self.tech_framework = self.report_generator.tech_framework
        self.timeline_framework = self.report_generator.timeline_framework
        self.exit_strategy = self.report_generator.exit_strategy
        self.category_checks = self.report_generator.category_checks
    
    def _load_real_cases(self) -> List[Dict]:
        """加载真实案例库"""
        cases_file = os.path.join(self.base_dir, 'case-db', 'real_crowdfunding_cases.json')
        if not os.path.exists(cases_file):
            return []
        
        try:
            with open(cases_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('data', [])
        except Exception as e:
            print(f"加载真实案例失败: {e}")
            return []
    
    def identify_category(self, product_info: Dict) -> str:
        """识别产品品类"""
        description = product_info.get('description', '') + ' ' + product_info.get('name', '')
        description = description.lower()
        
        # 增强规则：优先匹配明确的品类关键词
        # 注意：订阅制是很多品类共有的商业模式，不作为saas的判定依据
        if any(k in description for k in ['app', '应用', '软件', 'saas']):
            return 'saas'
        if any(k in description for k in ['播客', '内容', '文章', '视频', '课程', ' newsletter']):
            return 'content'
        if any(k in description for k in ['服务', '咨询', '培训', '代运营']):
            return 'service'
        if any(k in description for k in ['社群', '社区', '会员', '俱乐部']):
            return 'community'
        if any(k in description for k in ['平台', 'marketplace', '撮合', '连接']):
            return 'platform'
        if any(k in description for k in ['b2b', '企业', '商家', '批发', '供应链']):
            return 'b2b'
        
        # 回退到关键词打分系统
        keywords = {
            'saas': ['订阅', '云端', 'saas', '软件', 'app', '工具', 'crm', '协作'],
            'hardware': ['硬件', '实体', '3d打印', '机器人', '智能', '设备', '芯片', '传感器', 'ai硬件'],
            'service': ['服务', '咨询', '代运营', '培训', '1v1', '定制', '人力'],
            'content': ['内容', '社群', '陪伴', '情感', '娱乐', '粉丝', '会员', '创作者'],
            'b2b': ['企业', 'b2b', '采购', 'poc', '决策链', '集成', '部署'],
            'platform': ['平台', '双边', '网络效应', '供需', '匹配', '交易'],
        }
        
        scores = {}
        for cat, words in keywords.items():
            score = sum(1 for w in words if w in description)
            scores[cat] = score
        
        if max(scores.values()) == 0:
            return 'hardware'  # 默认硬件
        
        return max(scores, key=scores.get)
    
    def analyze_competitors(self, category: str = '', keyword: str = '') -> Dict:
        """竞品分析"""
        competitors = self.competitor_db.search_competitors(keyword=keyword, category=category)
        
        if not competitors and keyword:
            competitors = self.competitor_db.search_competitors(keyword=keyword)
        
        if not competitors:
            competitors = self.competitor_db.load_db().get('data', [])
        
        # 匹配真实案例
        real_case_matches = []
        keyword_lower = keyword.lower() if keyword else ''
        for case in self.real_cases:
            if (keyword_lower and keyword_lower in case.get('name', '').lower()) or \
               (keyword_lower and keyword_lower in case.get('description', '').lower()) or \
               (category and category in case.get('category', '')):
                real_case_matches.append(case)
        
        analysis = self.competitor_analyzer.analyze_by_category()
        
        return {
            'total_competitors': len(competitors),
            'competitors': competitors[:20],
            'category_analysis': analysis.get('category_analysis', {}),
            'real_cases': real_case_matches[:10],
            'all_real_cases': self.real_cases,
        }
    
    def calculate_financials(self, cost: float, target_amount: float, avg_pledge: float = 500,
                        desired_margin: float = 0.5, platform: str = 'zeczec') -> Dict:
        """财务计算"""
        pricing = self.crowdfunding_calculator.calculate_pricing(cost, desired_margin)
        revenue = self.crowdfunding_calculator.calculate_actual_revenue(target_amount, platform)
        backers = self.crowdfunding_calculator.calculate_backer_breakdown(target_amount, avg_pledge)
        
        break_even_units = 0
        if pricing.get('margin_at_retail', 0) > 0:
            fixed_cost = target_amount * 0.3
            break_even_units = int(fixed_cost / (pricing['retail_price'] * pricing['margin_at_retail'])) if pricing['retail_price'] > 0 else 0
        
        return {
            'pricing': pricing,
            'revenue': revenue,
            'backers_needed': backers,
            'break_even_units': break_even_units,
            'margin': int(desired_margin * 100),
            'platform_fees': {
                'total_fee_cny': revenue.get('platform_fee_cny', 0),
                'payment_fee_cny': revenue.get('payment_fee_cny', 0),
                'total_fee': revenue.get('total_fee', 0),
            }
        }
    
    def calculate_score(self, scores: Dict, category: str = 'hardware') -> Dict:
        """计算可行性评分"""
        weights = self.scoring_model.get('category_weights', {}).get(category, 
            self.scoring_model['category_weights']['hardware'])
        
        dimensions = self.scoring_model.get('dimensions', [])
        
        total_weight = 0
        total_score = 0
        dimension_scores = []
        
        for dim in dimensions:
            key = dim['key']
            name = dim['name']
            weight = weights.get(key, dim['weight'])
            
            user_score = scores.get(key, 50)
            
            weighted = user_score / 100 * weight
            
            total_weight += weight
            total_score += weighted
            
            dimension_scores.append({
                'name': name,
                'key': key,
                'score': user_score,
                'max_score': 100,
                'weight': weight,
                'weighted_score': round(weighted, 2),
                'comment': scores.get(f'{key}_comment', ''),
            })
        
        final_score = round(total_score, 2) if total_weight > 0 else 0
        
        # 确定评级
        grade = 'D'
        grade_info = {}
        for g, info in self.scoring_model['grade_levels'].items():
            if final_score >= info['min']:
                grade = g
                grade_info = info
                break
        
        strengths = [d['name'] for d in dimension_scores if d['score'] >= 70]
        weaknesses = [d['name'] for d in dimension_scores if d['score'] < 50]
        
        scores_dict = {d['name']: {'weight': d['weight'], 'score': d['score'], 'comment': d['comment']} for d in dimension_scores}
        
        return {
            'total_score': final_score,
            'total_weight': total_weight,
            'grade': grade,
            'rating': grade_info.get('label', '未评级'),
            'recommendation': grade_info.get('action', '待评估'),
            'dimension_scores': dimension_scores,
            'scores': scores_dict,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'category': category,
        }
    
    def find_similar_cases(self, product_info: Dict, top_n: int = 5) -> List[Dict]:
        """查找相似案例"""
        category = self.identify_category(product_info)
        keyword = product_info.get('name', '') + ' ' + product_info.get('description', '')
        
        similar = []
        for case in self.real_cases:
            score = 0
            if case.get('category') == category:
                score += 3
            for word in keyword.split():
                if word.lower() in case.get('name', '').lower() or \
                   word.lower() in case.get('description', '').lower():
                    score += 1
            if score > 0:
                case_copy = case.copy()
                case_copy['match_score'] = score
                similar.append(case_copy)
        
        similar.sort(key=lambda x: x.get('match_score', 0), reverse=True)
        return similar[:top_n]
    
    def generate_growth_flywheel_analysis(self, category: str) -> Dict:
        """生成增长飞轮分析"""
        flywheel = self.growth_flywheel['category_flywheels'].get(category,
            self.growth_flywheel['category_flywheels']['hardware'])
        
        return {
            'flywheel': flywheel,
            'growth_stages': self.growth_flywheel['growth_stages'],
        }
    
    def generate_metrics_framework(self, category: str) -> Dict:
        """生成数据指标框架"""
        north_star = self.metrics_framework['north_star'].get(category,
            self.metrics_framework['north_star']['hardware'])
        
        return {
            'north_star': north_star,
            'aarrr': self.metrics_framework['aarrr'],
        }
    
    def generate_tech_assessment(self, category: str) -> Dict:
        """生成技术架构评估"""
        return {
            'dimensions': self.tech_framework['dimensions'],
            'risk_levels': self.tech_framework['risk_levels'],
        }
    
    def generate_timeline(self) -> Dict:
        """生成时间规划"""
        return {
            'stages': self.timeline_framework['stages'],
        }
    
    def generate_exit_strategy(self) -> Dict:
        """生成退出策略"""
        return {
            'options': self.exit_strategy['options'],
            'stop_loss': self.exit_strategy['stop_loss'],
        }
    
    def generate_category_checks(self, category: str) -> List[str]:
        """生成品类特别检查项"""
        return self.category_checks.get(category, [])
    
    def _recommend_platform(self, category: str, product_info: Dict) -> Dict:
        """根据品类和产品信息推荐募资平台"""
        # 品类到平台推荐映射
        category_platforms = {
            'hardware': [
                {'name': 'Kickstarter', 'rating': 5, 'reason': '全球最大，适合硬件/创新产品出海', 'fee': '5%+3%', 'avg_amount': '$10万-$100万'},
                {'name': '嘖嘖', 'rating': 4, 'reason': '台湾最大众筹平台，适合中文市场', 'fee': '5%+3%', 'avg_amount': '¥500万-¥1500万'},
            ],
            'ai': [
                {'name': 'Kickstarter', 'rating': 5, 'reason': '全球最大，适合AI硬件出海', 'fee': '5%+3%', 'avg_amount': '$10万-$100万'},
                {'name': '嘖嘖', 'rating': 4, 'reason': '台湾最大众筹平台，适合中文市场', 'fee': '5%+3%', 'avg_amount': '¥500万-¥1500万'},
            ],
            'saas': [
                {'name': 'Kickstarter', 'rating': 5, 'reason': '全球最大，适合软件工具类', 'fee': '5%+3%', 'avg_amount': '$5万-$50万'},
                {'name': '摩点', 'rating': 3, 'reason': '中国大陆，适合软件工具', 'fee': '5%+3%', 'avg_amount': '¥100万-¥500万'},
            ],
            'content': [
                {'name': 'Patreon', 'rating': 5, 'reason': '最适合内容创作者持续募资', 'fee': '5%-12%', 'avg_amount': '$1千-$10万'},
                {'name': '嘖嘖', 'rating': 4, 'reason': '台湾最大，适合内容项目', 'fee': '5%+3%', 'avg_amount': '¥500万-¥1500万'},
                {'name': 'Kickstarter', 'rating': 4, 'reason': '全球最大，适合内容出海', 'fee': '5%+3%', 'avg_amount': '$5万-$50万'},
            ],
            'service': [
                {'name': '嘖嘖', 'rating': 5, 'reason': '台湾最大，适合服务类项目', 'fee': '5%+3%', 'avg_amount': '¥500万-¥1500万'},
                {'name': 'FlyingV', 'rating': 4, 'reason': '台湾本土，适合服务/设计', 'fee': '8%+3%', 'avg_amount': '¥200万-¥800万'},
            ],
            'community': [
                {'name': '嘖嘖', 'rating': 5, 'reason': '台湾最大，适合社群类项目', 'fee': '5%+3%', 'avg_amount': '¥500万-¥1500万'},
                {'name': 'Patreon', 'rating': 5, 'reason': '最适合社群持续运营', 'fee': '5%-12%', 'avg_amount': '$1千-$10万'},
            ],
            'platform': [
                {'name': 'Kickstarter', 'rating': 5, 'reason': '全球最大，适合平台类项目', 'fee': '5%+3%', 'avg_amount': '$10万-$100万'},
                {'name': 'Indiegogo', 'rating': 4, 'reason': '灵活审核，适合创新平台', 'fee': '5%+5%', 'avg_amount': '$5万-$50万'},
            ],
            'b2b': [
                {'name': 'Indiegogo', 'rating': 5, 'reason': '灵活审核，适合B2B创新产品', 'fee': '5%+5%', 'avg_amount': '$5万-$50万'},
                {'name': 'Kickstarter', 'rating': 4, 'reason': '全球最大，适合B2B硬件/工具', 'fee': '5%+3%', 'avg_amount': '$10万-$100万'},
            ],
        }

        # 根据产品描述关键词微调推荐（如目标用户在中国大陆，则提高摩点权重）
        desc = product_info.get('description', '') + product_info.get('target_users', '')
        target_users = product_info.get('target_users', '')

        platforms = category_platforms.get(category, category_platforms['hardware'])

        # 如果目标用户明确指向大陆，添加摩点
        if any(kw in desc for kw in ['大陆', '中国', '国内', 'bilibili', 'B站', 'ACG']):
            has_modian = any(p['name'] == '摩点' for p in platforms)
            if not has_modian:
                platforms.append({'name': '摩点', 'rating': 4, 'reason': '中国大陆，适合ACG/文创', 'fee': '5%+3%', 'avg_amount': '¥100万-¥500万'})

        recommended = platforms[0]['name'] if platforms else 'Kickstarter'

        return {
            'recommended': recommended,
            'platforms': platforms,
            'category': category,
        }
    
    def extract_product_info(self, raw_text: str) -> Dict:
        """提取产品信息（规则提取优先，LLM增强）"""
        import os
        
        # 1. 先进行规则提取（无论有无API都执行）
        rule_result = RuleBasedExtractor.extract(raw_text)
        
        # 2. 检查是否有可用的API密钥
        has_api_key = any([
            os.environ.get("OPENAI_API_KEY"),
            os.environ.get("DEEPSEEK_API_KEY"),
            os.environ.get("DASHSCOPE_API_KEY"),
            os.environ.get("ANTHROPIC_API_KEY"),
        ])
        
        if not has_api_key:
            # 无API时直接返回规则提取结果，跳过LLM调用
            return {"product_info": rule_result}
        
        # 3. 尝试使用LLM增强
        print("正在尝试使用大模型分析产品资料...")
        llm_result = self.llm_analyzer.analyze_from_raw(raw_text)
        
        if "error" in llm_result:
            print(f"大模型分析失败: {llm_result.get('error', '')}")
            print("使用规则提取结果完成分析")
            return {"product_info": rule_result}
        
        # 3. 合并LLM结果和规则结果（LLM优先）
        llm_product = llm_result.get('product_info', {})
        
        merged_product = rule_result.copy()
        
        # LLM结果优先覆盖规则结果（字符串字段）
        for key in ['name', 'description', 'category', 'target_users', 'value_proposition',
                    'business_model', 'platform']:
            if llm_product.get(key):
                merged_product[key] = llm_product[key]
        
        # 数值字段：LLM有值则覆盖
        for key in ['cost', 'target_amount', 'avg_pledge']:
            if llm_product.get(key) is not None:
                merged_product[key] = llm_product[key]
        
        # 列表字段合并（去重，LLM优先）
        for key in ['features', 'pain_points']:
            llm_list = llm_product.get(key, [])
            rule_list = rule_result.get(key, [])
            if llm_list:
                merged = []
                seen = set()
                for item in list(llm_list) + list(rule_list):
                    s = str(item).strip()
                    if s and s not in seen:
                        seen.add(s)
                        merged.append(item)
                merged_product[key] = merged
        
        # suggested_scores：LLM有则覆盖，否则保留规则评分
        if llm_product.get('suggested_scores'):
            merged_product['suggested_scores'] = llm_product['suggested_scores']
        
        # 组装返回结果
        result = {
            "product_info": merged_product,
        }
        
        if llm_result.get('intake'):
            result['intake'] = llm_result['intake']
        if llm_result.get('analysis'):
            result['analysis'] = llm_result['analysis']
        
        return result
    
    def run_full_analysis(self, product_info: Dict, scores: Dict = None) -> Dict:
        """运行完整分析"""
        if scores is None:
            scores = {}
        
        category = self.identify_category(product_info)
        
        # 竞品分析
        competitor_analysis = self.analyze_competitors(
            category=category,
            keyword=product_info.get('name', '')
        )
        
        # 财务分析
        financials = {}
        if product_info.get('cost') and product_info.get('target_amount'):
            try:
                cost = float(product_info['cost'])
                target = float(str(product_info['target_amount']).replace(',', '').replace('¥', '').replace('NT$', '').replace('$', ''))
                financials = self.calculate_financials(
                    cost=cost,
                    target_amount=target,
                    avg_pledge=product_info.get('avg_pledge', 500),
                    platform=product_info.get('platform', 'zeczec'),
                )
            except Exception as e:
                print(f"财务计算失败: {e}")
        
        # 如果没有提供评分，使用默认评分或从大模型获取
        if not scores and product_info.get('suggested_scores'):
            llm_scores = product_info['suggested_scores']
            scores = {}
            for dim in self.scoring_model['dimensions']:
                key = dim['key']
                name = dim['name']
                if name in llm_scores:
                    scores[key] = llm_scores[name] * 10
        
        if not scores:
            scores = {dim['key']: 50 for dim in self.scoring_model['dimensions']}
        
        # 计算评分
        score_result = self.calculate_score(scores, category)
        
        # 查找相似案例
        similar_cases = self.find_similar_cases(product_info)
        
        # 生成增长飞轮分析
        growth_flywheel = self.generate_growth_flywheel_analysis(category)
        
        # 生成数据指标框架
        metrics_framework = self.generate_metrics_framework(category)
        
        # 生成技术架构评估
        tech_assessment = self.generate_tech_assessment(category)
        
        # 生成时间规划
        timeline = self.generate_timeline()
        
        # 生成退出策略
        exit_strategy = self.generate_exit_strategy()
        
        # 生成品类检查项
        category_checks = self.generate_category_checks(category)
        
        # 募资平台推荐
        platform_recommendation = self._recommend_platform(category, product_info)
        
        # 组装完整报告
        report = {
            'generated_at': datetime.now().isoformat(),
            'product': product_info,
            'category': category,
            'competitor_analysis': competitor_analysis,
            'financial_analysis': financials,
            'scoring': score_result,
            'similar_cases': similar_cases,
            'growth_flywheel': growth_flywheel,
            'metrics_framework': metrics_framework,
            'tech_assessment': tech_assessment,
            'timeline': timeline,
            'exit_strategy': exit_strategy,
            'category_checks': category_checks,
            'crowdfunding': platform_recommendation,
            'strengths': score_result.get('strengths', []),
            'risks': score_result.get('weaknesses', []),
            'need_improve': score_result.get('weaknesses', []),
            'swot': {
                'strengths': [{'item': s, 'impact': '高', 'evidence': '中', 'suggestion': '保持'} for s in score_result.get('strengths', [])],
                'weaknesses': [{'item': w, 'impact': '高', 'evidence': '强', 'suggestion': '需要补强'} for w in score_result.get('weaknesses', [])],
                'opportunities': [{'item': 'AI市场增长', 'impact': '高', 'evidence': '强', 'suggestion': '借势切入'}],
                'threats': [{'item': '竞品跟进', 'impact': '高', 'evidence': '强', 'suggestion': '差异化定位'}],
            },
        }
        
        return report
    
    def generate_and_save_reports(self, report: Dict, product_name: str) -> Dict:
        """生成并保存报告"""
        safe_name = ''.join(c for c in product_name if c.isalnum() or c in ('-', '_', ' '))
        safe_name = safe_name.strip().replace(' ', '-')
        
        report_dir = os.path.join(self.reports_dir, safe_name)
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        
        # 保存JSON报告
        report_file = os.path.join(report_dir, 'full_analysis_report.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 生成完整Markdown报告
        md_content = self.report_generator.generate_full_report(report)
        md_file = os.path.join(report_dir, f'{safe_name}-完整可行性分析.md')
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        # 生成完整HTML报告
        html_content = self.html_generator.generate_full_html(report)
        html_file = os.path.join(report_dir, f'{safe_name}-完整可行性分析.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return {
            'json_report': report_file,
            'markdown_report': md_file,
            'html_report': html_file,
        }
    
    def record_iteration(self, report: Dict):
        """记录迭代历史"""
        iteration_data = {
            'project_name': report.get('product', {}).get('name', ''),
            'category': report.get('category', ''),
            'score': report.get('scoring', {}).get('total_score', 0),
            'outcome': report.get('scoring', {}).get('rating', ''),
            'issues': report.get('scoring', {}).get('weaknesses', []),
            'suggestions': ['需要补强关键短板'],
        }
        self.iteration_engine.record_iteration(iteration_data)
    
    def process_from_raw(self, raw_text: str) -> Dict:
        """从原始文字处理"""
        # 提取产品信息（规则+LLM）
        extraction_result = self.extract_product_info(raw_text)
        
        if not extraction_result or 'product_info' not in extraction_result:
            print("产品信息提取失败，使用基础分析")
            product_info = {
                'name': '未命名产品',
                'description': raw_text[:200],
                'category': 'hardware',
            }
        else:
            product_info = extraction_result['product_info']
        
        # 运行完整分析
        report = self.run_full_analysis(product_info)
        
        # 添加大模型分析结果
        if extraction_result.get('intake'):
            report['intake'] = extraction_result['intake']
        if extraction_result.get('analysis'):
            report['llm_analysis'] = extraction_result['analysis']
        
        # 生成并保存报告
        saved = self.generate_and_save_reports(report, product_info.get('name', '未命名产品'))
        report['saved_files'] = saved
        
        # 记录迭代
        self.record_iteration(report)
        
        return report


def main():
    print("=" * 60)
    print("产品可行性分析智能体 - 完整版")
    print("整合：增长飞轮、市场规模、财务模型、数据指标、技术架构、时间规划、退出策略")
    print("=" * 60)
    
    agent = FeasibilityAgent()
    
    # 测试产品
    test_product = {
        'name': 'AI智能陪伴机器人',
        'description': '一款基于AI技术的情感陪伴机器人，具备语音交互、表情识别、个性化定制等功能。用户可以通过语音与机器人交流，机器人能识别用户情绪并做出相应回应。支持自定义虚拟人物形象，包括动漫角色等。',
        'target_users': '独居老人、儿童、情感需求人群',
        'value_proposition': '24小时陪伴，情感交流，个性化服务',
        'platform': '啧啧',
        'target_amount': '500000',
        'cost': 300,
        'pain_points': '情感陪伴缺失，独居孤独，儿童陪伴需求',
        'suggested_scores': {
            '痛点强度': 8,
            '目标用户清晰度': 7,
            '竞争壁垒': 5,
            '产品可演示性': 8,
            '技术可行性': 6,
            '合规与信任': 7,
            '商业模式': 7,
            '市场推广': 6,
            '团队匹配度': 7,
            '证据完整度': 4,
        }
    }
    
    print("\n1. 运行完整分析...")
    report = agent.run_full_analysis(test_product)
    
    print(f"\n产品名称: {report['product'].get('name')}")
    print(f"识别品类: {report['category']}")
    print(f"可行性评分: {report['scoring']['total_score']}/100")
    print(f"评级: {report['scoring']['grade']} - {report['scoring']['rating']}")
    print(f"建议: {report['scoring']['recommendation']}")
    
    print(f"\n增长飞轮: {report['growth_flywheel']['flywheel']['name']}")
    print(f"北极星指标: {report['metrics_framework']['north_star']['metric']}")
    
    print(f"\n竞品数量: {report['competitor_analysis']['total_competitors']}")
    print(f"相似案例: {len(report['similar_cases'])}个")
    
    if report['financial_analysis']:
        print(f"\n建议零售价: {report['financial_analysis']['pricing']['retail_price']}元")
        print(f"毛利率: {report['financial_analysis']['margin']}%")
        print(f"需要支持者: {report['financial_analysis']['backers_needed']['total_backers']}人")
    
    print("\n2. 生成完整报告...")
    saved = agent.generate_and_save_reports(report, test_product['name'])
    print(f"JSON报告: {saved['json_report']}")
    print(f"Markdown报告: {saved['markdown_report']}")
    print(f"HTML报告: {saved['html_report']}")
    
    print("\n3. 记录迭代历史...")
    agent.record_iteration(report)
    
    print("\n" + "=" * 60)
    print("完整智能体整合完成！")
    print("=" * 60)
    print("\n已整合的资源：")
    print("  ✅ 增长飞轮模型（6品类）")
    print("  ✅ 市场规模估算（TAM/SAM/SOM）")
    print("  ✅ 财务模型分析（收入、成本、盈利）")
    print("  ✅ 数据指标框架（北极星、AARRR）")
    print("  ✅ 技术架构评估（5维度）")
    print("  ✅ 时间规划（5阶段）")
    print("  ✅ 退出策略与止损机制")
    print("  ✅ 品类特别检查项")
    print("  ✅ 迭代引擎（历史记录）")
    print("  ✅ 真实案例库（15个）")
    print("  ✅ 完整HTML报告（15章节）")
    
    print("\n使用方式：")
    print("  python feasibility_agent.py")
    print("  或在代码中调用 agent.process_from_raw(raw_text)")


if __name__ == '__main__':
    main()