#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import os
import time
import random
import re
from datetime import datetime
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import pandas as pd

class ZeczecCrawler:
    def __init__(self):
        self.base_url = 'https://www.zeczec.com'
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
        ]
        
        self.session = requests.Session()
        self._update_headers()
    
    def _update_headers(self):
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'https://www.zeczec.com/',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
        }
        self.session.headers.update(headers)
    
    def _random_delay(self, min_delay=3, max_delay=6):
        time.sleep(random.uniform(min_delay, max_delay))
    
    def _make_request(self, url, method='GET', params=None, data=None):
        try:
            self._random_delay()
            self._update_headers()
            
            response = self.session.request(
                method, url, 
                params=params, 
                data=data,
                timeout=30
            )
            
            response.raise_for_status()
            return response
        
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {url} - {str(e)}")
            return None
    
    def get_page_html(self, url: str) -> Optional[str]:
        response = self._make_request(url)
        if response:
            return response.text
        return None
    
    def extract_projects_from_html(self, html: str) -> List[Dict]:
        soup = BeautifulSoup(html, 'html.parser')
        projects = []
        
        script_tags = soup.find_all('script')
        for script in script_tags:
            if script.string and 'window.__INITIAL_STATE__' in script.string:
                try:
                    state_str = script.string.split('window.__INITIAL_STATE__ = ')[1].split(';')[0]
                    state = json.loads(state_str)
                    
                    if 'projects' in state:
                        if isinstance(state['projects'], dict):
                            for key, project in state['projects'].items():
                                if isinstance(project, dict):
                                    projects.append(project)
                        elif isinstance(state['projects'], list):
                            projects.extend(state['projects'])
                    
                    elif 'projectList' in state:
                        if isinstance(state['projectList'], list):
                            projects.extend(state['projectList'])
                    
                    elif 'data' in state:
                        if isinstance(state['data'], list):
                            projects.extend(state['data'])
                        elif isinstance(state['data'], dict) and 'projects' in state['data']:
                            projects.extend(state['data']['projects'])
                
                except Exception as e:
                    print(f"解析JSON失败: {e}")
        
        if not projects:
            project_elements = soup.find_all('div', class_=re.compile(r'project|Project'))
            for elem in project_elements[:20]:
                project = {}
                title_tag = elem.find('h1') or elem.find('h2') or elem.find('h3') or elem.find('h4')
                if title_tag:
                    project['title'] = title_tag.get_text(strip=True)
                
                link_tag = elem.find('a')
                if link_tag and 'href' in link_tag.attrs:
                    href = link_tag['href']
                    if href.startswith('/'):
                        project['url'] = self.base_url + href
                    else:
                        project['url'] = href
                
                projects.append(project)
        
        return projects
    
    def search_projects(self, keyword: str, page: int = 1) -> List[Dict]:
        url = f'{self.base_url}/projects/search'
        
        response = self._make_request(url, params={'q': keyword, 'page': page})
        if not response:
            return []
        
        return self.extract_projects_from_html(response.text)
    
    def get_category_projects(self, category: str, page: int = 1) -> List[Dict]:
        url = f'{self.base_url}/projects/category/{category}'
        
        response = self._make_request(url, params={'page': page})
        if not response:
            return []
        
        return self.extract_projects_from_html(response.text)
    
    def get_project_detail(self, project_url: str) -> Optional[Dict]:
        response = self._make_request(project_url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        detail = {'url': project_url}
        
        script_tags = soup.find_all('script')
        for script in script_tags:
            if script.string and ('window.__INITIAL_STATE__' in script.string or 'window.project' in script.string):
                try:
                    if 'window.__INITIAL_STATE__' in script.string:
                        state_str = script.string.split('window.__INITIAL_STATE__ = ')[1].split(';')[0]
                        state = json.loads(state_str)
                        
                        if 'project' in state:
                            detail.update(state['project'])
                        elif 'data' in state:
                            detail.update(state['data'])
                    
                    elif 'window.project' in script.string:
                        state_str = script.string.split('window.project = ')[1].split(';')[0]
                        project_data = json.loads(state_str)
                        detail.update(project_data)
                
                except Exception as e:
                    print(f"解析项目详情JSON失败: {e}")
        
        if 'title' not in detail:
            title_tag = soup.find('h1', class_=re.compile(r'title|name'))
            if title_tag:
                detail['title'] = title_tag.get_text(strip=True)
        
        if 'creator' not in detail:
            creator_tag = soup.find('span', class_=re.compile(r'creator|author'))
            if creator_tag:
                detail['creator'] = creator_tag.get_text(strip=True)
        
        return detail
    
    def crawl_ai_hardware_projects(self, max_pages: int = 3) -> List[Dict]:
        all_projects = []
        
        keywords = ['AI', '人工智能', '智能硬件', 'AI硬件']
        
        for keyword in keywords:
            print(f"\n搜索关键词: {keyword}")
            
            for page in range(1, max_pages + 1):
                print(f"正在搜索第 {page} 页...")
                projects = self.search_projects(keyword, page)
                
                if not projects:
                    break
                
                for project in projects:
                    project['search_keyword'] = keyword
                
                all_projects.extend(projects)
                print(f"第 {page} 页获取到 {len(projects)} 个项目")
        
        categories = ['technology', 'electronics']
        
        for category in categories:
            print(f"\n浏览类目: {category}")
            
            for page in range(1, max_pages + 1):
                print(f"正在浏览第 {page} 页...")
                projects = self.get_category_projects(category, page)
                
                if not projects:
                    break
                
                for project in projects:
                    if 'search_keyword' not in project:
                        project['search_keyword'] = f'category_{category}'
                
                all_projects.extend(projects)
                print(f"第 {page} 页获取到 {len(projects)} 个项目")
        
        unique_projects = []
        seen_urls = set()
        
        for p in all_projects:
            url = p.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_projects.append(p)
        
        return unique_projects

class DataProcessor:
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = os.path.join(os.path.dirname(__file__), data_dir)
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def save_to_json(self, data: List[Dict], filename: str):
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到: {filepath}")
    
    def save_to_excel(self, data: List[Dict], filename: str):
        filepath = os.path.join(self.data_dir, filename)
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False)
        print(f"数据已保存到: {filepath}")
    
    def load_from_json(self, filename: str) -> List[Dict]:
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            return []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def extract_numeric_value(self, value) -> float:
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
    
    def analyze_projects(self, projects: List[Dict]) -> Dict:
        if not projects:
            return {}
        
        df = pd.DataFrame(projects)
        
        analysis = {
            'total_projects': len(projects),
            'date_range': {
                'start': datetime.now().strftime('%Y-%m-%d'),
                'end': datetime.now().strftime('%Y-%m-%d')
            }
        }
        
        for col in df.columns:
            if 'amount' in col.lower() or 'price' in col.lower():
                df[f'{col}_num'] = df[col].apply(self.extract_numeric_value)
                analysis['amount_stats'] = {
                    'avg_amount': round(df[f'{col}_num'].mean(), 2),
                    'max_amount': round(df[f'{col}_num'].max(), 2),
                    'min_amount': round(df[f'{col}_num'].min(), 2),
                    'total_amount': round(df[f'{col}_num'].sum(), 2)
                }
            
            if 'backer' in col.lower() or 'backer' in col.lower():
                df[f'{col}_num'] = df[col].apply(self.extract_numeric_value)
                analysis['backers_stats'] = {
                    'avg_backers': round(df[f'{col}_num'].mean(), 2),
                    'max_backers': round(df[f'{col}_num'].max(), 2),
                    'min_backers': round(df[f'{col}_num'].min(), 2),
                    'total_backers': round(df[f'{col}_num'].sum(), 2)
                }
        
        if 'status' in df.columns:
            analysis['status_distribution'] = df['status'].value_counts().to_dict()
        
        if 'search_keyword' in df.columns:
            analysis['keyword_distribution'] = df['search_keyword'].value_counts().to_dict()
        
        analysis['sample_projects'] = projects[:5]
        
        return analysis

