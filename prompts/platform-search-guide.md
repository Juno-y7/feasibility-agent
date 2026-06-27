# 募资平台搜索操作手册

> 本手册供 LLM 在分析产品可行性时，自主前往各募资平台搜索最新案例数据使用。目标是让 LLM 在本地标杆案例不足时，能够实时获取最新的竞品和市场数据。

---

## 一、使用说明

### 什么时候应该主动搜索

在以下场景中，LLM 应该主动使用搜索引擎和平台页面获取最新数据：

1. **品类不确定时**：用户提供的产品资料模糊，无法自动归类到已知品类，需要浏览平台分类页面确认品类归属和竞争格局。
2. **需要最新竞品数据时**：本地标杆案例库的数据可能已过时（超过 6 个月），需要确认当前平台上同类产品的最新表现、定价趋势和用户反馈。
3. **用户要求验证时**：用户明确要求验证某个假设（如"这个价位是否有市场"、"类似产品能募多少钱"），需要用真实数据回答。
4. **新品类或小众品类时**：本地案例库中缺少对应品类的标杆案例，需要从平台上挖掘参考数据。
5. **地域性验证时**：用户计划在特定市场（日本、台湾、中国大陆）上线募资，需要了解该市场的平台数据和用户偏好。

### 什么时候用本地标杆案例即可

在以下场景中，优先使用 `data/benchmark-cases.json`（标杆案例库，精选19个成功+失败案例）中的本地标杆案例，无需额外搜索：

1. **品类明确且案例充足时**：产品能明确归类，且本地案例库中有 3 个以上同品类案例可做校准。
2. **标杆案例时效性足够时**：案例数据在 2 年以内，品类格局未发生重大变化（如成熟品类：充电宝、背包、桌面收纳等）。
3. **快速初筛阶段时**：只需做粗粒度的可行性判断，不需要精确到具体数字的对比。
4. **用户未要求最新数据时**：用户没有特别强调需要最新的市场数据，且本地案例足以支撑分析结论。

### 搜索优先级建议

```
本地案例库（最快） → WebSearch 间接搜索（推荐） → WebFetch 直接抓取平台页面（备选）
```

- **WebSearch** 更稳定，不容易被反爬机制拦截。
- **WebFetch** 可能被 Cloudflare 等防护拦截，建议在 WebSearch 结果不足时再使用。
- 多数情况下，WebSearch 已经能获取足够的关键数据（金额、支持者数、状态等）。

---

## 二、6 个平台搜索指南

---

### 1. Kickstarter

**平台首页**：https://www.kickstarter.com

**分类页面（直接链接）**：

| 品类 | 链接 |
|------|------|
| 科技 | https://www.kickstarter.com/categories/technology |
| 设计 | https://www.kickstarter.com/categories/design |
| 游戏 | https://www.kickstarter.com/categories/games |
| 影视 | https://www.kickstarter.com/categories/film |
| 音乐 | https://www.kickstarter.com/categories/music |
| 出版 | https://www.kickstarter.com/categories/publishing |
| 食品 | https://www.kickstarter.com/categories/food |
| 时尚 | https://www.kickstarter.com/categories/fashion |
| 手工艺 | https://www.kickstarter.com/categories/crafts |
| 艺术 | https://www.kickstarter.com/categories/art |
| 摄影 | https://www.kickstarter.com/categories/photography |
| 戏剧 | https://www.kickstarter.com/categories/theater |
| 新闻业 | https://www.kickstarter.com/categories/journalism |
| 科幻 | https://www.kickstarter.com/categories/comics |

**搜索方法**：

1. **网页搜索关键词模板（WebSearch）**：
   ```
   site:kickstarter.com [品类关键词] most funded
   site:kickstarter.com [品类关键词] 2024 OR 2025
   kickstarter [品类] top projects funded amount
   "kickstarter" [产品类型] funding successful
   ```
   示例：
   - `site:kickstarter.com smart ring most funded`
   - `kickstarter EDC tool top funded 2024`
   - `site:kickstarter.com portable projector most backed`

2. **平台内搜索（WebFetch URL 模式）**：
   ```
   https://www.kickstarter.com/discover/advanced?category_id={分类ID}&sort=magic&seed=2796304&page=1
   https://www.kickstarter.com/discover/advanced?term={搜索关键词}&sort=magic
   https://www.kickstarter.com/discover/advanced?category_id=16&sort=most_funded
   ```
   常用分类 ID：Technology=16, Design=7, Games=12

