import os
from PIL import Image, ImageDraw, ImageFont

VID_DIR = r"d:\AKFile\其他\投资\去杠杆与暴跌速度对比分析\video_production"
SRC_DIR = r"d:\AKFile\其他\投资\去杠杆与暴跌速度对比分析"
SLIDES_DIR = os.path.join(VID_DIR, "dynamic_slides")
os.makedirs(SLIDES_DIR, exist_ok=True)

font_bold = r"C:\Windows\Fonts\msyhbd.ttc"
font_reg = r"C:\Windows\Fonts\msyh.ttc"

f_huge = ImageFont.truetype(font_bold, 80)
f_title = ImageFont.truetype(font_bold, 60)
f_h2 = ImageFont.truetype(font_bold, 44)
f_h3 = ImageFont.truetype(font_bold, 36)
f_body = ImageFont.truetype(font_reg, 32)
f_sub = ImageFont.truetype(font_reg, 26)
f_pill = ImageFont.truetype(font_bold, 24)
f_num = ImageFont.truetype(font_bold, 90)

BG_COLOR = (8, 14, 30)

def base_slide(category, title_text):
    img = Image.new('RGB', (1920, 1080), color=BG_COLOR)
    d = ImageDraw.Draw(img)
    # Top bar
    d.rectangle([(0, 0), (1920, 85)], fill=(16, 26, 56))
    d.rectangle([(0, 83), (1920, 85)], fill=(0, 229, 255))
    
    # Category tag
    d.rounded_rectangle([(40, 18), (240, 68)], radius=8, fill=(25, 45, 90), outline=(0, 229, 255), width=1)
    d.text((55, 27), category, font=f_pill, fill=(0, 229, 255))
    
    # Title
    d.text((260, 18), title_text, font=f_h3, fill=(255, 255, 255))
    
    # Bottom margin reservation for subtitles (height 980-1080 is reserved for subtitles)
    d.rectangle([(0, 970), (1920, 1080)], fill=(5, 9, 20))
    d.line([(0, 970), (1920, 970)], fill=(30, 45, 75), width=1)
    return img, d

def embed_chart_slide(category, title_text, chart_name, banner_text, out_name):
    img, d = base_slide(category, title_text)
    chart_path = os.path.join(SRC_DIR, chart_name)
    if os.path.exists(chart_path):
        c_img = Image.open(chart_path)
        c_img.thumbnail((1780, 780), Image.Resampling.LANCZOS)
        cx = (1920 - c_img.width) // 2
        cy = 100 + (780 - c_img.height) // 2
        img.paste(c_img, (cx, cy))
    
    # Highlight banner above subtitles
    d.rounded_rectangle([(80, 895), (1840, 955)], radius=10, fill=(20, 35, 75), outline=(255, 179, 0), width=1)
    d.text((110, 908), banner_text, font=ImageFont.truetype(font_bold, 28), fill=(255, 215, 0))
    img.save(os.path.join(SLIDES_DIR, out_name))

print("Generating 27 dynamic slides...")

# 01. Cover: 跳伞绑沙袋
img, d = base_slide("核心悬念", "A股科技去杠杆到底到没到位？")
d.text((120, 200), "高空跳伞打不开伞，", font=f_huge, fill=(255, 255, 255))
d.text((120, 300), "正常人拉备用伞自救，", font=f_huge, fill=(0, 229, 255))
d.text((120, 400), "大机构却往自己身上拼命绑沙袋？！", font=f_huge, fill=(255, 82, 82))
d.rounded_rectangle([(120, 550), (1800, 880)], radius=16, fill=(16, 28, 60), outline=(40, 65, 120), width=2)
d.text((160, 590), "· 现象揭秘：指数深跌30%，借款却纹丝不动，两融曲线不寻常走平钝化", font=f_h3, fill=(240, 240, 250))
d.text((160, 680), "· 核心矛盾：个股融资被砍得血肉模糊，科技ETF两融却逆势暴涨创新高！", font=f_h3, fill=(255, 193, 7))
d.text((160, 770), "· 深度推演：中国科技股去杠杆远未到位，一场融资堰塞湖正在成型！", font=f_h3, fill=(255, 82, 82))
img.save(os.path.join(SLIDES_DIR, "slide_01.png"))

# 02. 项目与数据源背景
img, d = base_slide("研究背景", "底层数据权威来源与研究范围说明")
d.text((120, 160), "100% 提取自中国银河证券交易所实盘清算库", font=f_title, fill=(0, 229, 255))
boxes = [
    ("全市场两融汇总", "每日沪深北三大交易所完整清算库汇总（截至2026年10月30日）", (20, 45, 90)),
    ("个股与ETF两融明细", "涵盖科创芯片、通信ETF、半导体设备ETF以及易中天/寒武纪全部流水", (30, 40, 85)),
    ("官方复权K线与份额", "精确剔除分红拆股扰动（通信ETF 1拆2、科创芯片 1拆3 完整复权修正）", (20, 50, 70)),
    ("全球历史股灾数据库", "标普500、纳斯达克、2015股灾、2008金融危机全周期日度高频数据", (40, 30, 80))
]
y_box = 270
for title, desc, col in boxes:
    d.rounded_rectangle([(120, y_box), (1800, y_box + 125)], radius=12, fill=col, outline=(50, 80, 150), width=1)
    d.text((160, y_box + 22), title, font=f_h2, fill=(255, 215, 0))
    d.text((160, y_box + 75), desc, font=f_body, fill=(220, 230, 245))
    y_box += 155
