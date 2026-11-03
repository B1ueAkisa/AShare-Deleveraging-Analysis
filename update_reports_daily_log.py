# Update Part 1
with open('A股双创去杠杆与历史暴跌速度对比研究_Part1.md', 'r', encoding='utf-8') as f:
    p1 = f.read()

p1_daily_log = """
---

## 七、 盘后动态跟踪（每日速记）

* **2026-11-02（周一）**：全市场两融跌破 2.3 万亿关口（22,951 亿元）；科创50 ETF 融资余额逆势冲上 **50.77 亿元历史最高峰**，通信 ETF 融资升至 10.75 亿元，呈现明显的弱反弹诱多与 ETF 避险抗单特征。
* **2026-11-03（周二）**：科技权重遭遇毁灭性无差别暴跌（天孚 -12.80%、旭创 -12.69%、寒武纪 -10.81%、生益科技跌停），通信 ETF 暴跌 **-7.36%**、科创半导暴跌 **-6.16%**；新易盛自历史顶累计跌幅达 **-78.82%**，ETF 避难所全面决堤，30年国债 ETF 逆势涨 **+0.60%**（收盘 121.31）避险。
"""

if "## 七、 盘后动态跟踪" not in p1:
    p1 = p1.strip() + "\n" + p1_daily_log
    with open('A股双创去杠杆与历史暴跌速度对比研究_Part1.md', 'w', encoding='utf-8') as f:
        f.write(p1)
    print("Part 1 updated with daily log!")
else:
    print("Part 1 already has daily log.")

# Update Part 2
with open('A股双创去杠杆与历史暴跌速度对比研究_Part2.md', 'r', encoding='utf-8') as f:
    p2 = f.read()

p2_daily_log = """
---

## 六、 盘后动态跟踪（每日速记）

* **2026-11-02（周一）**：个股撤出杠杆继续向 ETF 搬家，科创50 ETF（588000）融资余额突破 **50.77 亿元** 刷新历史天量，寒武纪两融逆势增至 140.58 亿元，ETF 避风港拥挤度达到极限。
* **2026-11-03（周二）**：避风港神话破灭引发二次踩踏，通信 ETF 单日重挫 **-7.36%**，科创半导重挫 **-6.16%**，生益科技等跌停；由于个股跌停无法出逃，抛压集中倾泻至高流动性的 ETF 标的，避难所宣告决堤。
"""

if "## 六、 盘后动态跟踪" not in p2:
    p2 = p2.strip() + "\n" + p2_daily_log
    with open('A股双创去杠杆与历史暴跌速度对比研究_Part2.md', 'w', encoding='utf-8') as f:
        f.write(p2)
    print("Part 2 updated with daily log!")
else:
    print("Part 2 already has daily log.")
