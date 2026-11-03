import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Referer': 'http://www.sse.com.cn/'}
url = "http://query.sse.com.cn/commonQuery.do?isPagination=false&sqlId=COMMON_SSE_SJ_GPSJ_CJGK_MRGK_L"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        txt = resp.read().decode('utf-8')
        data = json.loads(txt)
        res = data.get('pageHelp', {}).get('data', [])
        print("Latest SSE margin rows:", len(res))
        for r in res[:5]:
            print(r)
except Exception as e:
    print("Error:", e)