img.save(os.path.join(SLIDES_DIR, "slide_02.png"))

# 03. 两波下跌本质差异卡片
img, d = base_slide("核心框架", "为什么必须严格区分两波独立下跌？")
# Left Card: Wave 1
d.rounded_rectangle([(120, 180), (920, 880)], radius=16, fill=(15, 35, 70), outline=(0, 229, 255), width=2)
d.text((160, 220), "【第一波：7月踩踏波】", font=f_h2, fill=(0, 229, 255))
d.text((160, 300), "性质：牛市初次见顶，主动出清", font=f_h3, fill=(255, 255, 255))
d.text((160, 380), "· 指数下跌：-21% ~ -24%", font=f_body, fill=(220, 230, 245))
d.text((160, 460), "· 全市场融资：净砍 -4,211 亿元", font=f_h2, fill=(76, 175, 80))
d.text((160, 550), "· 杠杆去化率：-14.0% 坚决砍仓", font=f_body, fill=(220, 230, 245))
d.text((160, 630), "· 资金行为：良性平仓，股价跌杠杆降", font=f_body, fill=(220, 230, 245))
d.text((160, 750), "结论：标准健康的真出清！", font=f_h2, fill=(76, 175, 80))

# Right Card: Wave 2
d.rounded_rectangle([(1000, 180), (1800, 880)], radius=16, fill=(45, 20, 40), outline=(255, 82, 82), width=2)
d.text((1040, 220), "【第二波：国庆后深跌波】", font=f_h2, fill=(255, 82, 82))
d.text((1040, 300), "性质：假摔与机构死扛补仓", font=f_h3, fill=(255, 255, 255))
d.text((1040, 380), "· 指数下跌：深达 -29% ~ -30%", font=f_body, fill=(220, 230, 245))
d.text((1040, 460), "· 全市场融资：仅微降 -7.23%！", font=f_h2, fill=(255, 82, 82))
d.text((1040, 550), "· 资金行为：误判反弹，资金耗光抗单", font=f_body, fill=(220, 230, 245))
d.text((1040, 630), "· 筹码状态：2.35万亿两融死死套在高位", font=f_body, fill=(220, 230, 245))
d.text((1040, 750), "结论：危机四伏的假摔死扛！", font=f_h2, fill=(255, 82, 82))
img.save(os.path.join(SLIDES_DIR, "slide_03.png"))

# 04. 7月第一波出清数据大字卡
img, d = base_slide("第一波解构", "2026.06.25 - 2026.07.31：良性真出清")
d.text((120, 180), "第一波全市场融资净出清：", font=f_h2, fill=(200, 215, 240))
d.text((120, 260), "-4,210.8 亿元", font=ImageFont.truetype(font_bold, 120), fill=(76, 175, 80))
d.text((120, 430), "（从 3.010 万亿元 骤降至 2.589 万亿元，单月去化 -13.99%）", font=f_h3, fill=(150, 180, 220))

d.rounded_rectangle([(120, 540), (1800, 880)], radius=16, fill=(18, 32, 65), outline=(40, 70, 130), width=1)
d.text((160, 580), "· 创业板指同期跌幅： -23.51%", font=f_h2, fill=(255, 255, 255))
d.text((160, 670), "· 通信 ETF（515880）复权跌幅： -38.18%", font=f_h2, fill=(255, 255, 255))
d.text((160, 760), "· 科创芯片 ETF（588200）复权跌幅： -32.23%", font=f_h2, fill=(255, 255, 255))
d.text((160, 835), "特点：高位获利盘汹涌止损，被动平仓与主动降杠杆并举，出清相当果断", font=f_body, fill=(0, 229, 255))
img.save(os.path.join(SLIDES_DIR, "slide_04.png"))

# 05. 杠杆弹性对比卡 (第一波)
img, d = base_slide("量化指标", "两融去化弹性（Elasticity）的健康基准")
d.text((120, 170), "第一波杠杆弹性（两融跌幅 / 指数跌幅）：", font=f_h2, fill=(200, 215, 240))
d.text((120, 250), "0.58", font=ImageFont.truetype(font_bold, 130), fill=(0, 229, 255))
d.text((500, 320), "（健康合理区间，杠杆平稳跟随撤退）", font=f_h3, fill=(150, 200, 230))

