#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
from datetime import datetime
from typing import List, Dict, Optional
try:
    import pandas as pd
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

class AgentIterationEngine:
    def __init__(self, base_dir: str = '.'):
        self.base_dir = base_dir
        self.iteration_dir = os.path.join(base_dir, 'iterations')
        self.case_db_dir = os.path.join(base_dir, 'case-db')
        self.vector_db_dir = os.path.join(base_dir, 'vector-db')
        
        for dir_path in [self.iteration_dir, self.case_db_dir, self.vector_db_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        
        self.iteration_file = os.path.join(self.iteration_dir, 'iteration_history.json')
        self.case_db_file = os.path.join(self.case_db_dir, 'cases.json')
        self.vector_index_file = os.path.join(self.vector_db_dir, 'vector_index.npy')
        self.vector_meta_file = os.path.join(self.vector_db_dir, 'vector_meta.json')
        
        if HAS_SKLEARN:
            self.vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(1, 2))
        else:
            self.vectorizer = None
        
        if not os.path.exists(self.iteration_file):
            self._init_iteration_file()
        
        if not os.path.exists(self.case_db_file):
            self._init_case_db()
    
    def _init_iteration_file(self):
        initial_data = {
            "description": "智能体迭代历史记录",
            "created_at": datetime.now().isoformat(),
            "iterations": []
        }
        with open(self.iteration_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=2)
    
    def _init_case_db(self):
        initial_data = {
            "description": "案例库",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "cases": []
        }
        with open(self.case_db_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=2)
    
    def record_iteration(self, iteration_data: Dict):
        db = self._load_json(self.iteration_file)
        iteration_data['id'] = len(db['iterations']) + 1
        iteration_data['timestamp'] = datetime.now().isoformat()
        db['iterations'].append(iteration_data)
        
        with open(self.iteration_file, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        
        print(f"迭代记录已保存，ID: {iteration_data['id']}")
    
    def analyze_iterations(self) -> Dict:
        db = self._load_json(self.iteration_file)
        iterations = db['iterations']
        
        if not iterations:
            return {"error": "暂无迭代记录"}
        
        analysis = {
            "total_iterations": len(iterations),
            "first_iteration": iterations[0]['timestamp'],
            "last_iteration": iterations[-1]['timestamp'],
            "trends": {},
            "suggestions": []
        }
        
        scores = []
        categories = []
        outcomes = []
        
        for it in iterations:
            if 'score' in it:
                scores.append(it['score'])
            if 'category' in it:
                categories.append(it['category'])
            if 'outcome' in it:
                outcomes.append(it['outcome'])
        
        if scores:
            analysis['score_trends'] = {
                "avg_score": round(sum(scores) / len(scores), 2),
                "max_score": max(scores),
                "min_score": min(scores),
                "score_list": scores
            }
        
        if categories:
            category_counts = {}
            for cat in categories:
                category_counts[cat] = category_counts.get(cat, 0) + 1
            analysis['category_distribution'] = category_counts
        
        if outcomes:
            outcome_counts = {}
            for out in outcomes:
                outcome_counts[out] = outcome_counts.get(out, 0) + 1
            analysis['outcome_distribution'] = outcome_counts
        
        analysis['suggestions'] = self._generate_suggestions(iterations)
        
        return analysis
    
    def _generate_suggestions(self, iterations: List[Dict]) -> List[str]:
        suggestions = []
        
        scores = [it['score'] for it in iterations if 'score' in it]
        if len(scores) >= 3:
            recent_scores = scores[-3:]
            if all(s < 60 for s in recent_scores):
                suggestions.append("近期分析评分较低，建议优化评分标准或分析方法")
            if recent_scores[-1] > recent_scores[0]:
                suggestions.append("评分呈上升趋势，当前分析方法有效")
        
        categories = [it['category'] for it in iterations if 'category' in it]
        if categories:
            most_common = max(set(categories), key=categories.count)
            suggestions.append(f"分析最多的品类是{most_common}，建议丰富该品类的案例库")
        
        return suggestions
    
    def _load_json(self, filepath: str) -> Dict:
        if not os.path.exists(filepath):
            return {}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def optimize_prompt(self, feedback: str = '') -> Dict:
        iterations = self._load_json(self.iteration_file).get('iterations', [])
        
        optimization = {
            "optimization_id": len(iterations) + 1,
            "timestamp": datetime.now().isoformat(),
            "feedback": feedback,
            "improvements": [],
            "updated_prompt_elements": []
        }
        
        if feedback:
            optimization['improvements'].append(f"基于用户反馈: {feedback}")
        
        if iterations:
            recent_iterations = iterations[-3:] if len(iterations) >= 3 else iterations
            
            for it in recent_iterations:
                if 'issues' in it:
                    for issue in it['issues']:
                        optimization['improvements'].append(f"修复问题: {issue}")
                
                if 'suggestions' in it:
                    for suggestion in it['suggestions']:
                        optimization['improvements'].append(f"实现建议: {suggestion}")
        
        optimization['updated_prompt_elements'] = self._generate_prompt_updates(optimization['improvements'])
        
        return optimization
    
    def _generate_prompt_updates(self, improvements: List[str]) -> List[Dict]:
        updates = []
        
        if any("评分" in imp for imp in improvements):
            updates.append({
                "section": "评分标准",
                "update": "优化评分权重，增加竞品对比维度的权重"
            })
        
        if any("案例" in imp for imp in improvements):
            updates.append({
                "section": "案例库",
                "update": "扩充案例库，增加更多品类的成功/失败案例"
            })
        
        if any("竞品" in imp for imp in improvements):
            updates.append({
                "section": "竞品分析",
                "update": "增加竞品数据库的查询频率和对比维度"
            })
        
        if any("风险" in imp for imp in improvements):
            updates.append({
                "section": "风险评估",
                "update": "增加更详细的风险分类和应对策略"
            })
        
        return updates

class CaseLibraryGenerator:
    def __init__(self, agent_engine: AgentIterationEngine):
        self.engine = agent_engine
        self._load_case_db()
    
    def _load_case_db(self):
        self.case_db = self.engine._load_json(self.engine.case_db_file)
    
    def generate_case_from_project(self, project_data: Dict, analysis_result: Dict) -> Dict:
        case = {
            "id": len(self.case_db.get('cases', [])) + 1,
            "created_at": datetime.now().isoformat(),
            "name": project_data.get('name', ''),
            "category": project_data.get('category', ''),
            "description": project_data.get('description', ''),
            "platform": project_data.get('platform', '啧啧'),
            "key_metrics": {
                "amount_raised": project_data.get('amount_raised', ''),
                "target_amount": project_data.get('target_amount', ''),
                "backers": project_data.get('backers', ''),
                "success_rate": project_data.get('success_rate', '')
            },
            "analysis": {
                "score": analysis_result.get('score', ''),
                "swot": analysis_result.get('swot', {}),
                "opportunities": analysis_result.get('opportunities', []),
                "risks": analysis_result.get('risks', []),
                "conclusion": analysis_result.get('conclusion', '')
            },
            "lessons_learned": self._extract_lessons(project_data, analysis_result),
            "similar_cases": []
        }
        
        return case
    
    def _extract_lessons(self, project_data: Dict, analysis_result: Dict) -> List[str]:
        lessons = []
        
        success_rate = self._parse_percentage(project_data.get('success_rate', '0%'))
        if success_rate >= 200:
            lessons.append("高达成率通常意味着产品定位精准，痛点明确")
        elif success_rate >= 100:
            lessons.append("达成目标说明产品有市场需求，但竞争可能激烈")
        elif success_rate < 100:
            lessons.append("未达成目标可能存在产品定位、定价或推广问题")
        
        score = analysis_result.get('score', 0)
        if score >= 80:
            lessons.append("高评分产品通常在多个维度都表现优秀")
        elif score >= 60:
            lessons.append("中等评分产品需要补强关键短板")
        else:
            lessons.append("低评分产品需要重新评估定位或方向")
        
        swot = analysis_result.get('swot', {})
        if swot.get('strengths'):
            lessons.append(f"核心优势: {', '.join(swot['strengths'][:2])}")
        if swot.get('weaknesses'):
            lessons.append(f"主要短板: {', '.join(swot['weaknesses'][:2])}")
        
        return lessons
    
    def _parse_percentage(self, value: str) -> float:
        num_str = re.sub(r'[^\d.]', '', str(value))
        try:
            return float(num_str)
        except ValueError:
            return 0.0
    
    def add_case(self, case: Dict):
        self._load_case_db()
        self.case_db['cases'].append(case)
        self.case_db['updated_at'] = datetime.now().isoformat()
        
        with open(self.engine.case_db_file, 'w', encoding='utf-8') as f:
            json.dump(self.case_db, f, ensure_ascii=False, indent=2)
        
        print(f"案例已添加: {case['name']}")
    
    def add_cases_batch(self, cases: List[Dict]):
        self._load_case_db()
        self.case_db['cases'].extend(cases)
        self.case_db['updated_at'] = datetime.now().isoformat()
        
        with open(self.engine.case_db_file, 'w', encoding='utf-8') as f:
            json.dump(self.case_db, f, ensure_ascii=False, indent=2)
        
        print(f"批量添加完成，共添加 {len(cases)} 个案例")
    
    def search_cases(self, keyword: str = '', category: str = '') -> List[Dict]:
        cases = self.case_db.get('cases', [])
        
        if keyword:
            keyword = keyword.lower()
            cases = [
                c for c in cases
                if keyword in str(c.get('name', '')).lower()
                or keyword in str(c.get('description', '')).lower()
                or keyword in str(c.get('category', '')).lower()
            ]
        
        if category:
            cases = [c for c in cases if c.get('category') == category]
        
        return cases
    
    def generate_case_summary(self, case: Dict) -> str:
        summary = f"""案例: {case['name']}
品类: {case['category']}
平台: {case['platform']}

核心指标:
- 募集金额: {case['key_metrics'].get('amount_raised', '')}
- 目标金额: {case['key_metrics'].get('target_amount', '')}
- 达成率: {case['key_metrics'].get('success_rate', '')}
- 支持者: {case['key_metrics'].get('backers', '')}

分析结论: {case['analysis'].get('conclusion', '')}

经验教训:
"""
        for lesson in case.get('lessons_learned', []):
            summary += f"- {lesson}\n"
        
        return summary

class VectorCaseRetriever:
    def __init__(self, case_generator: CaseLibraryGenerator):
        self.case_generator = case_generator
        if HAS_SKLEARN:
            self.vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(1, 2))
        else:
            self.vectorizer = None
        self.vectors = None
        self.cases = []
        self.fit_vectors()
    
    def fit_vectors(self):
        self.case_generator._load_case_db()
        self.cases = self.case_generator.case_db.get('cases', [])
        
        if not self.cases:
            if HAS_SKLEARN:
                self.vectors = np.array([])
            else:
                self.vectors = []
            return
        
        if HAS_SKLEARN:
            texts = self._extract_texts(self.cases)
            self.vectors = self.vectorizer.fit_transform(texts).toarray()
        else:
            self.vectors = self.cases
    
    def _extract_texts(self, cases: List[Dict]) -> List[str]:
        texts = []
        for case in cases:
            text = f"{case.get('name', '')} {case.get('category', '')} {case.get('description', '')}"
            texts.append(text)
        return texts
    
    def _simple_keyword_match(self, query_text: str, case: Dict) -> float:
        """无sklearn时的简单关键词匹配"""
        query_words = set(query_text.lower().split())
        case_text = f"{case.get('name', '')} {case.get('category', '')} {case.get('description', '')}".lower()
        case_words = set(case_text.split())
        
        if not query_words:
            return 0.0
        
        overlap = len(query_words & case_words)
        return overlap / len(query_words)
    
    def find_similar_cases(self, query_text: str, top_n: int = 5) -> List[Dict]:
        if not self.cases:
            return []
        
        if HAS_SKLEARN and self.vectors is not None and len(self.vectors) > 0:
            query_vector = self.vectorizer.transform([query_text]).toarray()
            similarities = cosine_similarity(query_vector, self.vectors)[0]
            sorted_indices = similarities.argsort()[::-1][:top_n]
            
            results = []
            for idx in sorted_indices:
                case = self.cases[idx].copy()
                case['similarity_score'] = round(float(similarities[idx]), 4)
                results.append(case)
            return results
        else:
            # Fallback: 简单关键词匹配
            scored_cases = []
            for case in self.cases:
                score = self._simple_keyword_match(query_text, case)
                case_copy = case.copy()
                case_copy['similarity_score'] = round(score, 4)
                scored_cases.append(case_copy)
            
            scored_cases.sort(key=lambda x: x['similarity_score'], reverse=True)
            return scored_cases[:top_n]
    
    def update_index(self):
        self.cases = self.case_generator.case_db.get('cases', [])
        self.fit_vectors()
        print("向量索引已更新")

