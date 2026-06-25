#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd
import numpy as np

class CompetitorDatabase:
    def __init__(self, db_dir: str = 'data'):
        self.db_dir = os.path.join(os.path.dirname(__file__), db_dir)
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)
        
        self.competitors_file = os.path.join(self.db_dir, 'competitors.json')
        self.analysis_file = os.path.join(self.db_dir, 'competitor_analysis.json')
        
        if not os.path.exists(self.competitors_file):
            self._create_initial_data()
    
    def _create_initial_data(self):
        sample_data = {
            "description": "啧啧平台AI硬件类目竞品数据库",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "categories": ["AI硬件", "智能穿戴", "智能家居", "机器人", "AI配件"],
            "data": []
        }
        self.save_db(sample_data)
    
    def save_db(self, data: Dict):
        with open(self.competitors_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_db(self) -> Dict:
        if not os.path.exists(self.competitors_file):
            self._create_initial_data()
        
        with open(self.competitors_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def add_competitor(self, competitor: Dict):
        db = self.load_db()
        
        competitor['id'] = len(db['data']) + 1
        competitor['added_at'] = datetime.now().isoformat()
        
        db['data'].append(competitor)
        db['updated_at'] = datetime.now().isoformat()
        
        self.save_db(db)
        print(f"已添加竞品: {competitor.get('name', '未知')}")
    
    def add_competitors_batch(self, competitors: List[Dict]):
        db = self.load_db()
        
        for competitor in competitors:
            competitor['id'] = len(db['data']) + 1
            competitor['added_at'] = datetime.now().isoformat()
            db['data'].append(competitor)
        
        db['updated_at'] = datetime.now().isoformat()
        self.save_db(db)
        
        print(f"批量添加完成，共添加 {len(competitors)} 个竞品")
    
    def search_competitors(self, keyword: str = '', category: str = '') -> List[Dict]:
        db = self.load_db()
        results = db['data']
        
        if keyword:
            keyword = keyword.lower()
            results = [
                c for c in results 
                if keyword in str(c.get('name', '')).lower() 
                or keyword in str(c.get('description', '')).lower()
                or keyword in str(c.get('category', '')).lower()
            ]
        
        if category:
            results = [c for c in results if c.get('category') == category]
        
        return results
    
    def get_competitor_by_id(self, competitor_id: int) -> Optional[Dict]:
        db = self.load_db()
        for c in db['data']:
            if c.get('id') == competitor_id:
                return c
        return None
    
    def update_competitor(self, competitor_id: int, updates: Dict):
        db = self.load_db()
        
        for c in db['data']:
            if c.get('id') == competitor_id:
                c.update(updates)
                c['updated_at'] = datetime.now().isoformat()
                db['updated_at'] = datetime.now().isoformat()
                self.save_db(db)
                print(f"已更新竞品 ID {competitor_id}")
                return
        
        print(f"未找到竞品 ID {competitor_id}")
    
    def delete_competitor(self, competitor_id: int):
        db = self.load_db()
        
        original_count = len(db['data'])
        db['data'] = [c for c in db['data'] if c.get('id') != competitor_id]
        
        if len(db['data']) < original_count:
            db['updated_at'] = datetime.now().isoformat()
            self.save_db(db)
            print(f"已删除竞品 ID {competitor_id}")
        else:
            print(f"未找到竞品 ID {competitor_id}")
    
    def export_to_excel(self, filename: str = 'competitors_export.xlsx'):
        db = self.load_db()
        df = pd.DataFrame(db['data'])
        
        filepath = os.path.join(self.db_dir, filename)
        df.to_excel(filepath, index=False)
        print(f"数据已导出到: {filepath}")
    
    def import_from_excel(self, filepath: str):
        df = pd.read_excel(filepath)
        competitors = df.to_dict('records')
        
        self.add_competitors_batch(competitors)
        print(f"从 {filepath} 导入了 {len(competitors)} 个竞品")

class CompetitorAnalyzer:
    def __init__(self, db: CompetitorDatabase):
        self.db = db
        self.analysis_file = os.path.join(db.db_dir, 'competitor_analysis.json')
    
    def extract_numeric(self, value) -> float:
        if value is None:
            return 0.0
        
        if isinstance(value, (int, float)):
            return float(value)
        
        value_str = str(value).strip()
        num_str = re.sub(r'[^\d.]', '', value_str)
        
        try:
            return float(num_str) if num_str else 0.0
        except ValueError:
            return 0.0
    
    def analyze_by_category(self) -> Dict:
        db = self.db.load_db()
        df = pd.DataFrame(db['data'])
        
        if df.empty:
            return {"error": "数据库为空"}
        
        analysis = {
            "total_competitors": len(df),
            "analysis_date": datetime.now().strftime('%Y-%m-%d'),
            "category_analysis": {}
        }
        
        if 'category' in df.columns:
            categories = df['category'].unique()
            
            for category in categories:
                cat_df = df[df['category'] == category]
                cat_analysis = self._analyze_category(cat_df, category)
                analysis['category_analysis'][category] = cat_analysis
        
        analysis['overall_trends'] = self._analyze_overall_trends(df)
        
        return analysis
    
    def _analyze_category(self, df: pd.DataFrame, category: str) -> Dict:
        df = df.copy()
        analysis = {
            "category": category,
            "total_projects": len(df),
            "projects": []
        }
        
        if 'amount_raised' in df.columns:
            df['amount_raised_num'] = df['amount_raised'].apply(self.extract_numeric)
            analysis['amount_stats'] = {
                "avg_amount": round(df['amount_raised_num'].mean(), 2),
                "max_amount": round(df['amount_raised_num'].max(), 2),
                "min_amount": round(df['amount_raised_num'].min(), 2),
                "total_amount": round(df['amount_raised_num'].sum(), 2)
            }
        
        if 'backers' in df.columns:
            df['backers_num'] = df['backers'].apply(self.extract_numeric)
            analysis['backers_stats'] = {
                "avg_backers": round(df['backers_num'].mean(), 2),
                "max_backers": round(df['backers_num'].max(), 2),
                "min_backers": round(df['backers_num'].min(), 2),
                "total_backers": round(df['backers_num'].sum(), 2)
            }
        
        if 'success_rate' in df.columns:
            df['success_rate_num'] = df['success_rate'].apply(self.extract_numeric)
            analysis['success_rate_stats'] = {
                "avg_success_rate": round(df['success_rate_num'].mean(), 2),
                "max_success_rate": round(df['success_rate_num'].max(), 2),
                "min_success_rate": round(df['success_rate_num'].min(), 2)
            }
        
        for _, row in df.iterrows():
            project = {
                "id": row.get('id', ''),
                "name": row.get('name', ''),
                "amount_raised": row.get('amount_raised', ''),
                "backers": row.get('backers', ''),
                "success_rate": row.get('success_rate', ''),
                "status": row.get('status', ''),
                "url": row.get('url', '')
            }
            analysis['projects'].append(project)
        
        return analysis
    
    def _analyze_overall_trends(self, df: pd.DataFrame) -> Dict:
        trends = {}
        
        if 'launch_date' in df.columns:
            df['launch_date'] = pd.to_datetime(df['launch_date'], errors='coerce')
            df['month'] = df['launch_date'].dt.to_period('M')
            
            monthly_counts = df['month'].value_counts().sort_index()
            trends['monthly_projects'] = {str(k): int(v) for k, v in monthly_counts.items()}
        
        if 'amount_raised' in df.columns:
            df['amount_raised_num'] = df['amount_raised'].apply(self.extract_numeric)
            
            price_bins = [0, 50000, 100000, 500000, 1000000, float('inf')]
            price_labels = ['0-5万', '5-10万', '10-50万', '50-100万', '100万+']
            df['price_range'] = pd.cut(df['amount_raised_num'], bins=price_bins, labels=price_labels)
            
            price_distribution = df['price_range'].value_counts()
            trends['price_distribution'] = price_distribution.to_dict()
        
        if 'backers' in df.columns:
            df['backers_num'] = df['backers'].apply(self.extract_numeric)
            
            backer_bins = [0, 100, 500, 1000, 5000, float('inf')]
            backer_labels = ['0-100', '100-500', '500-1000', '1000-5000', '5000+']
            df['backer_range'] = pd.cut(df['backers_num'], bins=backer_bins, labels=backer_labels)
            
            backer_distribution = df['backer_range'].value_counts()
            trends['backer_distribution'] = backer_distribution.to_dict()
        
        return trends
    
    def generate_comparison_report(self, target_product: Dict) -> Dict:
        db = self.db.load_db()
        df = pd.DataFrame(db['data'])
        
        if df.empty:
            return {"error": "数据库为空，无法生成对比报告"}
        
        report = {
            "target_product": target_product,
            "comparison_date": datetime.now().strftime('%Y-%m-%d'),
            "similar_projects": [],
            "benchmark_metrics": {},
            "competitive_position": {}
        }
        
        target_category = target_product.get('category', '')
        if target_category:
            similar_df = df[df['category'] == target_category]
        else:
            similar_df = df
        
        if 'amount_raised' in similar_df.columns:
            similar_df['amount_raised_num'] = similar_df['amount_raised'].apply(self.extract_numeric)
            report['benchmark_metrics']['amount'] = {
                "target_amount": self.extract_numeric(target_product.get('amount_raised', 0)),
                "avg_competitor_amount": round(similar_df['amount_raised_num'].mean(), 2),
                "median_competitor_amount": round(similar_df['amount_raised_num'].median(), 2),
                "top_25_percent": round(similar_df['amount_raised_num'].quantile(0.75), 2),
                "bottom_25_percent": round(similar_df['amount_raised_num'].quantile(0.25), 2)
            }
        
        if 'backers' in similar_df.columns:
            similar_df['backers_num'] = similar_df['backers'].apply(self.extract_numeric)
            report['benchmark_metrics']['backers'] = {
                "target_backers": self.extract_numeric(target_product.get('backers', 0)),
                "avg_competitor_backers": round(similar_df['backers_num'].mean(), 2),
                "median_competitor_backers": round(similar_df['backers_num'].median(), 2),
                "top_25_percent": round(similar_df['backers_num'].quantile(0.75), 2),
                "bottom_25_percent": round(similar_df['backers_num'].quantile(0.25), 2)
            }
        
        for _, row in similar_df.head(10).iterrows():
            project = {
                "name": row.get('name', ''),
                "amount_raised": row.get('amount_raised', ''),
                "backers": row.get('backers', ''),
                "success_rate": row.get('success_rate', ''),
                "status": row.get('status', ''),
                "url": row.get('url', ''),
                "launch_date": row.get('launch_date', '')
            }
            report['similar_projects'].append(project)
        
        report['competitive_position']['total_competitors'] = len(similar_df)
        report['competitive_position']['category'] = target_category
        
        return report
    
    def save_analysis(self, analysis: Dict):
        with open(self.analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        print(f"分析结果已保存到: {self.analysis_file}")

def generate_sample_data():
    sample_competitors = [
        {
            "name": "AI智能音箱 Pro",
            "category": "AI硬件",
            "description": "搭载大语言模型的智能音箱，支持多轮对话",
            "platform": "啧啧",
            "amount_raised": "¥1,200,000",
            "target_amount": "¥500,000",
            "backers": "2,856",
            "success_rate": "240%",
            "status": "已成功",
            "launch_date": "2024-03-15",
            "delivery_date": "2024-09-30",
            "price_range": "¥899-¥1,299",
            "url": "https://www.zeczec.com/projects/ai-speaker-pro"
        },
        {
            "name": "AI绘画板 Master",
            "category": "AI硬件",
            "description": "AI辅助绘画板，实时生成绘画建议",
            "platform": "啧啧",
            "amount_raised": "¥850,000",
            "target_amount": "¥300,000",
            "backers": "1,623",
            "success_rate": "283%",
            "status": "已成功",
            "launch_date": "2024-04-20",
            "delivery_date": "2024-10-15",
            "price_range": "¥1,599-¥2,499",
            "url": "https://www.zeczec.com/projects/ai-drawing-board"
        },
        {
            "name": "AI翻译耳机 Air",
            "category": "智能穿戴",
            "description": "实时AI翻译耳机，支持40+语言",
            "platform": "啧啧",
            "amount_raised": "¥2,100,000",
            "target_amount": "¥800,000",
            "backers": "4,321",
            "success_rate": "262%",
            "status": "已成功",
            "launch_date": "2024-02-10",
            "delivery_date": "2024-08-20",
            "price_range": "¥1,299-¥1,999",
            "url": "https://www.zeczec.com/projects/ai-translate-earbuds"
        },
        {
            "name": "AI智能摄像头 Home",
            "category": "智能家居",
            "description": "AI人形检测、行为识别的智能安防摄像头",
            "platform": "啧啧",
            "amount_raised": "¥680,000",
            "target_amount": "¥200,000",
            "backers": "1,890",
            "success_rate": "340%",
            "status": "已成功",
            "launch_date": "2024-05-05",
            "delivery_date": "2024-11-01",
            "price_range": "¥599-¥899",
            "url": "https://www.zeczec.com/projects/ai-camera-home"
        },
        {
            "name": "AI机械臂 Mini",
            "category": "机器人",
            "description": "桌面级AI机械臂，支持编程和语音控制",
            "platform": "啧啧",
            "amount_raised": "¥3,500,000",
            "target_amount": "¥1,500,000",
            "backers": "3,124",
            "success_rate": "233%",
            "status": "进行中",
            "launch_date": "2024-06-01",
            "delivery_date": "2025-01-15",
            "price_range": "¥2,999-¥4,999",
            "url": "https://www.zeczec.com/projects/ai-robot-arm"
        },
        {
            "name": "AI手写板 Note",
            "category": "AI配件",
            "description": "AI笔记整理手写板，自动识别并整理笔记",
            "platform": "啧啧",
            "amount_raised": "¥420,000",
            "target_amount": "¥150,000",
            "backers": "987",
            "success_rate": "280%",
            "status": "已成功",
            "launch_date": "2024-04-15",
            "delivery_date": "2024-10-30",
            "price_range": "¥499-¥799",
            "url": "https://www.zeczec.com/projects/ai-note-pad"
        },
        {
            "name": "AI智能台灯",
            "category": "智能家居",
            "description": "AI调光台灯，根据环境自动调节亮度",
            "platform": "啧啧",
            "amount_raised": "¥350,000",
            "target_amount": "¥100,000",
            "backers": "1,234",
            "success_rate": "350%",
            "status": "已成功",
            "launch_date": "2024-03-20",
            "delivery_date": "2024-09-15",
            "price_range": "¥299-¥499",
            "url": "https://www.zeczec.com/projects/ai-lamp"
        },
        {
            "name": "AI语音助手 Cube",
            "category": "AI硬件",
            "description": "便携AI语音助手，支持离线使用",
            "platform": "啧啧",
            "amount_raised": "¥560,000",
            "target_amount": "¥200,000",
            "backers": "2,156",
            "success_rate": "280%",
            "status": "已成功",
            "launch_date": "2024-05-10",
            "delivery_date": "2024-11-30",
            "price_range": "¥399-¥599",
            "url": "https://www.zeczec.com/projects/ai-voice-cube"
        },
        {
            "name": "AI运动手表 Fit",
            "category": "智能穿戴",
            "description": "AI健康监测运动手表，实时分析运动数据",
            "platform": "啧啧",
            "amount_raised": "¥1,800,000",
            "target_amount": "¥600,000",
            "backers": "3,678",
            "success_rate": "300%",
            "status": "已成功",
            "launch_date": "2024-01-25",
            "delivery_date": "2024-07-30",
            "price_range": "¥1,199-¥1,799",
            "url": "https://www.zeczec.com/projects/ai-fit-watch"
        },
        {
            "name": "AI陪伴机器人",
            "category": "机器人",
            "description": "面向儿童的AI陪伴机器人，支持教育内容",
            "platform": "啧啧",
            "amount_raised": "¥2,400,000",
            "target_amount": "¥1,000,000",
            "backers": "2,890",
            "success_rate": "240%",
            "status": "进行中",
            "launch_date": "2024-06-15",
            "delivery_date": "2025-02-01",
            "price_range": "¥1,999-¥2,999",
            "url": "https://www.zeczec.com/projects/ai-companion-robot"
        }
    ]
    return sample_competitors

def main():
    db = CompetitorDatabase()
    analyzer = CompetitorAnalyzer(db)
    
    print("=" * 60)
    print("啧啧平台AI硬件竞品分析系统")
    print("=" * 60)
    
    print("\n1. 初始化样本数据...")
    sample_data = generate_sample_data()
    
    current_db = db.load_db()
    if len(current_db['data']) == 0:
        db.add_competitors_batch(sample_data)
        print("已添加10个AI硬件样本数据")
    else:
        print(f"数据库已有 {len(current_db['data'])} 条数据")
    
    print("\n2. 按类目分析...")
    analysis = analyzer.analyze_by_category()
    analyzer.save_analysis(analysis)
    
    print(json.dumps(analysis, ensure_ascii=True, indent=2))
    
    print("\n3. 生成对比报告...")
    target_product = {
        "name": "我的AI硬件产品",
        "category": "AI硬件",
        "amount_raised": "¥1,000,000",
        "backers": "2,000"
    }
    
    comparison_report = analyzer.generate_comparison_report(target_product)
    print(json.dumps(comparison_report, ensure_ascii=True, indent=2))
    
    print("\n4. 导出数据到Excel...")
    db.export_to_excel()
    
    print("\n" + "=" * 60)
    print("分析完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()