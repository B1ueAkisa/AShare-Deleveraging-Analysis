import os
from PIL import Image, ImageDraw, ImageFont

def create_slides():
    os.makedirs(r'd:\AKFile\其他\投资\去杠杆与暴跌速度对比分析\video_production', exist_ok=True)
    out_dir = r'd:\AKFile\其他\投资\去杠杆与暴跌速度对比分析\video_production'
    src_dir = r'd:\AKFile\其他\投资\去杠杆与暴跌速度对比分析'
    
    font_bold = r'C:\Windows\Fonts\msyhbd.ttc'
    font_reg = r'C:\Windows\Fonts\msyh.ttc'
    
    f_title = ImageFont.truetype(font_bold, 70)
    f_sub = ImageFont.truetype(font_bold, 36)
    f_pill = ImageFont.truetype(font_bold, 24)
    f_header = ImageFont.truetype(font_bold, 40)
    f_footer = ImageFont.truetype(font_reg, 24)
    f_banner = ImageFont.truetype(font_bold, 28)

    # 1. Slide 1: Cover
    img1 = Image.new('RGB', (1920, 1080), color=(10, 17, 40))
    d1 = ImageDraw.Draw(img1)
    # Background accents
    d1.rectangle([(0, 0), (1920, 20)], fill=(0, 229, 255))
    d1.rectangle([(0, 1060), (1920, 1080)], fill=(255, 179, 0))
    # Subtle inner border
    d1.rectangle([(50, 50), (1870, 1030)], outline=(30, 45, 80), width=2)
    
    # Pills
    pills = ["交易所实盘清算库", "2.4万亿两融穿透", "两波下跌分段解构", "5次历史股灾对标"]
    x_pill = 120
    for p in pills:
        tw = d1.textlength(p, font=f_pill)
        d1.rounded_rectangle([(x_pill, 220), (x_pill + tw + 30, 270)], radius=10, fill=(20, 35, 70), outline=(0, 229, 255), width=1)
        d1.text((x_pill + 15, 230), p, font=f_pill, fill=(0, 229, 255))
        x_pill += int(tw + 50)
        
    # Title & Subtitle
    d1.text((120, 340), "A股双创科技去杠杆到底到没到位？", font=f_title, fill=(255, 255, 255))
    d1.text((120, 450), "科技ETF融资“堰塞湖”真相与历史暴跌速度全景量化穿透", font=f_sub, fill=(255, 193, 7))
    
    # Key points box
    d1.rounded_rectangle([(120, 560), (1800, 880)], radius=16, fill=(15, 25, 55), outline=(40, 60, 110), width=2)
    bullets = [
        "· 第一波与第二波本质差异：7月出清4200亿真去杠杆 vs 10月指数暴跌杠杆死扛补仓",
        "· 核心微观背离：“易中天”个股融资腰斩蒸发452亿，科技ETF两融却逆势暴增创新高！",
        "· 历史速度横向对标：局部日均跌速 -3.19%/日，仅次于2015股灾第二波，远超2020美股熔断",
        "· 流动性极限预警：30年国债跳水杀跌1%、黄金下挫，机构被迫抛售安全资产救火"
    ]
    y_b = 600
    for b in bullets:
        d1.text((160, y_b), b, font=ImageFont.truetype(font_reg, 30), fill=(220, 230, 245))
        y_b += 65
        
    d1.text((120, 950), "银河证券官方实盘数据 · 深度量化研究出品", font=f_footer, fill=(120, 140, 175))
    img1.save(os.path.join(out_dir, "slide1.png"))

    # Helper for chart slides
    def make_chart_slide(chart_name, header_title, banner_text, out_name):
        img = Image.new('RGB', (1920, 1080), color=(10, 17, 40))
        d = ImageDraw.Draw(img)
        
        # Header bar
        d.rectangle([(0, 0), (1920, 90)], fill=(16, 26, 58))
        d.rectangle([(0, 88), (1920, 90)], fill=(0, 229, 255))
        d.text((60, 22), header_title, font=f_header, fill=(255, 255, 255))
        
        # Load and resize chart
        chart_path = os.path.join(src_dir, chart_name)
        if os.path.exists(chart_path):
            c_img = Image.open(chart_path)
            # Target size: width 1800, max height 840
            max_w, max_h = 1800, 840
            c_img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
            cx = (1920 - c_img.width) // 2
            cy = 105 + (max_h - c_img.height) // 2
            img.paste(c_img, (cx, cy))
            
        # Bottom banner
        d.rectangle([(0, 990), (1920, 1080)], fill=(15, 25, 55))
        d.rectangle([(0, 990), (1920, 992)], fill=(255, 179, 0))
        d.text((60, 1015), banner_text, font=f_banner, fill=(255, 215, 0))
        img.save(os.path.join(out_dir, out_name))

    # Slide 2: 两波下跌解构 (chart4)
    make_chart_slide(
        "chart4_two_waves_deep_dive.png",
        "第一波是“真出清”，第二波是“假摔与死扛补仓”",
        "【量化实证】7月第一波出清4211亿 (-14.0%) | 10月第二波指数跌30%，融资仅微降7.2%，抗单钝化极其严重！",
        "slide2.png"
    )

    # Slide 3: 剪刀差总览 (chart1)
    make_chart_slide(
        "chart1_deleveraging_vs_price.png",
        "全市场融资剪刀差正在张开：杠杆与走势严重脱节",
        "【总量穿透】全市场融资余额高达2.35万亿，两融去化弹性由0.58断崖下跌至0.24，两融钝化未充分出清",
        "slide3.png"
    )

    # Slide 4: 个股 vs ETF 背离 (chart5)
    make_chart_slide(
        "chart5_individual_stocks_vs_etf_margin.png",
        "个股腰斩 vs 科技ETF融资创新高：制度风控下的惊天背离",
        "【核心真相】“易中天”融资净砍452亿(-53.8%) | 科创芯片ETF逆势创20.9亿历史新高！ETF成抗单堰塞湖",
        "slide4.png"
    )

    # Slide 5: 历史速度天梯 (chart2)
    make_chart_slide(
        "chart2_velocity_comparison.png",
        "历史暴跌速度横向天梯：局部下泄速度赶超2015股灾第二波",
        "【极速狂泻】通信与芯片ETF 6天日均暴跌 -3.19%/日！金融史上仅次于2015年8月股灾第二波，远超2020美股熔断",
        "slide5.png"
    )

    # Slide 6: 流动性穿透与警报 (chart3)
    make_chart_slide(
        "chart3_liquidity_transmission_bonds_gold.png",
        "流动性底牌打穿：30年国债跳水杀跌，去杠杆远未到位！",
        "【终极预警】机构抛售国债与黄金救火追加保证金，ETF融资堰塞湖未出清前，盲目左侧抄底极易接飞刀！",
        "slide6.png"
    )

    print("All 6 slides generated successfully in video_production folder.")

if __name__ == '__main__':
    create_slides()