def generate_sample_cases():
    sample_cases = [
        {
            "name": "AI智能音箱 Pro",
            "category": "AI硬件",
            "description": "搭载大语言模型的智能音箱，支持多轮对话和智能家居控制",
            "platform": "啧啧",
            "key_metrics": {
                "amount_raised": "¥1,200,000",
                "target_amount": "¥500,000",
                "backers": "2,856",
                "success_rate": "240%"
            },
            "analysis": {
                "score": 85,
                "swot": {
                    "strengths": ["产品成熟度高", "品牌认知度强"],
                    "weaknesses": ["竞争激烈", "技术壁垒一般"],
                    "opportunities": ["智能家居生态整合", "语音交互趋势"],
                    "threats": ["大厂竞争", "技术迭代快"]
                },
                "opportunities": ["智能家居市场增长", "AI交互需求提升"],
                "risks": ["供应链风险", "技术过时风险"],
                "conclusion": "产品市场需求明确，但需持续创新保持竞争力"
            },
            "lessons_learned": [
                "高达成率意味着产品定位精准",
                "AI硬件需要持续的技术迭代",
                "智能家居生态整合是重要卖点"
            ]
        },
        {
            "name": "AI翻译耳机 Air",
            "category": "智能穿戴",
            "description": "实时AI翻译耳机，支持40+语言，低延迟通话翻译",
            "platform": "啧啧",
            "key_metrics": {
                "amount_raised": "¥2,100,000",
                "target_amount": "¥800,000",
                "backers": "4,321",
                "success_rate": "262%"
            },
            "analysis": {
                "score": 90,
                "swot": {
                    "strengths": ["刚需痛点", "技术领先"],
                    "weaknesses": ["价格较高", "续航挑战"],
                    "opportunities": ["跨境出行增长", "远程办公需求"],
                    "threats": ["手机厂商竞争", "翻译服务免费化"]
                },
                "opportunities": ["全球化趋势", "远程沟通需求"],
                "risks": ["技术替代风险", "竞品降价"],
                "conclusion": "刚需产品，市场潜力大，需控制成本"
            },
            "lessons_learned": [
                "刚需痛点产品更容易获得高支持",
                "技术领先是核心竞争优势",
                "定价策略需要平衡利润和销量"
            ]
        },
        {
            "name": "AI绘画板 Master",
            "category": "AI硬件",
            "description": "AI辅助绘画板，实时生成绘画建议，提升创作效率",
            "platform": "啧啧",
            "key_metrics": {
                "amount_raised": "¥850,000",
                "target_amount": "¥300,000",
                "backers": "1,623",
                "success_rate": "283%"
            },
            "analysis": {
                "score": 78,
                "swot": {
                    "strengths": ["垂直细分", "创意人群精准"],
                    "weaknesses": ["市场规模较小", "用户教育成本高"],
                    "opportunities": ["创作者经济增长", "AI创作工具普及"],
                    "threats": ["软件替代", "硬件成本高"]
                },
                "opportunities": ["创作者经济", "AI工具趋势"],
                "risks": ["市场天花板", "技术替代"],
                "conclusion": "垂直市场机会，需精准定位目标用户"
            },
            "lessons_learned": [
                "垂直细分市场可以避开激烈竞争",
                "创作者人群付费意愿强",
                "需要降低用户教育成本"
            ]
        }
    ]
    return sample_cases