d.rounded_rectangle([(120, 480), (1800, 880)], radius=16, fill=(16, 30, 60), outline=(0, 229, 255), width=2)
d.text((160, 520), "【什么是杠杆去化弹性？】", font=f_h2, fill=(255, 215, 0))
d.text((160, 600), "· 弹性 = 全市场融资余额降幅 ÷ 核心指数跌幅", font=f_h3, fill=(255, 255, 255))
d.text((160, 680), "· 当弹性在 0.5 ~ 0.8 时：说明指数每跌1%，就有0.5%~0.8%的杠杆平仓离场；", font=f_body, fill=(220, 230, 245))
d.text((160, 760), "· 资金没有死扛，风险在下跌过程中被动态释放，市场自我修复能力强。", font=f_body, fill=(220, 230, 245))
img.save(os.path.join(SLIDES_DIR, "slide_05.png"))

# 06. 10月第二波假摔死扛数据大字卡
img, d = base_slide("第二波异象", "2026.09.22 - 2026.10.30：指数暴跌，融资死扛")
d.text((120, 170), "第二波指数跌得更凶，但融资仅微降：", font=f_h2, fill=(200, 215, 240))
d.text((120, 250), "-7.23%", font=ImageFont.truetype(font_bold, 130), fill=(255, 82, 82))
d.text((650, 320), "（国庆节后仅减少 -1,837 亿元，死扛抗单！）", font=f_h3, fill=(255, 120, 120))

d.rounded_rectangle([(120, 480), (1800, 880)], radius=16, fill=(40, 20, 35), outline=(255, 82, 82), width=1)
d.text((160, 520), "· 创业板指暴跌： -29.01% （比7月第一波跌得更深！）", font=f_h2, fill=(255, 255, 255))
d.text((160, 610), "· 科创50指数暴跌： -30.28% （彻底击穿前低破位！）", font=f_h2, fill=(255, 255, 255))
d.text((160, 700), "· 通信 ETF（515880）暴跌： -38.90% （一个月内几近腰斩）", font=f_h2, fill=(255, 255, 255))
d.text((160, 790), "· 科创芯片 ETF（588200）暴跌： -34.93%", font=f_h2, fill=(255, 255, 255))
img.save(os.path.join(SLIDES_DIR, "slide_06.png"))

# 07. 杠杆弹性暴跌至冰点
img, d = base_slide("量化断层", "杠杆弹性从 0.58 暴跌至 0.24：两融钝化")
d.text((120, 170), "第二波杠杆去化弹性断崖跳水：", font=f_h2, fill=(200, 215, 240))
d.text((120, 250), "0.58  ➔  0.24", font=ImageFont.truetype(font_bold, 120), fill=(255, 82, 82))

d.rounded_rectangle([(120, 460), (1800, 880)], radius=16, fill=(20, 25, 55), outline=(255, 179, 0), width=2)
d.text((160, 500), "【弹性暴跌意味着什么？】", font=f_h2, fill=(255, 215, 0))
d.text((160, 580), "1. 钝化脱节：指数暴跌30%，融资盘只肯撤退7%，去杠杆速度落后股价4倍！", font=f_h3, fill=(240, 240, 250))
d.text((160, 670), "2. 机构误判：8-9月反弹时机构错当牛市第二波，将富余资金全用于补仓；", font=f_h3, fill=(240, 240, 250))
d.text((160, 760), "3. 筹码套死：2.35万亿两融杠杆几乎没有主动止损，全部悬在半山腰死扛！", font=f_h3, fill=(255, 82, 82))
img.save(os.path.join(SLIDES_DIR, "slide_07.png"))

# 08. 两波对比总览图 chart4
embed_chart_slide(
    "图表4 · 专题走势",
    "两波下跌走势轨迹与核心量化指标柱状矩阵对比",
    "chart4_two_waves_deep_dive.png",
    "【复权走势对比】第一波真出清（砍4211亿） vs 第二波深跌但融资死扛（弹性跌至0.24）",
    "slide_08.png"
)

# 09. 3.4节 33只半导体设备材料ETF全量验证
img, d = base_slide("3.4节全量印证", "全市场33只半导体/材料/设备ETF全量穿透")
d.text((120, 160), "“ETF死扛不降反增”是不是单一巨无霸的孤例？", font=f_title, fill=(255, 215, 0))
d.text((120, 250), "——我们对全市场2026年前上市的33只半导体ETF进行了全量测算！", font=f_h3, fill=(200, 225, 255))