3. **热门项目发现页**：
   ```
   https://www.kickstarter.com/discover/most-funded?category_id={分类ID}
   https://www.kickstarter.com/discover/recommended?category_id={分类ID}
   ```

**关键指标解读**：

| 指标 | 说明 | 判断标准 |
|------|------|----------|
| Pledged Amount（已募金额） | 项目实际募集到的总金额 | 对比同品类中位数，判断产品竞争力 |
| Backers（支持者数） | 支持该项目的人数 | 判断真实需求规模；<100 人需警惕 |
| Goal（目标金额） | 项目设定的募资目标 | 达成率 = Pledged / Goal |
| % Funded（达成率） | 募集金额占目标的百分比 | >100% 为成功；>1000% 为爆款 |
| Estimated Delivery（预计交付） | 承诺的交付时间 | 对比当前日期判断是否延期 |
| Campaign Duration（募资周期） | 募资活动持续天数 | 通常 30-60 天 |

**URL 模式**：
```
https://www.kickstarter.com/projects/{creator}/{slug}
```
示例：`https://www.kickstarter.com/projects/ouraring/oura-ring-gen3`

**数据提取技巧**：

1. 从搜索结果页抓取项目列表时，重点关注：项目名称、缩略图、简短描述、已募金额、支持者数、分类标签。
2. 进入项目详情页后，提取以下信息：
   - 价格档位（Reward tiers）：最低入门价、最受欢迎档位、均价
   - 项目描述中的核心卖点和差异化表述
   - 更新日志（Updates）：看是否有延期、生产问题、退款投诉
   - 评论区（Comments）：看真实用户反馈和常见问题
3. 注意区分 "Staff Pick"（平台推荐）和普通项目，Staff Pick 通常流量更高。

---

### 2. Indiegogo

**平台首页**：https://www.indiegogo.com

**分类页面（直接链接）**：

| 品类 | 链接 |
|------|------|
| 科技与设计 | https://www.indiegogo.com/explore/tech-design |
| 健康与健身 | https://www.indiegogo.com/explore/health-fitness |
| 创意与艺术 | https://www.indiegogo.com/explore/creative-arts |
| 教育与公益 | https://www.indiegogo.com/explore/education |
| 食品与饮品 | https://www.indiegogo.com/explore/food-beverage |
| 手工与家居 | https://www.indiegogo.com/explore/home-crafts |
| 旅行与户外 | https://www.indiegogo.com/explore/travel-outdoor |
| 动画与影视 | https://www.indiegogo.com/explore/film |
| 音乐 | https://www.indiegogo.com/explore/music |
| 游戏 | https://www.indiegogo.com/explore/games |
| 出版 | https://www.indiegogo.com/explore/publishing |
| 全部探索 | https://www.indiegogo.com/explore |

**搜索方法**：

1. **网页搜索关键词模板（WebSearch）**：
   ```
   site:indiegogo.com [品类] crowdfunding
   indiegogo [品类] top funded projects
   "indiegogo" [产品类型] raised
   indiegogo [品类] InDemand
   indiegogo [品类] collection featured
   ```
   示例：
   - `site:indiegogo.com smart glasses crowdfunding`
   - `indiegogo portable power station top funded`
   - `indiegogo EDC multi-tool InDemand`

2. **平台内搜索（WebFetch URL 模式）**：
   ```
   https://www.indiegogo.com/explore?q={搜索关键词}&sort=trending
   https://www.indiegogo.com/explore?q={搜索关键词}&sort=most_funded
   https://www.indiegogo.com/explore?q={搜索关键词}&sort=newest
   ```

3. **精选合集页**：
   ```
   https://www.indiegogo.com/explore/collections
   https://www.indiegogo.com/explore/tech-design?sort=most_funded
   ```

**关键指标解读**：

| 指标 | 说明 | 判断标准 |
|------|------|----------|
| Raised（已募金额） | 实际募集到的总金额 | 对比同品类项目中位数 |
| Goal（目标金额） | 设定的募资目标 | Indiegogo 有灵活目标制 |
| Funded %（达成率） | 募集金额占目标的百分比 | >=100% 为达到目标 |
| Backers（支持者数） | 支持该项目的人数 | 判断需求规模 |
| InDemand 状态 | 募资结束后继续销售 | InDemand 项目仍在持续产生收入 |
| Estimated Delivery（预计交付） | 承诺的交付时间 | 注意是否延期 |

**特别注意事项**：

