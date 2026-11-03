import urllib.request
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'http://www.sse.com.cn/'
}

# Query SSE margin summary
url = "http://query.sse.com.cn/marketdata/tradedata/queryMargin.do?isPagination=false&tabType=mxtab"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        txt = resp.read().decode('utf-8')
        print("SSE response snippet:", txt[:300])
except Exception as e:
    print("SSE summary error:", e)

# Also check date from another common SSE margin endpoint
url2 = "http://query.sse.com.cn/commonQuery.do?isPagination=false&sqlId=COMMON_SSE_SJ_GPSJ_CJGK_MRGK_L&trade_date=20261103"
req2 = urllib.request.Request(url2, headers=headers)
try:
    with urllib.request.urlopen(req2, timeout=5) as resp:
        txt2 = resp.read().decode('utf-8')
        print("SSE query2 snippet:", txt2[:300])
except Exception as e:
    print("SSE query2 error:", e)
