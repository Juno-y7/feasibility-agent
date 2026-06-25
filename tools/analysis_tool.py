#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from datetime import datetime

class FeasibilityAnalyzer:
    def __init__(self):
        self.data = {}
    
    def load_project_data(self, file_path):
        """加载项目数据"""
        if file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            self.data = pd.read_excel(file_path).to_dict()
        elif file_path.endswith('.csv'):
            self.data = pd.read_csv(file_path).to_dict()
        return self.data
    
    def calculate_market_size(self, tam, sam_ratio=0.3, som_ratio=0.05, years=3):
        """计算市场规模"""
        sam = tam * sam_ratio
        som_year1 = sam * som_ratio
        som_year2 = som_year1 * 1.5
        som_year3 = som_year2 * 1.8
        
        return {
            'TAM': tam,
            'SAM': sam,
            'SOM_Year1': som_year1,
            'SOM_Year2': som_year2,
            'SOM_Year3': som_year3
        }
    
    def calculate_financial_model(self, revenue, costs, margin=0.6):
        """计算财务模型"""
        gross_profit = revenue * margin
        net_profit = gross_profit - costs
        
        return {
            'revenue': revenue,
            'gross_profit': gross_profit,
            'net_profit': net_profit,
            'gross_margin': margin,
            'net_margin': net_profit / revenue if revenue > 0 else 0
        }
    
    def calculate_crowdfunding_score(self, criteria):
        """计算募资可行性评分"""
        weights = {
            'product_clarity': 15,
            'visual_presentation': 15,
            'trust_evidence': 15,
            'market_demand': 15,
            'competitive_advantage': 10,
            'delivery_capability': 15,
            'pricing_strategy': 10,
            'promotion_preparation': 5
        }
        
        total_score = 0
        for key, weight in weights.items():
            score = criteria.get(key, 0)
            total_score += score * weight / 100
        
        return round(total_score, 2)
    
    def analyze_competitors(self, competitors):
        """分析竞品"""
        if not competitors:
            return None
        
        df = pd.DataFrame(competitors)
        
        analysis = {
            'total_competitors': len(df),
            'avg_price': df['price'].mean() if 'price' in df.columns else 0,
            'avg_rating': df['rating'].mean() if 'rating' in df.columns else 0,
            'features_summary': {}
        }
        
        if 'features' in df.columns:
            all_features = []
            for features in df['features']:
                if isinstance(features, list):
                    all_features.extend(features)
            feature_counts = pd.Series(all_features).value_counts()
            analysis['features_summary'] = feature_counts.head(10).to_dict()
        
        return analysis
    
    def generate_score_summary(self, scores):
        """生成评分摘要"""
        summary = {
            'total_score': scores.get('total', 0),
            'grade': self._get_grade(scores.get('total', 0)),
            'strengths': [],
            'weaknesses': []
        }
        
        for dimension, score in scores.items():
            if dimension != 'total':
                if score >= 8:
                    summary['strengths'].append(dimension)
                elif score < 5:
                    summary['weaknesses'].append(dimension)
        
        return summary
    
    def _get_grade(self, score):
        """获取评级"""
        if score >= 80:
            return 'A - 强烈推荐'
        elif score >= 65:
            return 'B - 建议补强后推荐'
        elif score >= 50:
            return 'C - 需要重新定位'
        else:
            return 'D - 暂不建议'
    
    def generate_report(self, output_file='feasibility_report.json'):
        """生成分析报告"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'market_analysis': self.data.get('market_analysis', {}),
            'financial_analysis': self.data.get('financial_analysis', {}),
            'competitor_analysis': self.data.get('competitor_analysis', {}),
            'score_summary': self.data.get('score_summary', {})
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report

class CrowdfundingCalculator:
    def __init__(self):
        self.platform_fees = {
            'zeczec': 0.05,
            'kickstarter': 0.05,
            'indiegogo': 0.05,
            'flyingv': 0.05
        }
        self.payment_fees = 0.03
    
    def calculate_actual_revenue(self, target_amount, platform='zeczec'):
        """计算实际收入"""
        platform_fee = self.platform_fees.get(platform, 0.05)
        total_fees = platform_fee + self.payment_fees
        actual_revenue = target_amount * (1 - total_fees)
        
        return {
            'target_amount': target_amount,
            'platform_fee': target_amount * platform_fee,
            'payment_fee': target_amount * self.payment_fees,
            'total_fees': target_amount * total_fees,
            'actual_revenue': actual_revenue
        }
    
    def calculate_pricing(self, cost, desired_margin=0.5, discount=0.3):
        """计算定价"""
        retail_price = cost / (1 - desired_margin)
        early_bird_price = retail_price * (1 - discount)
        
        return {
            'cost': cost,
            'retail_price': round(retail_price, 2),
            'early_bird_price': round(early_bird_price, 2),
            'discount': discount,
            'margin_at_retail': desired_margin,
            'margin_at_early_bird': (early_bird_price - cost) / early_bird_price if early_bird_price > 0 else 0
        }
    
    def calculate_backer_breakdown(self, target_amount, avg_pledge=500):
        """计算支持者数量"""
        num_backers = target_amount / avg_pledge
        daily_backers = num_backers / 30
        
        return {
            'target_amount': target_amount,
            'avg_pledge': avg_pledge,
            'total_backers': round(num_backers),
            'daily_backers': round(daily_backers, 2),
            'first_day_target': round(num_backers * 0.3)
        }

def main():
    analyzer = FeasibilityAnalyzer()
    calculator = CrowdfundingCalculator()
    
    print("=" * 60)
    print("产品可行性分析工具")
    print("=" * 60)
    
    print("\n1. 市场规模估算示例")
    market = analyzer.calculate_market_size(10000000)
    print(f"TAM: {market['TAM']:,}")
    print(f"SAM: {market['SAM']:,}")
    print(f"SOM(第1年): {market['SOM_Year1']:,}")
    print(f"SOM(第2年): {market['SOM_Year2']:,}")
    print(f"SOM(第3年): {market['SOM_Year3']:,}")
    
    print("\n2. 募资收入计算示例")
    revenue = calculator.calculate_actual_revenue(1000000, 'zeczec')
    print(f"目标金额: {revenue['target_amount']:,}")
    print(f"平台费用: {revenue['platform_fee']:,}")
    print(f"支付手续费: {revenue['payment_fee']:,}")
    print(f"实际收入: {revenue['actual_revenue']:,}")
    
    print("\n3. 定价计算示例")
    pricing = calculator.calculate_pricing(200, 0.5, 0.3)
    print(f"成本: {pricing['cost']}")
    print(f"零售价: {pricing['retail_price']}")
    print(f"早鸟价: {pricing['early_bird_price']}")
    print(f"早鸟毛利率: {pricing['margin_at_early_bird']:.2%}")
    
    print("\n4. 支持者估算示例")
    backers = calculator.calculate_backer_breakdown(500000, 800)
    print(f"目标金额: {backers['target_amount']:,}")
    print(f"平均支持金额: {backers['avg_pledge']}")
    print(f"需要支持者: {backers['total_backers']}人")
    print(f"日均支持者: {backers['daily_backers']}人")
    print(f"首日目标: {backers['first_day_target']}人")
    
    print("\n" + "=" * 60)
    print("工具使用完成")
    print("=" * 60)

if __name__ == '__main__':
    main()