d.rounded_rectangle([(120, 340), (1800, 880)], radius=16, fill=(15, 28, 60), outline=(0, 229, 255), width=1)
d.text((160, 380), "· 验证样本：涵盖半导体材料、半导体设备、科创半导体、芯片全系列", font=f_h3, fill=(255, 255, 255))
d.text((160, 480), "· 发现一：2026年全市场弹性之王确为【半导体材料设备】板块", font=f_h3, fill=(0, 229, 255))
d.text((160, 580), "· 发现二：细分品种两融体量极度庞大（单只ETF融资达14~19亿元）", font=f_h3, fill=(255, 255, 255))
d.text((160, 680), "· 发现三：在第二波大跌超30%~40%时，多数细分ETF两融逆势暴涨！", font=f_h3, fill=(255, 82, 82))
d.text((160, 780), "结论：死扛抗单绝非个案，而是横跨整个科技ETF矩阵的行业性集体行为！", font=f_h2, fill=(255, 215, 0))
img.save(os.path.join(SLIDES_DIR, "slide_09.png"))

# 10. 细分ETF弹性榜TOP
img, d = base_slide("细分榜单", "2026年半导体材料设备 ETF 涨幅榜 TOP 4")
# Table headers
y_t = 180
d.rounded_rectangle([(120, y_t), (1800, y_t + 70)], radius=8, fill=(25, 45, 90))
d.text((150, y_t + 18), "ETF 代码与名称", font=f_h3, fill=(0, 229, 255))
d.text((650, y_t + 18), "2026年峰值涨幅", font=f_h3, fill=(0, 229, 255))
d.text((1050, y_t + 18), "第二波暴跌跌幅", font=f_h3, fill=(0, 229, 255))
d.text((1450, y_t + 18), "最新融资余额", font=f_h3, fill=(0, 229, 255))

rows = [
    ("科创半导 ETF (588170.SH)", "+163.97%", "-38.56%", "19.13 亿元"),
    ("半导体设备 ETF (159558.SZ)", "+144.95%", "-39.80%", "3.52 亿元"),
    ("半导设备 ETF (560780.SH)", "+110.07%", "-40.85%", "2.41 亿元"),
    ("半导设备 ETF (159516.SZ)", "+98.35%", "-40.91%", "14.27 亿元")
]
y_t += 90
for name, p_up, p_dn, margin in rows:
    d.rounded_rectangle([(120, y_t), (1800, y_t + 115)], radius=10, fill=(16, 30, 65), outline=(40, 60, 110), width=1)
    d.text((150, y_t + 35), name, font=f_h3, fill=(255, 255, 255))
    d.text((680, y_t + 35), p_up, font=f_h2, fill=(255, 82, 82))
    d.text((1080, y_t + 35), p_dn, font=f_h2, fill=(76, 175, 80))
    d.text((1470, y_t + 35), margin, font=f_h2, fill=(255, 215, 0))
    y_t += 135
img.save(os.path.join(SLIDES_DIR, "slide_10.png"))

# 11. 行业集体死扛铁证
img, d = base_slide("逆势狂飙", "股价大跌超40%，细分ETF融资盘逆势暴增！")
d.text((120, 180), "第二波暴跌期间部分细分 ETF 融资余额变动：", font=f_h2, fill=(200, 215, 240))
cards_data = [
    ("芯片 ETF (159995.SZ)", "股价暴跌 -30.5%", "两融余额逆势增加", "+8.52%", (255, 82, 82)),
    ("半导体 (512480.SH)", "股价暴跌 -31.2%", "两融余额逆势增加", "+14.10%", (255, 82, 82)),
    ("科创芯片 (588200.SH)", "股价暴跌 -34.9%", "融资飙至历史新天量", "20.90 亿元", (255, 215, 0))
]
x_c = 120
for title, sub1, sub2, num, col in cards_data:
    d.rounded_rectangle([(x_c, 300), (x_c + 530, 850)], radius=16, fill=(18, 30, 65), outline=col, width=2)
    d.text((x_c + 40, 340), title, font=f_h3, fill=(255, 255, 255))
    d.text((x_c + 40, 420), sub1, font=f_body, fill=(180, 200, 230))
    d.line([(x_c + 40, 490), (x_c + 490, 490)], fill=(40, 60, 100), width=1)
    d.text((x_c + 40, 530), sub2, font=f_body, fill=(200, 220, 240))
    d.text((x_c + 40, 620), num, font=ImageFont.truetype(font_bold, 70), fill=col)
    x_c += 560
img.save(os.path.join(SLIDES_DIR, "slide_11.png"))

# 12. 全市场融资剪刀差总览 chart1
embed_chart_slide(
    "图表1 · 剪刀差总览",
    "全市场融资余额与双创代表指数走势对比图",
    "chart1_deleveraging_vs_price.png",
    "【剪刀差张开】指数下泄斜率极度拉陡，但两融曲线走平钝化，2.35万亿套在高位",
    "slide_12.png"
)

# 13. 第6节 易中天三巨头腰斩大字卡
img, d = base_slide("个股腰斩", "龙头科技股融资盘血流成河：净蒸发452亿！")
d.text((120, 160), "“易中天”通信三巨头融资余额暴跌：", font=f_h2, fill=(200, 215, 240))
d.text((120, 240), "-451.8 亿元 (-53.75%)", font=ImageFont.truetype(font_bold, 110), fill=(76, 175, 80))
d.text((120, 390), "（从 6月底 840.49 亿元断崖跌至最新 388.70 亿元，完美跟随股价暴跌）", font=f_h3, fill=(150, 180, 220))

