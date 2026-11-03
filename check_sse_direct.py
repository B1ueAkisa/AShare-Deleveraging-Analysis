import urllib.request
import json

headers = {
    'Referer': 'http://www.sse.com.cn/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

url = 'http://query.sse.com.cn/marketdata/tradedata/queryMargin.do'
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        results = data.get('result', [])
        print(f"Total records returned: {len(results)}")
        for r in results[:5]:
            print(r)
except Exception as e:
    print("Error:", e)