- **InDemand 项目**：Indiegogo 的独有机制。项目在募资期结束后可以转为 InDemand 状态继续接受预购。这意味着一个项目的"总金额"可能远超初始募资目标。分析时要区分"募资期金额"和"InDemand 累计金额"。
- **Flexible Funding（灵活目标制）**：Indiegogo 允许项目设定灵活目标，即使未达标也能拿到已募集的资金。这与 Kickstarter 的"全有或全无"机制不同，因此 Indiegogo 上低金额项目的"成功率"不能直接和 Kickstarter 对比。
- **分类整合**：Indiegogo 的分类较 Kickstarter 更粗（如 Tech & Design 合并为一个），搜索时需要用关键词进一步细分。

**URL 模式**：
```
https://www.indiegogo.com/projects/{slug}
https://www.indiegogo.com/projects/{slug}/#/  （带评论页）
```
示例：`https://www.indiegogo.com/projects/amazon-smart-glasses`

**数据提取技巧**：

1. Indiegogo 的项目页面通常包含"Story"部分（长文案）和"Gallery"部分（图片/视频），重点从 Story 中提取核心卖点和定价策略。
2. 关注 Perks（价格档位）部分，提取价格阶梯和各档位的支持人数。
3. InDemand 项目要查看"Total Raised"（累计金额），这往往远大于初始募资金额。
4. 评论区可能包含关于交付延迟、产品质量等关键信息。

---

### 3. 嘖嘖 zeczec

**平台首页**：https://www.zeczec.com

**分类页面（直接链接）**：

| 品类 | 链接 |
|------|------|
| 全部分类 | https://www.zeczec.com/categories |
| 设计应用 | https://www.zeczec.com/categories/设计应用 |
| 科技发明 | https://www.zeczec.com/categories/科技发明 |
| 社会公益 | https://www.zeczec.com/categories/社会公益 |
| 影音娱乐 | https://www.zeczec.com/categories/影音娱乐 |
| 美食农产 | https://www.zeczec.com/categories/美食农产 |
| 演出活动 | https://www.zeczec.com/categories/演出活动 |
| 地方创生 | https://www.zeczec.com/categories/地方创生 |
| 出版 | https://www.zeczec.com/categories/出版 |
| 休旅交通 | https://www.zeczec.com/categories/休旅交通 |
| 桌游 | https://www.zeczec.com/categories/桌游 |
| 教育学习 | https://www.zeczec.com/categories/教育学习 |
| 摄影出版 | https://www.zeczec.com/categories/摄影出版 |
| 游戏动漫 | https://www.zeczec.com/categories/游戏动漫 |
| 医疗健康 | https://www.zeczec.com/categories/医疗健康 |
| 环保永续 | https://www.zeczec.com/categories/环保永续 |
| 美妆保养 | https://www.zeczec.com/categories/美妆保养 |

**搜索方法**：

1. **网页搜索关键词模板（WebSearch）**——推荐使用，更稳定：
   ```
   嘖嘖 zeczec [品类] 募資
   嘖嘖 [品类] 众筹 成功
   "zeczec" [品类] 募资 金额
   嘖嘖 [品类] 热门 项目
   ```
   示例：
   - `嘖嘖 zeczec 科技發明 募資 2024`
   - `嘖嘖 智慧家居 募資 成功`
   - `"zeczec" 背包 募资`
   - `嘖嘖 EDC 工具 募資`

2. **平台内搜索（WebFetch URL 模式）**：
   ```
   https://www.zeczec.com/search?q={搜索关键词}
   https://www.zeczec.com/categories/{分类名}
   ```
   **注意**：嘖嘖使用 Cloudflare 防护，WebFetch 直接抓取可能被拦截（返回 Cloudflare 验证页面）。建议优先使用 WebSearch 间接搜索。

3. **热门/推荐项目**：
   ```
   https://www.zeczec.com/ （首页展示热门和推荐项目）
   ```

**关键指标解读**：

| 指标 | 说明 | 判断标准 |
|------|------|----------|
| 已募集金额（NT$） | 项目募集到的新台币金额 | 需要换算为其他货币做对比 |
| 目标金额（NT$） | 设定的募资目标 | 达成率 = 已募集 / 目标 |
| 赞助人数 | 支持该项目的人数 | 台湾市场参考规模 |
| 赞助方案 | 价格档位 | 最低入门价、最受欢迎档位 |
| 募资状态 | 进行中 / 成功 / 失败 | 当前项目状态 |
| 预计交付 | 承诺的交付日期 | 判断履约情况 |

