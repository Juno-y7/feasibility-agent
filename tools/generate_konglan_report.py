#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成空蓝数据AI分身产品的完整可行性分析报告
输出：Markdown / HTML / PDF 三种格式
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from premium_report_generator import PremiumReportGenerator, PremiumHTMLGenerator, generate_pdf_from_html


def main():
    print("=" * 60)
    print("空蓝数据 AI分身 - 可行性分析报告生成")
    print("=" * 60)
    
    # 定义空蓝AI分身的产品信息
    konglan_product = {
        'name': '空蓝数据 AI分身',
        'description': '通过3D打印模型接入AI技术，支持真人形象复刻及虚拟人物定制（动漫角色、游戏角色等）。产品可作为亲情陪伴装置，让不在身边的子女以更具存在感的方式参与老人日常生活，同时满足年轻群体对虚拟偶像的实体化情感寄托需求。',
        'target_users': '独居老人、异地子女、二次元爱好者、情感陪伴需求人群',
        'value_proposition': '24小时AI陪伴 + 真人形象复刻 + 情感互动交流',
        'pain_points': '异地亲情陪伴缺失、独居老人孤独、虚拟偶像实体化需求、情感寄托需求',
        'platform': '啧啧',
        'target_amount': '1,000,000',
        'cost': 400,
        'mvp_features': '语音交互、情感识别、真人形象3D打印、AI对话',
        'tech_stack': 'AI大模型 + 3D打印 + 语音交互 + 云端服务',
        'dev_cycle': '4-6个月',
        'team_size': '5-8人核心团队',
    }
    
    # 构造完整分析数据
    report_data = {
        'product': konglan_product,
        'category': 'hardware',
        'scoring': {
            'total_score': 71,
            'grade': 'B',
            'rating': '建议补强后继续',
            'recommendation': '方向可行，但必须先补强2-3个关键短板，尤其是真实交互Demo、数据授权和用户反馈验证',
            'strengths': [
                '痛点真实明确（亲情陪伴+情感寄托）',
                '产品形态创新（3D打印+AI实体化）',
                '目标用户群体清晰',
            ],
            'weaknesses': [
                '竞争壁垒不足（技术门槛低）',
                '证据完整度低（缺用户验证）',
                '数据合规与隐私风险',
                '供应链与量产能力待验证',
            ],
            'dimension_scores': [
                {'name': '痛点强度', 'key': 'pain_point', 'score': 80, 'weight': 15, 'weighted_score': 12.0, 'comment': '亲情陪伴和情感寄托是真实刚需'},
                {'name': '目标用户清晰度', 'key': 'user_clarity', 'score': 75, 'weight': 10, 'weighted_score': 7.5, 'comment': '独居老人和二次元群体明确'},
                {'name': '竞争壁垒', 'key': 'moat', 'score': 45, 'weight': 8, 'weighted_score': 3.6, 'comment': '技术门槛低，易被复制'},
                {'name': '产品可演示性', 'key': 'demo_ability', 'score': 70, 'weight': 10, 'weighted_score': 7.0, 'comment': '3D打印实物+AI交互有视觉冲击力'},
                {'name': '技术/生产可行性', 'key': 'tech_feasibility', 'score': 60, 'weight': 15, 'weighted_score': 9.0, 'comment': 'AI和3D打印技术成熟，但供应链整合难度大'},
                {'name': '合规与信任', 'key': 'compliance', 'score': 55, 'weight': 10, 'weighted_score': 5.5, 'comment': '涉及真人形象和隐私数据，合规风险较高'},
                {'name': '商业模式', 'key': 'business_model', 'score': 70, 'weight': 12, 'weighted_score': 8.4, 'comment': '硬件销售+后续服务，定价合理'},
                {'name': '市场推广可行性', 'key': 'marketing', 'score': 65, 'weight': 8, 'weighted_score': 5.2, 'comment': '有话题性和传播点，但获客成本不确定'},
                {'name': '团队匹配度', 'key': 'team_fit', 'score': 65, 'weight': 7, 'weighted_score': 4.55, 'comment': '需验证团队在硬件和AI方面的综合能力'},
                {'name': '证据完整度', 'key': 'evidence', 'score': 40, 'weight': 5, 'weighted_score': 2.0, 'comment': '缺用户访谈、原型验证、预注册等证据'},
            ],
        },
        'competitor_analysis': {
            'real_cases': [
                {
                    'name': 'Eilik AI陪伴机器人',
                    'platform': 'Kickstarter',
                    'link': 'https://www.kickstarter.com/projects/energize-lab/eilik-a-little-companion-bot-with-endless-fun',
                    'amount_raised': '$780,000 (HK$6,064,614)',
                    'backers': '4,738',
                    'success_rate': '1555%',
                    'launch_date': '2021-11-09',
                    'price_range': '$129-$169',
                    'success_factors': [
                        '丰富表情系统(12+情绪状态)',
                        '触摸互动+情感反馈',
                        '社交功能(多机互动)',
                        '可更换外壳个性化',
                        '已有300K+用户基础',
                    ],
                    'key_insight': '情感连接是核心,不追求功能性而是陪伴感',
                },
                {
                    'name': 'Eiliko便携AI伴侣',
                    'platform': 'Kickstarter',
                    'link': 'https://store.energizelab.com/pages/eiliko-kickstarter',
                    'amount_raised': '$602,335',
                    'backers': '4,707',
                    'success_rate': '6000%',
                    'launch_date': '2025-08-05',
                    'price_range': '早鸟价$59(零售$99)',
                    'success_factors': [
                        '89克超轻便携设计',
                        'AI对话功能终身免费',
                        '社交配对"灵魂伴侣"概念',
                        '可挂在背包/钥匙链',
                        '41%早鸟折扣激励',
                    ],
                    'key_insight': '便携性+终身免费订阅是差异化优势',
                },
                {
                    'name': 'Rokid Glasses AI&AR眼镜',
                    'platform': 'Kickstarter + Makuake + 嘖嘖',
                    'link': 'https://www.kickstarter.com/projects/rokid/rokid-glasses',
                    'amount_raised': 'Kickstarter $3.61M + Makuake ¥6367万 + 嘖嘖 ¥2600万',
                    'backers': 'Kickstarter 5800+ / Makuake 7400+ / 嘖嘖 1300+',
                    'success_rate': 'Kickstarter 867%',
                    'launch_date': '2025-10',
                    'price_range': '嘖嘖 NT$19,888-$24,999',
                    'success_factors': [
                        'AR显示+实时翻译(89种语言)',
                        '49克超轻量化设计',
                        '多平台成功策略',
                        'CES创新奖+iF设计奖背书',
                        'ChatGPT+Gemini双AI模型',
                    ],
                    'key_insight': '多平台策略+技术领先+品牌背书',
                },
                {
                    'name': 'Ropet/Kamomo AI宠物',
                    'platform': 'Kickstarter + Makuake',
                    'link': 'https://www.kickstarter.com/projects/ropet/ropet-ai-pet',
                    'amount_raised': 'Kickstarter $400K + Makuake ¥5000万',
                    'backers': '女性用户占比70%',
                    'success_rate': '150倍超目标',
                    'launch_date': '2024-12',
                    'price_range': '$129-$169',
                    'success_factors': [
                        '39°C体温模拟真实感',
                        '不说话设计(表情+声音反馈)',
                        '宠物养成系统',
                        '女性用户精准定位',
                        '情感陪伴而非功能性',
                    ],
                    'key_insight': '不说话的反直觉设计反而更真实',
                },
                {
                    'name': 'Looi Robot AI伴侣',
                    'platform': 'Kickstarter + Indiegogo',
                    'link': 'https://www.kickstarter.com/projects/looi/looi-robot',
                    'amount_raised': '$648K (Kickstarter $518K + Indiegogo $130K)',
                    'backers': '4000+',
                    'success_rate': '100倍超目标',
                    'launch_date': '2024-02',
                    'price_range': '$119-$169',
                    'success_factors': [
                        'ChatGPT集成',
                        '仿生行为系统',
                        '情感陪伴+实用性功能',
                        '马斯克点赞背书',
                        '以手机为中心的交互',
                    ],
                    'key_insight': 'ChatGPT集成+名人背书+实用功能组合',
                },
                {
                    'name': 'PLAUD NotePin AI录音器',
                    'platform': 'Kickstarter + Makuake + 嘖嘖',
                    'link': 'https://www.kickstarter.com/projects/plaud/plaud-notepin',
                    'amount_raised': 'Kickstarter $1.1M + Makuake ¥270M + 嘖嘖 ¥2400万',
                    'backers': '日本活跃用户超美国',
                    'success_rate': '嘖嘖亚军',
                    'launch_date': '2023-10',
                    'price_range': '生产力工具定价',
                    'success_factors': [
                        '会议转录+AI摘要',
                        '日本本土化"AI秘书"定位',
                        '适配"議事録"文化',
                        '日本国民级明星代言',
                        '线下门店280→400家扩张',
                    ],
                    'key_insight': '本土化适配+明星代言+线下渠道',
                },
            ],
            'success_patterns': {
                'emotional_connection': {
                    'title': '情感连接是核心',
                    'examples': ['Eilik表情系统', 'Ropet体温+不说话', 'Eiliko社交配对'],
                    'insight': '不追求功能性,而是陪伴感和真实感',
                },
                'portability': {
                    'title': '便携性与日常陪伴',
                    'examples': ['Eiliko 89克', 'Rokid 49克', 'Looi手机交互'],
                    'insight': '轻量化设计让产品融入日常生活',
                },
                'differentiation': {
                    'title': '差异化功能',
                    'examples': ['Rokid AR显示+翻译', 'PLAUD会议转录', 'Looi ChatGPT'],
                    'insight': '必须有不可替代的核心功能',
                },
                'multi_platform': {
                    'title': '多平台策略',
                    'examples': ['Rokid三平台', 'Eilik三平台', 'PLAUD三平台'],
                    'insight': 'Kickstarter验证+Makuake爆发+嘖嘖本土化',
                },
                'localization': {
                    'title': '本土化适配',
                    'examples': ['PLAUD日本"AI秘书"', 'Ropet女性用户70%'],
                    'insight': '深入理解目标市场文化',
                },
                'pricing_strategy': {
                    'title': '价格策略',
                    'examples': ['Eiliko 41%早鸟折扣', 'Rokid嘖嘖优惠'],
                    'insight': '早鸟折扣激励+合理定价',
                },
                'brand_trust': {
                    'title': '品牌与信任',
                    'examples': ['Eilik 300K用户', 'Rokid CES奖', 'PLAUD明星代言'],
                    'insight': '已有用户基础+奖项背书+明星代言',
                },
                'continuous_iteration': {
                    'title': '持续迭代',
                    'examples': ['Eilik→Eiliko', 'Rokid单眼→双眼', 'PLAUD Note→NotePin S'],
                    'insight': '软件更新+硬件迭代保持竞争力',
                },
            },
            'competitors': [],
        },
        'similar_cases': [],
        'financial_analysis': {
            'pricing': {'retail_price': 999},
            'margin': 60,
            'backers_needed': {'total_backers': '1,000'},
            'revenue': {'actual_revenue_cny': 890000},
            'break_even_units': 600,
        },
        'swot': {
            'strengths': [
                {'item': '痛点真实（亲情陪伴+情感寄托）', 'impact': '高', 'evidence': '中', 'suggestion': '保持并深化'},
                {'item': '产品形态创新（3D打印+AI实体）', 'impact': '高', 'evidence': '中', 'suggestion': '强化差异化'},
                {'item': '目标用户清晰', 'impact': '中', 'evidence': '中', 'suggestion': '持续聚焦'},
            ],
            'weaknesses': [
                {'item': '竞争壁垒不足', 'impact': '高', 'evidence': '强', 'suggestion': '需要补强'},
                {'item': '数据合规风险', 'impact': '高', 'evidence': '中', 'suggestion': '需要补强'},
                {'item': '证据不足（缺用户验证）', 'impact': '高', 'evidence': '强', 'suggestion': '立即验证'},
            ],
            'opportunities': [
                {'item': 'AI硬件市场快速增长', 'impact': '高', 'evidence': '强', 'suggestion': '借势切入'},
                {'item': '情感科技赛道上升期', 'impact': '高', 'evidence': '中', 'suggestion': '提前布局'},
                {'item': '募资平台对AI品类友好', 'impact': '中', 'evidence': '强', 'suggestion': '把握窗口期'},
            ],
            'threats': [
                {'item': '竞品跟进速度快', 'impact': '高', 'evidence': '强', 'suggestion': '快速迭代差异化'},
                {'item': '供应链不确定性', 'impact': '高', 'evidence': '中', 'suggestion': '多供应商备选'},
                {'item': '监管政策变化', 'impact': '中', 'evidence': '低', 'suggestion': '合规前置设计'},
            ],
        },
        'growth_flywheel': {},
        'metrics_framework': {},
        'tech_assessment': {},
        'timeline': {},
        'exit_strategy': {},
        'category_checks': [],
        'strengths': ['痛点真实明确', '产品形态创新', '目标用户清晰'],
        'risks': ['竞争壁垒不足', '数据合规风险', '证据完整度低'],
        'need_improve': ['竞争壁垒不足', '数据合规与隐私', '用户反馈证据', '供应链验证', '团队能力验证'],
        'user_insights': {
            'score': 6.5,
            'personas': [
                {'type': '亲情陪伴型', 'characteristics': '异地工作子女，父母独居', 'needs': '让父母有陪伴，缓解思念', 'willingness': '高，为亲情付费'},
                {'type': '情感寄托型', 'characteristics': '二次元爱好者，独居青年', 'needs': '虚拟偶像实体化，情感陪伴', 'willingness': '中高，为爱好付费'},
                {'type': '尝鲜科技型', 'characteristics': '科技爱好者，早期adopters', 'needs': '体验新技术，收藏展示', 'willingness': '中，为新奇付费'},
                {'type': '礼品送礼型', 'characteristics': '节日送礼，企业礼品', 'needs': '独特有心意的礼物', 'willingness': '中，为场景付费'},
            ],
            'journey': [
                {'stage': '认知期', 'behavior': '刷到KOL推荐/朋友圈分享', 'touchpoints': '社交媒体、众筹平台', 'pain_points': '不知道这是什么，有什么用', 'opportunities': '30秒Demo视频讲清价值'},
                {'stage': '兴趣期', 'behavior': '点击进入详情页，看视频', 'touchpoints': '众筹页面、官网', 'pain_points': '功能是否真的好用？质量靠谱吗？', 'opportunities': '真实用户评价、详细演示'},
                {'stage': '决策期', 'behavior': '对比竞品，看评测', 'touchpoints': '测评视频、社群', 'pain_points': '价格是否合理？会不会踩坑？', 'opportunities': '早鸟优惠、限时限量、背书'},
                {'stage': '购买期', 'behavior': '下单支持', 'touchpoints': '众筹平台', 'pain_points': '档位选择困难、担心交付', 'opportunities': '清晰档位、发货承诺'},
                {'stage': '使用期', 'behavior': '开箱、设置、日常使用', 'touchpoints': '产品本身、APP', 'pain_points': '设置复杂、功能不及预期', 'opportunities': '引导设计、持续迭代'},
                {'stage': '推荐期', 'behavior': '分享给朋友、社群晒单', 'touchpoints': '社交媒体、社群', 'pain_points': '没什么可晒的、分享动力不足', 'opportunities': '社交功能、晒单奖励'},
            ],
            'use_cases': [
                {'title': '早晨唤醒', 'description': 'AI分身用熟悉的声音叫醒，播报天气和新闻'},
                {'title': '日常陪伴', 'description': '老人在家可以和"子女"说说话，缓解孤独'},
                {'title': '睡前故事', 'description': '小朋友听AI分身讲故事，陪伴入睡'},
                {'title': '节日问候', 'description': '不在身边也能以"实体"形式送上祝福'},
                {'title': '粉丝应援', 'description': '偶像/虚拟角色的实体化周边，情感寄托'},
            ],
            'summary': [
                '场景想象空间大，但需要验证真实使用频率',
                '情感价值明确，但功能价值待验证',
                '建议：先做5-10位种子用户深度访谈，录制真实使用场景',
            ],
        },
        'product_definition': {
            'score': 6,
            'moscow_features': [
                {'priority': 'must', 'module': '基础对话', 'feature': '语音对话、基础问答', 'description': '产品核心功能，没有就不是AI分身'},
                {'priority': 'must', 'module': '形象定制', 'feature': '照片建模、3D打印', 'description': '核心差异化，用户付费的主要理由'},
                {'priority': 'must', 'module': 'App控制', 'feature': '连接配置、基础设置', 'description': '硬件产品必备配套'},
                {'priority': 'should', 'module': '情感表达', 'feature': '表情、动作、语气变化', 'description': '增强陪伴感，提升用户粘性'},
                {'priority': 'should', 'module': '记忆功能', 'feature': '记住用户喜好、对话历史', 'description': '让AI更懂用户'},
                {'priority': 'should', 'module': '故事/资讯', 'feature': '讲故事、播报新闻天气', 'description': '增加使用场景和频率'},
                {'priority': 'could', 'module': '多角色切换', 'feature': '支持多个形象切换', 'description': '增加可玩性和复购'},
                {'priority': 'could', 'module': '社交分享', 'feature': '生成对话截图/视频分享', 'description': '自带传播属性'},
                {'priority': 'could', 'module': '技能扩展', 'feature': '闹钟、提醒、翻译等', 'description': '增加实用性'},
                {'priority': 'wont', 'module': '视频通话', 'feature': '实时视频功能', 'description': '技术复杂，手机已能实现'},
                {'priority': 'wont', 'module': '行走移动', 'feature': '自主移动能力', 'description': '成本高，技术难度大'},
                {'priority': 'wont', 'module': '智能家居控制', 'feature': '控制家电', 'description': '偏离核心定位'},
            ],
            'mvp_scope': {
                'core_features': ['语音对话', '形象定制', 'App控制'],
                'enhanced_features': ['情感表达', '记忆功能', '故事资讯'],
                'cut_features': ['视频通话', '行走移动', '智能家居'],
                'timeline': '3-4个月',
            },
            'roadmap': [
                {'stage': 'MVP阶段', 'time': '0-3月', 'goal': '验证核心价值', 'features': '语音对话+形象定制+基础App'},
                {'stage': 'V1.0阶段', 'time': '3-6月', 'goal': '完善体验', 'features': '情感表达+记忆+更多技能'},
                {'stage': 'V2.0阶段', 'time': '6-12月', 'goal': '增强社交', 'features': '多角色切换+社交分享+社区'},
                {'stage': 'V3.0阶段', 'time': '12月+', 'goal': '平台化', 'features': '开放平台+开发者生态'},
            ],
            'summary': [
                '核心功能明确，但需要进一步细化',
                '建议：和目标用户验证每个功能的价值，避免"我觉得用户需要"',
                '用5-10个用户访谈验证MVP范围',
            ],
        },
        'demo_evaluation': {
            'score': 5.5,
            'dimensions': [
                {'dimension': '视觉冲击力', 'item': '产品外观设计', 'score': 7, 'description': '3D打印真人形象有独特视觉记忆点'},
                {'dimension': '视觉冲击力', 'item': 'Demo视频质量', 'score': 4, 'description': '当前可能缺少高质量演示视频'},
                {'dimension': '功能演示', 'item': '核心功能展示', 'score': 5, 'description': '需制作30秒/3分钟不同版本Demo'},
                {'dimension': '功能演示', 'item': '交互流畅度', 'score': 5, 'description': '需验证实际交互体验是否自然'},
                {'dimension': '故事叙述', 'item': '产品故事', 'score': 6, 'description': '亲情陪伴主题有情感共鸣点'},
                {'dimension': '故事叙述', 'item': '创始人故事', 'score': 4, 'description': '需补充团队背景和创始初心'},
                {'dimension': '可信度', 'item': '原型完成度', 'score': 4, 'description': '需展示可工作的原型而非渲染图'},
                {'dimension': '可信度', 'item': '用户证言', 'score': 3, 'description': '缺少早期用户测试反馈'},
            ],
            'assets': [
                {'type': '主视觉图片', 'status': '待制作', 'priority': '高', 'suggestion': '产品高清渲染图+场景图，至少5张'},
                {'type': '30秒短视频', 'status': '待制作', 'priority': '高', 'suggestion': '黄金3秒抓住眼球，讲清核心价值'},
                {'type': '3分钟详视频', 'status': '待制作', 'priority': '高', 'suggestion': '功能演示+使用场景+团队介绍'},
                {'type': '产品原型照', 'status': '待补充', 'priority': '高', 'suggestion': '真实原型照片，增加可信度'},
                {'type': '用户测试视频', 'status': '待录制', 'priority': '中', 'suggestion': '真实用户使用反应和反馈'},
                {'type': '团队介绍视频', 'status': '待制作', 'priority': '中', 'suggestion': '展示团队背景和专业能力'},
                {'type': 'GIF动图', 'status': '待制作', 'priority': '中', 'suggestion': '社交媒体传播用的短动图'},
                {'type': '3D模型展示', 'status': '待制作', 'priority': '低', 'suggestion': '网页可交互3D模型展示'},
            ],
            'summary': [
                '产品概念有视觉冲击力，但Demo素材严重不足',
                '众筹是视觉驱动的，演示素材质量直接决定转化率',
                '建议优先级：30秒视频 > 主视觉图 > 产品原型照',
            ],
        },
        'crowdfunding_strategy': {
            'score': 5,
            'tiers': [
                {'name': '早鸟体验版', 'price': '¥499（限量50名）', 'benefits': 'AI分身1台+基础功能+首批用户徽章', 'limit': '限量50个，售完即止'},
                {'name': '早鸟标准版', 'price': '¥699（限量200名）', 'benefits': 'AI分身1台+全部功能+定制礼盒', 'limit': '限量200个，早鸟价'},
                {'name': '标准版', 'price': '¥899', 'benefits': 'AI分身1台+全部功能+1年云端服务', 'limit': '不限量'},
                {'name': '双人套装', 'price': '¥1,599', 'benefits': 'AI分身2台+家庭共享功能+专属客服', 'limit': '限量100套'},
                {'name': '定制典藏版', 'price': '¥2,999', 'benefits': '高精度定制+专属编号+签名版+终身会员', 'limit': '限量30个'},
                {'name': '企业定制', 'price': '¥咨询', 'benefits': '批量定制+品牌联名+API接入', 'limit': '企业客户专享'},
            ],
            'preheat_timeline': [
                {'stage': '预热期T-30', 'time': '上线前30天', 'actions': '官网上线、社群建立、概念视频发布', 'goal': '积累1000+意向用户'},
                {'stage': '种草期T-14', 'time': '上线前14天', 'actions': 'KOL测评、媒体报道、社群预热', 'goal': '预约登记500+人'},
                {'stage': '冲刺期T-7', 'time': '上线前7天', 'actions': '倒计时海报、早鸟预告、社群福利', 'goal': '首日目标30%预热完成'},
                {'stage': '上线首日', 'time': 'Day 0', 'actions': '全渠道发布、KOL集中推送、直播', 'goal': '达成目标30%-50%'},
                {'stage': '众筹中期', 'time': 'Day 10-20', 'actions': ' stretch goal解锁、用户晒单、更新', 'goal': '持续引流和转化'},
            ],
            'channels': [
                {'type': '社交媒体', 'channels': '微博、小红书、B站、抖音', 'budget': '40%', 'expected_effect': '主要流量来源，品牌曝光'},
                {'type': 'KOL合作', 'channels': '科技博主、情感博主、二次元博主', 'budget': '30%', 'expected_effect': '核心转化渠道，信任背书'},
                {'type': '社群运营', 'channels': '微信群、Discord、QQ群', 'budget': '10%', 'expected_effect': '种子用户培养，口碑传播'},
                {'type': '媒体报道', 'channels': '36Kr、虎嗅、品玩、动点科技', 'budget': '10%', 'expected_effect': '品牌背书，增加可信度'},
                {'type': '平台流量', 'channels': '啧啧首页推荐、项目集', 'budget': '5%', 'expected_effect': '平台自然流量转化'},
                {'type': '线下活动', 'channels': '科技展会、线下体验', 'budget': '5%', 'expected_effect': '真实体验，深度转化'},
            ],
            'kol_partners': [
                {'type': '科技类KOL', 'target': 'Top 10 科技博主（B站/YouTube）', 'cooperation': '测评视频+抽奖', 'priority': '高'},
                {'type': '情感类KOL', 'target': '亲情/陪伴类博主', 'cooperation': '故事营销+体验分享', 'priority': '高'},
                {'type': '二次元KOL', 'target': 'ACG领域博主', 'cooperation': '定制形象+开箱', 'priority': '中'},
                {'type': '生活方式KOL', 'target': '生活分享类博主', 'cooperation': '日常vlog植入', 'priority': '中'},
                {'type': '科技媒体', 'target': '36Kr、虎嗅、品玩', 'cooperation': '深度报道+专访', 'priority': '高'},
                {'type': '行业专家', 'target': 'AI/硬件领域专家', 'cooperation': '顾问背书+推荐', 'priority': '中'},
            ],
            'summary': [
                '档位设计基本合理，但需验证价格敏感度',
                '预热节奏是关键，首日表现决定众筹成败',
                'KOL选择要精准，科技+情感+二次元三类组合',
                '建议：先做小规模定价测试，验证最优价格点',
            ],
        },
    }
    
    # 创建报告目录
    reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports', 'konglan-ai-avatar')
    os.makedirs(reports_dir, exist_ok=True)
    
    # 1. 生成Markdown报告
    print("\n1. 生成Markdown报告...")
    md_gen = PremiumReportGenerator()
    md_content = md_gen.generate_markdown(report_data)
    md_file = os.path.join(reports_dir, 'konglan-ai-avatar-可行性分析.md')
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"   [OK] Markdown: {md_file}")
    
    # 2. 生成HTML报告
    print("\n2. 生成HTML报告...")
    html_gen = PremiumHTMLGenerator()
    html_content = html_gen.generate_html(report_data)
    html_file = os.path.join(reports_dir, 'konglan-ai-avatar-feasibility-analysis.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"   [OK] HTML: {html_file}")
    
    # 3. 生成PDF报告
    print("\n3. 生成PDF报告...")
    pdf_file = os.path.join(reports_dir, 'konglan-ai-avatar-可行性分析.pdf')
    pdf_success = generate_pdf_from_html(os.path.abspath(html_file), pdf_file)
    
    if pdf_success:
        print(f"   [OK] PDF: {pdf_file}")
    else:
        print("   [!] PDF生成失败（Playwright不可用），跳过PDF")
        print("   提示：可运行 pip install playwright && playwright install chromium 后重试")
    
    # 保存JSON数据
    json_file = os.path.join(reports_dir, 'full_analysis_report.json')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    print(f"\n   [OK] JSON: {json_file}")
    
    print("\n" + "=" * 60)
    print("报告生成完成！")
    print("=" * 60)
    print(f"\n报告目录: {reports_dir}")
    print(f"  - Markdown: konglan-ai-avatar-可行性分析.md")
    print(f"  - HTML: konglan-ai-avatar-feasibility-analysis.html")
    if pdf_success:
        print(f"  - PDF: konglan-ai-avatar-可行性分析.pdf")
    print(f"  - JSON: full_analysis_report.json")
    
    print("\n报告包含：")
    print("  [v5.0] 6维度分析框架")
    print("  [v5.0] 17个完整章节")
    print("  [v5.0] 竞品对比分析")
    print("  [v5.0] 风险矩阵（概率×影响）")
    print("  [v5.0] 数据可视化（雷达图、柱状图、饼图）")
    print("  [v5.0] 玻璃态UI设计")
    print("  [v5.0] 可折叠章节 + 侧边栏导航")
    print("  [v5.0] 移动端响应式适配")
    print("  [v5.0] 加载动画 + 分数动画")


if __name__ == '__main__':
    main()