d.rounded_rectangle([(120, 490), (1800, 880)], radius=16, fill=(18, 30, 60), outline=(40, 70, 120), width=1)
d.text((160, 530), "· 新易盛 (300502)：股价跌 -49.8%，融资由 209.8 亿跌至 128.2 亿 (-38.9%)", font=f_h3, fill=(240, 240, 250))
d.text((160, 630), "· 中际旭创 (300308)：股价跌 -37.3%，融资由 326.4 亿跌至 204.8 亿 (弹性刚好 1.00！)", font=f_h3, fill=(255, 215, 0))
d.text((160, 730), "· 天孚通信 (300394)：股价跌 -41.4%，融资由 75.9 亿降至 55.7 亿 (-26.6%)", font=f_h3, fill=(240, 240, 250))
d.text((160, 815), "个股去杠杆异常冷血与决绝，大机构资金从个股层面全面溃逃！", font=f_body, fill=(0, 229, 255))
img.save(os.path.join(SLIDES_DIR, "slide_13.png"))

# 14. 寒武纪中芯跳水 vs 科创芯片逆势新高
img, d = base_slide("惊天背离", "半导体个股腰斩 vs 科创芯片ETF融资创历史新高！")
# Left: 寒武纪
d.rounded_rectangle([(120, 180), (920, 880)], radius=16, fill=(18, 30, 60), outline=(76, 175, 80), width=2)
d.text((160, 220), "【个股被动斩仓：寒武纪】", font=f_h2, fill=(76, 175, 80))
d.text((160, 310), "· 峰值融资余额： 260.9 亿元", font=f_h3, fill=(255, 255, 255))
d.text((160, 390), "· 最新融资余额： 138.9 亿元", font=f_h3, fill=(255, 255, 255))
d.text((160, 480), "· 融资累计缩减： -46.75%", font=f_h2, fill=(76, 175, 80))
d.text((160, 570), "· 两融弹性： 1.13 ~ 1.23", font=f_h3, fill=(255, 215, 0))
d.text((160, 660), "特点：跟随股价同步腰斩，买盘被完全抽干", font=f_body, fill=(200, 220, 240))

# Right: 科创芯片ETF
d.rounded_rectangle([(1000, 180), (1800, 880)], radius=16, fill=(45, 20, 35), outline=(255, 82, 82), width=2)
d.text((1040, 220), "【ETF逆势被买爆：科创芯片】", font=f_h2, fill=(255, 82, 82))
d.text((1040, 310), "· 第一波逆势大增： +30.17%", font=f_h3, fill=(255, 255, 255))
d.text((1040, 390), "· 第二波逆势再增： +4.41%", font=f_h3, fill=(255, 255, 255))
d.text((1040, 480), "· 历史天量峰值： 20.90 亿元", font=f_h2, fill=(255, 82, 82))
d.text((1040, 570), "· 全周期累积增加： +28.10%", font=f_h3, fill=(255, 215, 0))
d.text((1040, 660), "特点：股价暴跌40%，融资余额反而创历史新高！", font=f_body, fill=(255, 215, 0))
img.save(os.path.join(SLIDES_DIR, "slide_14.png"))

# 15. 个股腰斩 vs ETF买爆背离图 chart5
embed_chart_slide(
    "图表5 · 核心背离",
    "个股融资同步腰斩 vs ETF逆势抗单分歧对比图",
    "chart5_individual_stocks_vs_etf_margin.png",
    "【核心真相】“易中天”融资蒸发452亿腰斩，而科创芯片ETF逆势飙至20.9亿历史新高！",
    "slide_15.png"
)

# 16. 券商风控内幕揭秘 1
img, d = base_slide("风控机制①", "为什么个股买盘被强行锁死？")
d.text((120, 160), "底牌一：单一股票持仓集中度 20%~30% 铁律", font=f_title, fill=(255, 215, 0))
d.rounded_rectangle([(120, 260), (1800, 880)], radius=16, fill=(16, 28, 60), outline=(0, 229, 255), width=2)
d.text((160, 320), "1. 证监会及券商合规规则规定：", font=f_h2, fill=(0, 229, 255))
d.text((160, 400), "   单一信用账户对单只个股的持仓市值，不得超过总资产的 20%~30%；", font=f_h3, fill=(240, 240, 250))
d.text((160, 510), "2. 预警线一触即切断：", font=f_h2, fill=(255, 82, 82))
d.text((160, 590), "   当易中天或寒武纪暴跌、账户维保比例逼近 140%-150% 预警线时，", font=f_h3, fill=(240, 240, 250))
d.text((160, 670), "   风控系统立刻自动锁定！【彻底剥夺该账户继续买入该个股的权限】；", font=f_h3, fill=(255, 82, 82))
d.text((160, 780), "3. 结果：操盘手即使想补仓也买不进个股，只能看着跌破130%被动平仓！", font=f_h2, fill=(255, 215, 0))
img.save(os.path.join(SLIDES_DIR, "slide_16.png"))