**特别注意事项**：

- **Cloudflare 防护**：嘖嘖网站有严格的反爬机制，WebFetch 可能被 Cloudflare 拦截返回 403 或验证页面。**强烈建议优先使用 WebSearch 搜索**，而不是直接 WebFetch 嘖嘖页面。
- **币种**：嘖嘖的金额以新台币（NT$ / TWD）计价。做跨平台对比时需换算（1 USD ≈ 30-32 TWD）。
- **台湾市场特色**：嘖嘖的用户以台湾为主，品类偏好与 Kickstarter 不同（更多社会公益、地方创生、桌游类项目）。硬件科技类项目的体量通常小于 Kickstarter。
- **繁体中文**：搜索关键词建议使用繁体中文以获得更好结果。

**URL 模式**：
```
https://www.zeczec.com/projects/{slug}
```
示例：`https://www.zeczec.com/projects/xxx`

**数据提取技巧**：

1. 通过 WebSearch 搜索嘖嘖项目时，搜索结果摘要通常已包含金额和状态信息，可以直接提取。
2. 如果 WebFetch 成功进入项目页面，重点关注：赞助方案（定价策略）、项目介绍（核心卖点）、赞助人数和金额。
3. 注意嘖嘖上"专案"和"提案"的用法，搜索时两个词都可以尝试。

---

### 4. Makuake

**平台首页**：https://www.makuake.com

**分类页面与排行榜（直接链接）**：

| 页面 | 链接 |
|------|------|
| 全部探索 | https://www.makuake.com/discover/ |
| 排行榜（总榜） | https://www.makuake.com/discover/ranking/ |
| 排行榜（进行中） | https://www.makuake.com/discover/ranking/?status=active |
| 排行榜（已结束） | https://www.makuake.com/discover/ranking/?status=end |
| 科技 | https://www.makuake.com/discover/ranking/?category=tech |
| 设计 | https://www.makuake.com/discover/ranking/?category=design |
| 生活 | https://www.makuake.com/discover/ranking/?category=lifestyle |
| 美食 | https://www.makuake.com/discover/ranking/?category=food |
| 时尚 | https://www.makuake.com/discover/ranking/?category=fashion |
| 地域 | https://www.makuake.com/discover/ranking/?category=local |
| 动漫/IP | https://www.makuake.com/discover/ranking/?category=anime |
| 影音 | https://www.makuake.com/discover/ranking/?category=movie |
| 游戏 | https://www.makuake.com/discover/ranking/?category=game |
| 书籍 | https://www.makuake.com/discover/ranking/?category=book |

**搜索方法**：

1. **网页搜索关键词模板（WebSearch）**——必须用日文：
   ```
   Makuake [品类日文] プロジェクト
   Makuake [品类日文] 最も集金
   マクアケ [品类日文] クラウドファンディング
   "makuake" [品类日文] 金額
   マクアケ [品类日文] 人気
   ```
   常用品类日文对照：
   - 智能设备 / IoT：スマートデバイス, IoT, スマートガジェット
   - 家居 / 生活用品：生活雑貨, インテリア, スマートホーム
   - 背包 / 箱包：バッグ, リュック, カバン
   - 厨房 / 炊具：キッチン, 調理器具
   - 户外 / 露营：アウトドア, キャンプ
   - 健康 / 养生：健康, ウェルネス, フィットネス
   - EDC / 工具：EDC, ツール, 多機能
   - 桌游 / 游戏：ボードゲーム, トレーディングカード
   - 手办 / 模型：フィギュア, プラモデル
   - 动画 / IP：アニメ, IPコラボ

   示例：
   - `Makuake スマートデバイス プロジェクト 最も集金`
   - `マクアケ キャンプ クラウドファンディング 人気 2024`
   - `"makuake" スマートリング 金額`

2. **平台内搜索（WebFetch URL 模式）**：
   ```
   https://www.makuake.com/discover/?keyword={日文关键词}
   https://www.makuake.com/discover/ranking/?keyword={日文关键词}
   ```

3. **排行榜页面**（推荐，数据最集中）：
   ```
   https://www.makuake.com/discover/ranking/?category={分类}&period=total
   https://www.makuake.com/discover/ranking/?period=yearly
   ```

**关键指标解读**：

