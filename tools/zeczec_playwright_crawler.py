#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import time
import random
import re
from datetime import datetime
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import pandas as pd

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


class PlaywrightCrawler:
    def __init__(self, headless: bool = True):
        self.base_url = 'https://www.zeczec.com'
        self.headless = headless
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def start(self):
        if not HAS_PLAYWRIGHT:
            raise ImportError("请先安装 playwright: pip install playwright")
        
        self._playwright = sync_playwright().start()
        
        # 优先使用系统 Edge 浏览器（Windows 自带），无需下载 Chromium
        browser_kwargs = {
            'headless': self.headless,
            'args': [
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox',
            ]
        }
        
        try:
            self._browser = self._playwright.chromium.launch(**browser_kwargs)
        except Exception:
            try:
                self._browser = self._playwright.chromium.launch(channel="msedge", **browser_kwargs)
                print("使用系统 Edge 浏览器")
            except Exception:
                try:
                    self._browser = self._playwright.chromium.launch(channel="chrome", **browser_kwargs)
                    print("使用系统 Chrome 浏览器")
                except Exception as e:
                    raise RuntimeError(
                        "无法启动浏览器。请确保已安装 Edge 或 Chrome，"
                        "或运行: python -m playwright install chromium"
                    ) from e
        self._context = self._browser.new_context(
            user_agent=random.choice(self.user_agents),
            viewport={'width': 1920, 'height': 1080},
            locale='zh-TW',
            timezone_id='Asia/Taipei',
        )
        self._context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.chrome = { runtime: {} };
        """)
        self._page = self._context.new_page()
    
    def close(self):
        if self._page:
            self._page.close()
        if self._context:
            self._context.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()
    
    def _random_delay(self, min_delay=2, max_delay=5):
        time.sleep(random.uniform(min_delay, max_delay))
    
    def _scroll_page(self, times=3):
        for i in range(times):
            self._page.evaluate(f'window.scrollTo(0, document.body.scrollHeight * {(i+1)/times})')
            time.sleep(random.uniform(0.5, 1.5))
        self._page.evaluate('window.scrollTo(0, 0)')
    
    def get_page_html(self, url: str, wait_selector: str = None, scroll: bool = True) -> Optional[str]:
        try:
            print(f"正在访问: {url}")
            self._page.goto(url, wait_until='domcontentloaded', timeout=30000)
            self._random_delay(2, 4)
            
            # 检测 Cloudflare 验证页面并等待
            title = self._page.title()
            if 'moment' in title.lower() or '安全检查' in title or 'verify' in title.lower():
                print("检测到安全验证页面，等待 8-15 秒...")
                self._random_delay(8, 15)
                title = self._page.title()
                if 'moment' in title.lower() or '安全检查' in title:
                    print("警告: 安全验证未通过，可能需要手动过验证或使用 data_manager.py 手动添加数据")
                    return None
            
            if wait_selector:
                try:
                    self._page.wait_for_selector(wait_selector, timeout=10000)
                except PlaywrightTimeout:
                    pass
            
            if scroll:
                self._scroll_page(3)
                self._random_delay(1, 2)
            
            html = self._page.content()
            return html
        except Exception as e:
            print(f"访问失败: {url} - {str(e)}")
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
                    
                    projects.extend(self._extract_projects_from_state(state))
                except Exception as e:
                    print(f"解析JSON失败: {e}")
        
        if not projects:
            projects = self._extract_projects_from_dom(soup)
        
        return projects
    
    def _extract_projects_from_state(self, state: Dict) -> List[Dict]:
        projects = []
        
        def find_projects(obj, key_path=''):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key in ('projects', 'projectList', 'items', 'data') and isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict) and ('title' in item or 'name' in item):
                                projects.append(item)
                    elif isinstance(value, (dict, list)):
                        find_projects(value, f'{key_path}.{key}')
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if isinstance(item, dict):
                        find_projects(item, f'{key_path}[{i}]')
        
        find_projects(state)
        return projects
    
    def _extract_projects_from_dom(self, soup: BeautifulSoup) -> List[Dict]:
        projects = []
        
        project_cards = soup.find_all(['div', 'article'], class_=re.compile(r'project|card|item', re.I))
        for card in project_cards[:30]:
            project = {}
            
            title_tag = card.find(['h1', 'h2', 'h3', 'h4', 'a'], class_=re.compile(r'title|name', re.I))
            if not title_tag:
                title_tag = card.find(['h1', 'h2', 'h3', 'h4'])
            if title_tag:
                project['title'] = title_tag.get_text(strip=True)
            
            link_tag = card.find('a', href=True)
            if link_tag:
                href = link_tag['href']
                if '/projects/' in href:
                    if href.startswith('/'):
                        project['url'] = self.base_url + href
                    else:
                        project['url'] = href
            
            amount_tag = card.find(string=re.compile(r'(募資|達成|NT\$|¥)'))
            if amount_tag:
                project['amount_text'] = amount_tag.strip()
            
            backer_tag = card.find(string=re.compile(r'(人|支持|backers)'))
            if backer_tag:
                project['backer_text'] = backer_tag.strip()
            
            if project.get('title'):
                projects.append(project)
        
        return projects
    
    def search_projects(self, keyword: str, page: int = 1) -> List[Dict]:
        url = f'{self.base_url}/projects/search?q={keyword}&page={page}'
        html = self.get_page_html(url)
        if not html:
            return []
        return self.extract_projects_from_html(html)
    
    def get_category_projects(self, category: str, page: int = 1) -> List[Dict]:
        url = f'{self.base_url}/projects/category/{category}?page={page}'
        html = self.get_page_html(url)
        if not html:
            return []
        return self.extract_projects_from_html(html)
    
    def get_project_detail(self, project_url: str) -> Optional[Dict]:
        html = self.get_page_html(project_url, scroll=True)
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        detail = {'url': project_url}
        
        script_tags = soup.find_all('script')
        for script in script_tags:
            if script.string and 'window.__INITIAL_STATE__' in script.string:
                try:
                    state_str = script.string.split('window.__INITIAL_STATE__ = ')[1].split(';')[0]
                    state = json.loads(state_str)
                    
                    if 'project' in state:
                        detail.update(state['project'])
                    elif 'data' in state and isinstance(state['data'], dict):
                        detail.update(state['data'])
                except Exception as e:
                    print(f"解析项目详情JSON失败: {e}")
        
        title_tag = soup.find('h1')
        if title_tag and 'title' not in detail:
            detail['title'] = title_tag.get_text(strip=True)
        
        return detail
    
    def crawl_by_keywords(self, keywords: List[str], max_pages: int = 3) -> List[Dict]:
        all_projects = []
        
        for keyword in keywords:
            print(f"\n搜索关键词: {keyword}")
            
            for page in range(1, max_pages + 1):
                print(f"第 {page} 页...")
                projects = self.search_projects(keyword, page)
                
                if not projects:
                    break
                
                for p in projects:
                    p['search_keyword'] = keyword
                
                all_projects.extend(projects)
                print(f"获取到 {len(projects)} 个项目")
                self._random_delay(2, 4)
        
        return self._deduplicate(all_projects)
    
    def crawl_by_categories(self, categories: List[str], max_pages: int = 3) -> List[Dict]:
        all_projects = []
        
        for category in categories:
            print(f"\n浏览类目: {category}")
            
            for page in range(1, max_pages + 1):
                print(f"第 {page} 页...")
                projects = self.get_category_projects(category, page)
                
                if not projects:
                    break
                
                for p in projects:
                    p['search_keyword'] = f'category_{category}'
                
                all_projects.extend(projects)
                print(f"获取到 {len(projects)} 个项目")
                self._random_delay(2, 4)
        
        return self._deduplicate(all_projects)
    
    def _deduplicate(self, projects: List[Dict]) -> List[Dict]:
        unique = []
        seen_urls = set()
        seen_titles = set()
        
        for p in projects:
            url = p.get('url', '')
            title = p.get('title', '')
            
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique.append(p)
            elif title and title not in seen_titles and not url:
                seen_titles.add(title)
                unique.append(p)
        
        return unique


def normalize_project(project: Dict) -> Dict:
    normalized = {
        'name': project.get('title') or project.get('name') or '',
        'description': project.get('description') or project.get('brief') or '',
        'category': project.get('category') or project.get('category_name') or '',
        'platform': '啧啧',
        'url': project.get('url') or project.get('project_url') or '',
    }
    
    amount = project.get('amount_raised') or project.get('raised_amount') or project.get('total_amount') or ''
    if not amount:
        for key in ['successAmount', 'currentAmount', 'totalFunding', 'amount']:
            if key in project:
                amount = project[key]
                break
    normalized['amount_raised'] = str(amount) if amount else ''
    
    target = project.get('target_amount') or project.get('funding_goal') or project.get('goal') or ''
    if not target:
        for key in ['targetAmount', 'goalAmount']:
            if key in project:
                target = project[key]
                break
    normalized['target_amount'] = str(target) if target else ''
    
    backers = project.get('backers') or project.get('backer_count') or project.get('total_backers') or ''
    if not backers:
        for key in ['backerCount', 'supporters']:
            if key in project:
                backers = project[key]
                break
    normalized['backers'] = str(backers) if backers else ''
    
    try:
        amt = float(re.sub(r'[^\d.]', '', str(amount))) if amount else 0
        tgt = float(re.sub(r'[^\d.]', '', str(target))) if target else 0
        if tgt > 0:
            normalized['success_rate'] = f"{round(amt/tgt*100)}%"
    except:
        pass
    
    normalized['status'] = project.get('status') or project.get('state') or ''
    normalized['launch_date'] = project.get('launch_date') or project.get('start_date') or ''
    normalized['delivery_date'] = project.get('delivery_date') or project.get('estimated_delivery') or ''
    normalized['price_range'] = project.get('price_range') or project.get('reward_price') or ''
    normalized['creator'] = project.get('creator') or project.get('owner') or project.get('team') or ''
    
    return normalized


def main():
    if not HAS_PLAYWRIGHT:
        print("错误: 未安装 playwright")
        print("请先运行: pip install playwright")
        print("然后运行: python -m playwright install chromium")
        return
    
    print("=" * 60)
    print("啧啧平台爬虫 (Playwright版)")
    print("=" * 60)
    
    with PlaywrightCrawler(headless=True) as crawler:
        print("\n开始抓取AI硬件相关项目...")
        
        keywords = ['AI', '智能硬件', '机器人', '人工智能']
        projects = crawler.crawl_by_keywords(keywords, max_pages=2)
        
        categories = ['technology', 'electronics', 'design']
        cat_projects = crawler.crawl_by_categories(categories, max_pages=2)
        projects.extend(cat_projects)
        
        projects = crawler._deduplicate(projects)
        
        print(f"\n共获取到 {len(projects)} 个项目")
        
        normalized = [normalize_project(p) for p in projects if p.get('title') or p.get('name')]
        print(f"其中有名称的项目: {len(normalized)} 个")
        
        if normalized:
            output_file = os.path.join(os.path.dirname(__file__), 'data', 'zeczec_real_projects.json')
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(normalized, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到: {output_file}")
            
            print("\n前5个项目:")
            for p in normalized[:5]:
                print(f"  - {p['name']}: {p.get('amount_raised', 'N/A')}")
        else:
            print("未能提取到项目数据")
    
    print("\n" + "=" * 60)
    print("爬取完成")
    print("=" * 60)


if __name__ == '__main__':
    main()