# 17. 券商风控内幕揭秘 2
img, d = base_slide("风控机制②", "为什么机构全把钱砸进 ETF？")
d.text((120, 160), "底牌二：ETF 无集中度限制 ＋ 抵押折算率高达 90%！", font=f_title, fill=(0, 229, 255))
d.rounded_rectangle([(120, 260), (1800, 880)], radius=16, fill=(16, 32, 65), outline=(255, 179, 0), width=2)
d.text((160, 320), "1. ETF 属于一篮子分散投资：", font=f_h2, fill=(0, 229, 255))
d.text((160, 400), "   券商合规【完全不设单一集中度限制】！客户可将 70%~100% 额度全押单只ETF；", font=f_h3, fill=(240, 240, 250))
d.text((160, 510), "2. 担保品折算率天差地别：", font=f_h2, fill=(255, 215, 0))
d.text((160, 590), "   · 科技类个股折算率仅 50%~60%（暴跌时甚至被券商直接下调为 0%！）", font=f_h3, fill=(200, 220, 240))
d.text((160, 670), "   · 而宽基与科技 ETF 担保折算率高达 85% ~ 90%！", font=f_h2, fill=(76, 175, 80))
d.text((160, 780), "3. 极限加杠杆：机构拿100元ETF抵押能借出90元，成为死扛借钱的唯一通道！", font=f_h2, fill=(255, 215, 0))
img.save(os.path.join(SLIDES_DIR, "slide_17.png"))

# 18. 机构乾坤大挪移机制图
img, d = base_slide("资金流向", "操盘手的“乾坤大挪移”：科技ETF沦为终极堰塞湖")
d.rounded_rectangle([(120, 180), (1800, 880)], radius=16, fill=(20, 30, 60), outline=(255, 82, 82), width=2)
steps = [
    ("步骤 1：个股爆仓", "易中天/寒武纪触碰风控红线，个股买盘被锁死，个股融资暴跌50%", (255, 82, 82)),
    ("步骤 2：乾坤大挪移", "操盘手为维持多头敞口，把追加保证金与所有可用信贷全砸进 ETF", (255, 193, 7)),
    ("步骤 3：ETF被买爆", "科创芯片/通信ETF两融逆势创20.9亿新高，全行业33只ETF集体死扛", (0, 229, 255)),
    ("危险结果：终极堰塞湖", "散户与个股杠杆已砍半，但机构死扛的所有残余筹码全挤在ETF里，一旦决口毁灭性极大！", (255, 50, 50))
]
y_s = 220
for tit, sub_txt, col in steps:
    d.text((160, y_s), tit, font=f_h2, fill=col)
    d.text((160, y_s + 60), sub_txt, font=f_body, fill=(220, 235, 255))
    y_s += 160
img.save(os.path.join(SLIDES_DIR, "slide_18.png"))

# 19. 第4节 极速狂泻
img, d = base_slide("暴跌速度", "10月下旬单日暴跌速度：金融史上极其罕见的下泄")
d.text((120, 170), "通信 ETF 与科创芯片 ETF 6日冲刺下杀跌速：", font=f_h2, fill=(200, 215, 240))
d.text((120, 250), "-3.19% / 日", font=ImageFont.truetype(font_bold, 130), fill=(255, 82, 82))
d.text((850, 320), "（短短6天内累计重挫 -16%，局部毁灭性狂泻）", font=f_h3, fill=(255, 140, 140))

d.rounded_rectangle([(120, 480), (1800, 880)], radius=16, fill=(35, 20, 35), outline=(255, 82, 82), width=1)
d.text((160, 530), "· 创业板指 6日跌速： -2.02% / 日 （大盘宽基共振杀跌）", font=f_h2, fill=(255, 255, 255))
d.text((160, 630), "· 科创50指数 6日跌速： -2.75% / 日 （大机构防线全线失守）", font=f_h2, fill=(255, 255, 255))
d.text((160, 730), "· 杀跌动力：国债跳水抽干流动性 + 机构补仓失败转入被动杀跌", font=f_h3, fill=(0, 229, 255))
d.text((160, 810), "在缺乏接盘资金的真空状态下，科技核心品种呈现自由落体式断崖！", font=f_body, fill=(255, 215, 0))
img.save(os.path.join(SLIDES_DIR, "slide_19.png"))