| 指标 | 说明 | 判断标准 |
|------|------|----------|
| 集金額（募集金额） | 项目募集到的日元总额 | 对比同品类项目中位数 |
| 目標金額（目标金额） | 设定的募资目标 | 达成率 = 集金額 / 目標金額 |
| サポーター数（支持者数） | 支持该项目的人数 | 日本市场规模参考 |
| 達成率（达成率） | 募集金额占目标的百分比 | >100% 为成功 |
| 価格（价格） | 各档位价格 | 日元计价，需换算 |
| ステータス（状态） | 实施中 / 成功 / 终了 | 当前项目状态 |

**特别注意事项**：

- **日文界面**：Makuake 全站为日文，搜索时必须使用日文关键词。中文或英文关键词搜索结果会非常有限。
- **币种**：金额以日元（JPY / 円）计价。做跨平台对比时需换算（1 USD ≈ 150-160 JPY，1 TWD ≈ 4.5-5 JPY）。
- **日本市场特色**：Makuake 用户偏好精致设计、IP 联名、动漫相关产品。生活质量类产品（家居、厨房、文具）表现突出。硬件科技类项目通常包装精美，强调"匠人精神"和"日本制造"。
- **排行榜功能强大**：Makuake 的排行榜页面数据非常集中，是获取品类数据的最佳入口。
- **集金額 vs 総額**：注意区分"募集期间金额"和"含贩路扩大（后期销售）的累计金额"。

**URL 模式**：
```
https://www.makuake.com/project/{slug}/
```
示例：`https://www.makuake.com/project/smart-device-xxx/`

**数据提取技巧**：

1. 排行榜页面是数据最密集的入口，一页可以看到多个项目的金额、支持者数、达成率。
2. 项目页面中，"リターン"（Return）部分对应价格档位，"プロジェクト詳細"部分包含详细描述。
3. 关注"Makuake magazine"部分，这里常有编辑推荐和品类分析文章，可以辅助了解市场趋势。
4. 注意日本产品的包装和文案风格，这对分析日本市场的用户偏好很有帮助。

---

### 5. 摩点 modian

**平台首页**：https://zhongchou.modian.com

**排行榜（直接链接）**：

| 页面 | 链接 |
|------|------|
| 全部排行 | https://zhongchou.modian.com/rank |
| 进行中排行 | https://zhongchou.modian.com/rank/ing |
| 已结束排行 | https://zhongchou.modian.com/rank/ed |
| 热门推荐 | https://zhongchou.modian.com/ |

**搜索方法**：

1. **网页搜索关键词模板（WebSearch）**：
   ```
   摩点 [品类] 众筹
   modian [品类] 众筹 金额
   site:zhongchou.modian.com [品类]
   摩点 [品类] 热门
   "摩点" [品类] 手办 众筹
   ```
   示例：
   - `摩点 手办 众筹 金额 2024`
   - `modian 桌游 众筹 热门`
   - `摩点 原画集 众筹 成功`
   - `site:zhongchou.modian.com 机械键盘`

2. **平台内搜索（WebFetch URL 模式）**：
   ```
   https://zhongchou.modian.com/search?keyword={搜索关键词}
   https://zhongchou.modian.com/search?keyword={搜索关键词}&type=item
   ```

3. **分类浏览**：
   ```
   https://zhongchou.modian.com/category/{分类ID}
   ```
   常见分类：动漫、游戏、影视、音乐、出版、科技、设计

**关键指标解读**：

| 指标 | 说明 | 判断标准 |
|------|------|----------|
| 已筹金额（CNY） | 项目募集到的人民币金额 | 中国大陆市场参考 |
| 目标金额（CNY） | 设定的募资目标 | 达成率 = 已筹 / 目标 |
| 支持人数 | 支持该项目的人数 | 判断粉丝经济效应 |
| 进度 | 募集进度百分比 | >100% 为成功 |
| 状态 | 筹集中 / 成功 / 失败 | 当前项目状态 |

**特别注意事项**：

- **ACG/IP 为核心品类**：摩点的头部品类是 ACG（动画、漫画、游戏）相关的手办、模型、桌游、原画集、周边产品。IP 驱动非常明显，知名 IP 的项目金额往往远超原创 IP。
- **粉丝经济效应**：摩点上的成功项目很大程度上依赖粉丝基础和社群运营。分析时要区分"产品本身的吸引力"和"IP/粉丝号召力"。
- **币种**：金额以人民币（CNY / 元）计价。
- **中国大陆市场**：用户以中国大陆为主，品类偏好集中在二次元文化和创意消费领域。硬件科技类项目在摩点上的表现通常不如 Kickstarter。
- **品类局限性**：如果用户的产品是非 ACG 类的硬件产品（如智能设备、户外装备），摩点的参考价值有限，建议优先看 Kickstarter 和 Indiegogo。

