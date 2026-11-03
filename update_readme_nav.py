with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

nav = """
## 📑 报告系列导航 (Report Series Navigation)
- 📘 **[Part 1: A股双创两波去杠杆宏观测算与历史暴跌速度对比](A股双创去杠杆与历史暴跌速度对比研究_Part1.md)**
  - 双波暴跌结构解构、对比 2008 / 2015 / 纳斯达克 2000、30年国债与黄金的流动性传导链条
- 📗 **[Part 2: 个股融资“断崖死降”与双创ETF“逆势翻倍”的杠杆大迁移剖析](A股双创去杠杆与历史暴跌速度对比研究_Part2.md)**
  - 30只核心科技股失血 870 亿 vs ETF 逆势扩张 100 亿，迁移率 12%~15% 的避风港假象
- 📕 **[Part 3: 决堤之日——科技ETF“避难所”失守与全线强平压力测试 (2026-11-03 最新复盘)](A股双创去杠杆与历史暴跌速度对比研究_Part3.md)**
  - 11-03 科技核心全线暴跌（天孚-12.8%、中际-12.7%、多只跌停）、ETF避难所失守（通信ETF-7.36%）、二次强平测算与30年国债避险虹吸

---
"""

badge = "[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)"

if badge in content:
    idx = content.find(badge) + len(badge)
    new_content = content[:idx] + "\n" + nav + "\n" + content[idx:].strip()
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("README.md updated!")
else:
    print("Badge not found")
