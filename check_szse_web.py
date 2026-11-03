import urllib.request
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

url = "http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1837_xxpl&TABKEY=tab1"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode('utf-8'))
        print("SZSE margin summary latest:")
        for row in data[0]['data'][:5]:
            print(row)
except Exception as e:
    print("Error fetching SZSE:", e)