**URL 模式**：
```
https://zhongchou.modian.com/item/{id}
```
示例：`https://zhongchou.modian.com/item/123456`

**数据提取技巧**：

1. 排行榜页面是获取摩点数据的最佳入口，可以看到各品类的金额和支持人数排名。
2. 项目页面中，"项目详情"包含产品描述，"支持方案"对应价格档位。
3. 重点关注"动态"或"评论"区域，了解 backers 的真实反馈和交付情况。
4. 摩点项目中很多是 IP 授权产品，分析时要记录 IP 名称和版权方，这对判断项目成功因素很重要。

---

### 6. flyingV

**平台首页**：https://flyingv.cc

**分类页面**：

| 品类 | 链接 |
|------|------|
| 全部项目 | https://flyingv.cc/ |
| 社会创新 | https://flyingv.cc/categories/social-innovation |
| 教育 | https://flyingv.cc/categories/education |
| 音乐 | https://flyingv.cc/categories/music |
| 美食 | https://flyingv.cc/categories/food |
| 设计 | https://flyingv.cc/categories/design |
| 影视 | https://flyingv.cc/categories/film |
| 出版 | https://flyingv.cc/categories/publishing |
| 科技 | https://flyingv.cc/categories/technology |
| 艺术 | https://flyingv.cc/categories/art |
| 表演 | https://flyingv.cc/categories/performance |
| 旅游 | https://flyingv.cc/categories/travel |

**搜索方法**：

1. **网页搜索关键词模板（WebSearch）**：
   ```
   flyingV 募資 [品类]
   flyingV [品类] 众筹 金额
   "flyingv" [品类] 募资
   flyingV [品类] 热门
   ```
   示例：
   - `flyingV 社会创新 募資 金额`
   - `flyingV 教育計畫 募資 2024`
   - `"flyingv" 音乐 专辑 募资`

2. **平台内搜索（WebFetch URL 模式）**：
   ```
   https://flyingv.cc/explore?q={搜索关键词}
   https://flyingv.cc/categories/{分类英文名}
   ```

3. **热门项目**：
   ```
   https://flyingv.cc/ （首页展示精选和热门项目）
   ```

**关键指标解读**：

| 指标 | 说明 | 判断标准 |
|------|------|----------|
| 已募金额（NT$） | 项目募集到的新台币金额 | 台湾市场参考 |
| 目标金额（NT$） | 设定的募资目标 | 达成率 = 已募 / 目标 |
| 赞助人数 | 支持该项目的人数 | 判断需求规模 |
| 状态 | 募资中 / 成功 / 失败 | 当前项目状态 |
| 募资天数 | 募资活动的持续时间 | 通常 30-60 天 |

**特别注意事项**：

- **流量较小**：flyingV 是台湾的募资平台，整体流量和项目数量远小于嘖嘖和 Kickstarter。因此单项目的金额和支持人数通常较低。
- **品类偏重**：flyingV 上社会创新、教育、音乐类项目占比较高，科技硬件类项目较少。如果分析的是硬件产品，flyingV 的参考价值有限。
- **数据量有限**：由于平台流量较小，搜索时可能找不到足够的同品类案例。建议将 flyingV 作为补充数据源，而非主要数据源。
- **币种**：金额以新台币（NT$ / TWD）计价。
- **繁体中文**：搜索关键词建议使用繁体中文。

**URL 模式**：
```
https://flyingv.cc/projects/{slug}
```
示例：`https://flyingv.cc/projects/xxx`

**数据提取技巧**：

1. flyingV 项目数量较少，搜索结果可能不理想。建议结合嘖嘖数据一起使用。
2. flyingV 的独特价值在于社会创新和教育类项目，这些品类在其他平台上数据较少。
3. 项目页面中关注"专案内容"和"赞助方案"部分。

---

## 三、搜索结果评估清单

搜到案例后，LLM 应该按以下清单提取信息，并进行结构化对比：

### 3.1 必须提取的信息

