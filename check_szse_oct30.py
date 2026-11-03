import urllib.request
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

dates = ['2026-10-30', '2026-10-29', '2026-10-28']
for d in dates:
    url = f"http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1837_xxpl&TABKEY=tab1&txtDate={d}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            meta = data[0].get('metadata', {})
            print(f"Date: {d} | subname: {meta.get('subname')} | rows: {len(data[0]['data'])}")
            if len(data[0]['data']) > 0:
                print(f"Data: {data[0]['data'][0]}")
    except Exception as e:
        print(f"Error for {d}: {e}")