def main():
    crawler = ZeczecCrawler()
    processor = DataProcessor()
    
    print("=" * 60)
    print("啧啧平台AI硬件类目爬虫")
    print("=" * 60)
    
    print("\n开始抓取AI硬件相关项目...")
    projects = crawler.crawl_ai_hardware_projects(max_pages=2)
    
    if projects:
        print(f"共获取到 {len(projects)} 个项目")
        
        processor.save_to_json(projects, 'ai_hardware_projects_list.json')
        
        project_urls = []
        for p in projects:
            if isinstance(p, dict) and 'url' in p:
                project_urls.append(p['url'])
        
        project_urls = list(set(project_urls))[:10]
        
        if project_urls:
            print(f"\n开始获取项目详情（最多10个）...")
            details = []
            for url in project_urls:
                print(f"正在获取: {url}")
                detail = crawler.get_project_detail(url)
                if detail:
                    details.append(detail)
            
            if details:
                processor.save_to_json(details, 'ai_hardware_projects_detail.json')
                processor.save_to_excel(details, 'ai_hardware_projects_detail.xlsx')
                
                analysis = processor.analyze_projects(details)
                processor.save_to_json(analysis, 'ai_hardware_projects_analysis.json')
                
                print(f"\n分析结果:")
                print(json.dumps(analysis, ensure_ascii=False, indent=2))
        else:
            print("未能提取项目URL")
    else:
        print("未获取到项目数据")
    
    print("\n" + "=" * 60)
    print("爬取完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()