| 信息项 | 说明 | 用途 |
|--------|------|------|
| 项目名称 | 完整的项目名称 | 用于引用和对比 |
| 平台来源 | 来自哪个募资平台 | 用于标注数据来源 |
| 项目状态 | 进行中 / 成功 / 失败 / InDemand | 判断项目当前阶段 |
| 募集金额 | 实际募集到的总金额（标注币种） | 核心对比数据 |
| 目标金额 | 设定的募资目标（标注币种） | 计算达成率 |
| 达成率 | 募集金额 / 目标金额 | 判断项目热度 |
| 支持者数量 | 支持该项目的人数 | 判断需求真实度 |
| 价格区间 | 最低价格 - 最高价格（标注币种） | 对比用户产品定价 |
| 核心卖点 | 1-3 个核心卖点描述 | 和用户产品做差异化对比 |
| 上线时间 | 募资活动开始日期 | 判断市场时机 |
| 募资周期 | 募资活动持续天数 | 判断募资效率 |
| 交付状态 | 是否按时交付 / 延期 / 取消 | 判断履约风险 |
| 项目 URL | 项目页面链接 | 用于引用 |

### 3.2 可选但建议提取的信息

| 信息项 | 说明 | 用途 |
|--------|------|------|
| 团队背景 | 创始团队/公司介绍 | 判断团队经验和可信度 |
| IP 授权 | 是否有 IP 联名/授权 | 判断 IP 依赖度 |
| 媒体报道 | 是否有媒体/博主推荐 | 判断外部背书 |
| 更新频率 | 项目更新日志数量 | 判断团队活跃度 |
| 评论区反馈 | 支持者的正面/负面评价 | 判断用户满意度 |
| 退换货政策 | 退款和售后政策 | 判断风险控制 |

### 3.3 对比分析方法

提取完信息后，按以下维度进行对比分析：

1. **金额对比**：将所有案例的募集金额统一换算为同一币种（建议 USD），计算中位数、最高值、最低值。用户产品的预期金额应在哪个区间？

2. **价格对比**：提取所有案例的均价和价格分布，判断用户产品的定价是否合理。过高可能导致转化率低，过低可能影响毛利。

3. **达成率分析**：达成率是判断产品市场吸引力的关键指标。如果同品类项目的达成率普遍低于 200%，说明该品类的市场接受度有限。

4. **交付风险评估**：如果同品类项目频繁出现延期交付，需要将履约风险纳入可行性分析。

5. **卖点差异化**：列出所有案例的核心卖点矩阵，判断用户产品是否有足够的差异化空间。如果所有竞品都主打同一个卖点，用户需要找到新的切入角度。

6. **支持者数量验证**：支持者数量是判断需求真实度的硬指标。如果同品类项目的支持者数量普遍低于 500 人，需要警惕该品类的真实市场规模。

### 3.4 数据记录格式

搜索完成后，LLM 应该将结果整理为以下格式，方便后续分析：

```json
{
  "platform_search_results": {
    "search_date": "YYYY-MM-DD",
    "search_keywords": ["关键词1", "关键词2"],
    "platforms_searched": ["kickstarter", "indiegogo", ...],
    "cases_found": [
      {
        "project_name": "项目名称",
        "platform": "平台名",
        "status": "成功/进行中/失败",
        "amount_raised": 金额数值,
        "amount_currency": "USD/TWD/JPY/CNY",
        "amount_raised_usd": 换算后美元金额,
        "goal_amount": 目标金额数值,
        "goal_currency": "币种",
        "achievement_rate": 达成率百分比,
        "backers": 支持者数量,
        "price_range": {
          "min": 最低价,
          "max": 最高价,
          "currency": "币种",
          "most_popular_tier": 最受欢迎档位价格
        },
        "key_selling_points": ["卖点1", "卖点2", "卖点3"],
        "launch_date": "YYYY-MM-DD",
        "campaign_duration_days": 天数,
        "delivery_status": "按时/延期/未到交付期",
        "project_url": "URL",
        "team_background": "团队简介",
        "ip_licensed": true/false,
        "notes": "其他值得注意的信息"
      }
    ],
    "analysis_summary": {
      "total_cases": 案例总数,
      "median_amount_usd": 中位数金额,
      "max_amount_usd": 最高金额,
      "min_amount_usd": 最低金额,
      "median_backers": 中位数支持者数,
      "average_achievement_rate": 平均达成率,
      "delivery_delay_rate": 延期交付比例,
      "price_range_usd": {
        "min": 最低均价,
        "max": 最高均价
      },
      "common_selling_points": ["最常见卖点1", "最常见卖点2"],
      "market_gap_opportunities": ["差异化机会1", "差异化机会2"],
      "key_insights": "整体市场观察总结"
    }
  }
}
```