def main():
    engine = AgentIterationEngine(os.path.dirname(__file__))
    case_generator = CaseLibraryGenerator(engine)
    
    print("=" * 60)
    print("智能体迭代引擎")
    print("=" * 60)
    
    print("\n1. 初始化案例库...")
    case_generator._load_case_db()
    if len(case_generator.case_db.get('cases', [])) == 0:
        sample_cases = generate_sample_cases()
        case_generator.add_cases_batch(sample_cases)
        print("已添加3个样本案例")
    
    print("\n2. 测试案例检索...")
    retriever = VectorCaseRetriever(case_generator)
    similar_cases = retriever.find_similar_cases("AI智能硬件 语音助手", top_n=3)
    print(f"找到 {len(similar_cases)} 个相似案例:")
    for case in similar_cases:
        print(f"- {case['name']} (相似度: {case['similarity_score']})")
    
    print("\n3. 测试迭代记录...")
    iteration_data = {
        "project_name": "测试项目",
        "category": "AI硬件",
        "score": 82,
        "outcome": "建议推进",
        "issues": ["竞品分析不够深入"],
        "suggestions": ["增加竞品数据库数据"]
    }
    engine.record_iteration(iteration_data)
    print("迭代记录已保存")
    
    print("\n4. 分析迭代历史...")
    iteration_analysis = engine.analyze_iterations()
    print(json.dumps(iteration_analysis, ensure_ascii=True, indent=2))
    
    print("\n5. 优化提示词...")
    optimization = engine.optimize_prompt("用户反馈竞品分析不够深入")
    print(json.dumps(optimization, ensure_ascii=True, indent=2))
    
    print("\n" + "=" * 60)
    print("智能体迭代引擎测试完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()