# 20. 历史对标对决卡
img, d = base_slide("全球对比", "横向对决全球著名股灾：比美股世纪熔断猛一倍多！")
# Card Left: 2020 美股熔断
d.rounded_rectangle([(120, 180), (920, 880)], radius=16, fill=(18, 30, 60), outline=(0, 229, 255), width=2)
d.text((160, 220), "2020 美股全球疫情熔断", font=f_h2, fill=(0, 229, 255))
d.text((160, 310), "· 历史背景：全球疫情恐慌 + 4次熔断", font=f_body, fill=(200, 220, 240))
d.text((160, 400), "· 持续交易日： 24 天", font=f_body, fill=(200, 220, 240))
d.text((160, 490), "· 累计跌幅： -33.92%", font=f_h3, fill=(255, 255, 255))
d.text((160, 600), "日均下跌速度：", font=f_h3, fill=(200, 220, 240))
d.text((160, 680), "-1.47% / 日", font=ImageFont.truetype(font_bold, 80), fill=(0, 229, 255))

# Card Right: 2026 双创冲刺
d.rounded_rectangle([(1000, 180), (1800, 880)], radius=16, fill=(45, 20, 35), outline=(255, 82, 82), width=2)
d.text((1040, 220), "2026 A股双创科技冲刺杀跌", font=f_h2, fill=(255, 82, 82))
d.text((1040, 310), "· 历史背景：国债跳水 + ETF流动性抽水", font=f_body, fill=(240, 200, 200))
d.text((1040, 400), "· 持续交易日： 6 天", font=f_body, fill=(240, 200, 200))
d.text((1040, 490), "· 累计跌幅： -15.95%", font=f_h3, fill=(255, 255, 255))
d.text((1040, 600), "日均下跌速度：", font=f_h3, fill=(240, 200, 200))
d.text((1040, 680), "-3.19% / 日", font=ImageFont.truetype(font_bold, 90), fill=(255, 82, 82))
d.text((1040, 800), "【速度对比】比2020美股熔断快 2.17 倍！", font=f_h3, fill=(255, 215, 0))
img.save(os.path.join(SLIDES_DIR, "slide_20.png"))

# 21. 历史暴跌速度天梯图 chart2
embed_chart_slide(
    "图表2 · 速度排行",
    "全球金融重大历史股灾日均暴跌速度横向天梯榜",
    "chart2_velocity_comparison.png",
    "【历史天梯】单日 -3.19% 跌速在金融史上仅次于 2015 股灾第二波，碾压 2000 科技泡沫！",
    "slide_21.png"
)

# 22. 流动性底牌打穿
img, d = base_slide("流动性警报", "终极底牌打穿：30年国债期货单日暴跌 1%！")
d.text((120, 170), "2026年10月30日市场最反常异象：", font=f_h2, fill=(200, 215, 240))
d.rounded_rectangle([(120, 250), (920, 500)], radius=16, fill=(35, 20, 40), outline=(255, 82, 82), width=2)
d.text((160, 290), "30年国债 ETF (511090)", font=f_h2, fill=(255, 255, 255))
d.text((160, 370), "单日破位暴跌 -1.00%", font=ImageFont.truetype(font_bold, 65), fill=(255, 82, 82))

d.rounded_rectangle([(1000, 250), (1800, 500)], radius=16, fill=(35, 20, 40), outline=(255, 179, 0), width=2)
d.text((1040, 290), "黄金 ETF (518880)", font=f_h2, fill=(255, 255, 255))
d.text((1040, 370), "单日同步下挫 -1.33%", font=ImageFont.truetype(font_bold, 65), fill=(255, 193, 7))

d.rounded_rectangle([(120, 540), (1800, 880)], radius=16, fill=(18, 30, 60), outline=(0, 229, 255), width=1)
d.text((160, 580), "国债和黄金是一切金融机构最安全的压箱底流动性避风港！", font=f_h2, fill=(0, 229, 255))
d.text((160, 670), "大机构为何连国债黄金都要无差别砸盘变现？", font=f_h3, fill=(255, 255, 255))
d.text((160, 760), "答案：机构手头闲置流动性耗尽，只能砸锅卖铁筹集保证金填补科技ETF窟窿！", font=f_h2, fill=(255, 215, 0))
img.save(os.path.join(SLIDES_DIR, "slide_22.png"))

# 23. 抵押品见底救火
img, d = base_slide("连锁踩踏", "拆东墙补西墙：流动性挤兑传导链条")
d.rounded_rectangle([(120, 180), (1800, 880)], radius=16, fill=(20, 28, 55), outline=(255, 179, 0), width=2)
chain = [
    ("1. 科技股持续阴跌加速", "重仓机构在个股与ETF上维保比例跌向 130% 强平线"),
    ("2. 账户可用现金耗尽", "前期反弹阶段补仓打光了所有闲置头寸"),
    ("3. 被迫抛售最优质避险资产", "不惜砸穿 30年国债与现货黄金，强制变现补窟窿"),
    ("4. 终极危机爆发", "国债跳水 ➔ 流动性全线抽水 ➔ ETF补仓资金彻底断流 ➔ 诱发二次强平")
]
y_c = 220
for tit, desc in chain:
    d.text((160, y_c), tit, font=f_h2, fill=(255, 215, 0))
    d.text((160, y_c + 60), desc, font=f_h3, fill=(230, 240, 255))
    y_c += 155
