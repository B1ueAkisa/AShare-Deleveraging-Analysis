import urllib.request
import json

# Eastmoney margin balance API
# http://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPTA_RZRQ_LSHJ&columns=ALL&filter=(DIM_DATE%3E%272026-10-15%27)&pageNumber=1&pageSize=20&sortTypes=-1&sortColumns=DIM_DATE
url = "http://datacenter-web.eastmoney.com/api/data/v1/get?reportName=RPTA_RZRQ_LSHJ&columns=ALL&pageNumber=1&pageSize=10&sortTypes=-1&sortColumns=DIM_DATE"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        data = res['result']['data']
        for d in data[:6]:
            print(f"Date: {d.get('DIM_DATE')} | Total RZ: {d.get('RZYE')} | SH RZ: {d.get('RZYE_SH')} | SZ RZ: {d.get('RZYE_SZ')} | Total RZRQ: {d.get('RZRQYE')}")
except Exception as e:
    print("Error:", e)