---

## 四、跨平台对比注意事项

### 4.1 币种换算参考

做跨平台对比时，需要将所有金额统一换算为同一币种。以下是常用参考汇率（LLM 应使用搜索获取实时汇率）：

| 货币 | 符号 | 参考汇率（兑 USD） |
|------|------|---------------------|
| 美元 | USD | 1.00 |
| 新台币 | TWD / NT$ | 1 USD ≈ 30-32 TWD |
| 日元 | JPY / 円 | 1 USD ≈ 150-160 JPY |
| 人民币 | CNY / 元 | 1 USD ≈ 7.0-7.3 CNY |

### 4.2 平台特性差异

| 维度 | Kickstarter | Indiegogo | 嘖嘖 | Makuake | 摩点 | flyingV |
|------|------------|-----------|------|---------|------|---------|
| 主要市场 | 全球（英语） | 全球（英语） | 台湾 | 日本 | 中国大陆 | 台湾 |
| 币种 | USD / 各国货币 | USD / 各国货币 | TWD | JPY | CNY | TWD |
| 募资机制 | 全有或全无 | 灵活/全有全无 | 全有或全无 | 全有或全无 | 全有或全无 | 全有或全无 |
| InDemand | 无 | 有 | 无 | 有（贩路扩大） | 无 | 无 |
| 典型金额范围 | $10K-$10M | $5K-$5M | NT$50万-5000万 | ¥500万-5亿 | ¥5万-500万 | NT$10万-500万 |
| 头部品类 | 科技/设计/游戏 | 科技/健康 | 社会公益/设计/桌游 | 生活/设计/动漫IP | 手办/桌游/出版 | 社会创新/教育/音乐 |
| 反爬严格度 | 中 | 低-中 | 高（Cloudflare） | 中 | 低 | 低 |

### 4.3 搜索效率建议

1. **先搜大平台，再补小平台**：先搜 Kickstarter 和 Indiegogo（数据量大、搜索稳定），再根据地域需要补充嘖嘖/Makuake/摩点。
2. **先搜关键词，再浏览分类**：先用 WebSearch 搜索具体品类关键词，获取精确案例；如果案例不足，再浏览平台分类页面。
3. **善用排行榜**：Makuake 和摩点的排行榜是获取大量案例数据的最快入口。
4. **控制搜索次数**：每个平台通常搜索 1-2 次就能获取足够数据，避免重复搜索浪费资源。
5. **记录搜索关键词**：记录实际使用的搜索关键词和对应结果数量，方便回溯和补充。

---

## 五、常见问题处理

### Q1：WebFetch 被拦截怎么办？

**解决方案**：
1. 切换到 WebSearch 间接搜索（`site:域名 关键词`）。
2. 尝试搜索该项目的媒体报道或测评文章，通常包含关键数据。
3. 尝试使用 Google Cache 或 Wayback Machine（`web.archive.org`）。
4. 如果多次尝试仍被拦截，跳过该平台，在报告中注明"因平台反爬限制，未能直接获取数据"。

### Q2：搜索结果不够多怎么办？

**解决方案**：
1. 扩大关键词范围（使用同义词、更宽泛的品类词）。
2. 切换到英文关键词搜索 Kickstarter/Indiegogo。
3. 搜索相近品类（如搜索"smart ring"时补充搜索"wearable device"）。
4. 搜索媒体报道和博客文章，它们通常汇总了多个案例。

### Q3：如何判断数据的可信度？

**判断标准**：
1. **平台官方数据**（项目页面上的金额、支持者数）可信度最高。
2. **媒体报道数据**：通常引用平台数据，但可能过时或引用错误。
3. **第三方统计网站**（如 Kicktraq、CrowdCrux）可能提供历史趋势数据。
4. 如果多个来源的数据一致，可信度较高。
5. 如果数据来自社交媒体或论坛帖子，需要交叉验证。

### Q4：找不到同品类案例怎么办？

**解决方案**：
1. 搜索相近品类或功能替代品（如用户做"智能戒指"，可搜索"智能手环"或"可穿戴设备"）。
2. 搜索该品类的传统市场数据（电商平台的销量、评价等）。
3. 使用本地标杆案例库中的通用案例作为参考基准。
4. 在报告中明确标注"该品类在募资平台上案例稀少，以下数据来自相近品类"。

---

*本手册版本：v1.0 | 最后更新：2026-06-27*
*供 LLM 在产品可行性分析过程中自主搜索募资平台数据使用*