img.save(os.path.join(SLIDES_DIR, "slide_23.png"))

# 24. 国债黄金流动性穿透图 chart3
embed_chart_slide(
    "图表3 · 流动性穿透",
    "30年国债跳水与黄金下挫对标科技ETF暴跌全景图",
    "chart3_liquidity_transmission_bonds_gold.png",
    "【流动性极限】大机构抵押品见底，连国债与黄金都被迫抛售变现救火！",
    "slide_24.png"
)

# 25. 去杠杆到底到没到位？
img, d = base_slide("终极结论", "研报量化裁决：去杠杆到底到唔到位？")
d.text((120, 160), "斩钉截铁结论：", font=f_h2, fill=(200, 215, 240))
d.text((120, 230), "绝对远远没有到位！", font=ImageFont.truetype(font_bold, 110), fill=(255, 82, 82))

d.rounded_rectangle([(120, 390), (1800, 880)], radius=16, fill=(16, 28, 60), outline=(255, 82, 82), width=2)
d.text((160, 440), "【真正的左侧见底信号是什么？】", font=f_h2, fill=(255, 215, 0))
d.text((160, 530), "1. 融资规模必须出现断崖：全市场融资余额至少需要单月断崖缩减 3000-5000 亿；", font=f_h3, fill=(240, 240, 250))
d.text((160, 630), "2. 科技ETF堰塞湖必须决口：科创芯片等ETF融资余额必须出现一次集中恐慌踩踏出清；", font=f_h3, fill=(240, 240, 250))
d.text((160, 730), "3. 杠杆比率回落：全市场融资占流通市值比从当前的 3.01% 回落至 2.4% 以下的冷清区间。", font=f_h3, fill=(240, 240, 250))
d.text((160, 810), "未见上述信号前的任何反弹，本质上都只是死扛机构的诱多自救！", font=f_body, fill=(255, 82, 82))
img.save(os.path.join(SLIDES_DIR, "slide_25.png"))

# 26. 终极预警：徒手接飞刀
img, d = base_slide("风险警示", "敬畏市场，管住双手：严禁盲目左侧抄底！")
d.rounded_rectangle([(120, 180), (1800, 880)], radius=16, fill=(35, 15, 25), outline=(255, 50, 50), width=3)
d.text((160, 240), "【重大风险警示】", font=ImageFont.truetype(font_bold, 55), fill=(255, 82, 82))
d.text((160, 340), "· 巨大惯性向下时，任何抢跑抄底本质上都是在帮机构死扛接飞刀！", font=f_h2, fill=(255, 255, 255))
d.text((160, 450), "· 机构之所以还在抗单，是因为还没触发最终的全面被动强平；", font=f_h3, fill=(230, 230, 245))
d.text((160, 550), "· 一旦流动性支持彻底断流，ETF融资堰塞湖一旦决堤，", font=f_h3, fill=(230, 230, 245))
d.text((160, 630), "  最后那一波踩踏出清的杀伤力将远超第一波！", font=f_h2, fill=(255, 193, 7))
d.text((160, 750), "保留子弹，等待恐慌盘与杠杆彻底出清，才是活下去的唯一法则。", font=f_h2, fill=(0, 229, 255))
img.save(os.path.join(SLIDES_DIR, "slide_26.png"))

# 27. 结尾思考与开源链接
img, d = base_slide("深思收尾", "当避险资产卖无可卖，下一个流动性黑洞在哪？")
d.rounded_rectangle([(120, 180), (1800, 880)], radius=16, fill=(16, 26, 56), outline=(0, 229, 255), width=2)
d.text((160, 230), "【终极悬念留给读者深思】", font=f_h2, fill=(255, 215, 0))
d.text((160, 320), "当大机构连 30年国债和现货黄金都已卖无可卖、退无可退时，", font=f_h2, fill=(255, 255, 255))
d.text((160, 410), "下一个被波及崩塌的避险资产又会是谁？整个市场的黑洞会蔓延到哪？", font=f_h2, fill=(0, 229, 255))

d.line([(160, 520), (1760, 520)], fill=(40, 60, 100), width=1)
d.text((160, 560), "本研究完整研报、高清图表与复现代码已全部开源至 GitHub：", font=f_h3, fill=(220, 230, 250))
d.text((160, 640), "https://github.com/B1ueAkisa/AShare-Deleveraging-Analysis", font=ImageFont.truetype(font_bold, 42), fill=(255, 215, 0))
d.text((160, 750), "数据驱动 · 深度量化 · 感谢收看，欢迎点赞交流！", font=f_h2, fill=(76, 175, 80))
img.save(os.path.join(SLIDES_DIR, "slide_27.png"))

print("27 dynamic slides created successfully!")
