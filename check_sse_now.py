import urllib.request
import json
import datetime

def check():
    headers = {
        'Referer': 'http://www.sse.com.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    url = 'http://query.sse.com.cn/marketdata/tradedata/queryMargin.do'
    req = urllib.request.Request(url, headers=headers)
    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now_str}] Checking SSE Margin Data...")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            results = data.get('result', [])
            if results:
                latest = results[0]
                print(f"Latest Date: {latest.get('opDate')}")
                print(f"SSE Margin Balance: {latest.get('rzye')} ({round(float(latest.get('rzye',0))/1e8, 2)} 亿元)")
                print(f"SSE Margin Buy: {latest.get('rzmre')} ({round(float(latest.get('rzmre',0))/1e8, 2)} 亿元)")
                print(f"SSE Margin Repay: {latest.get('rzche')} ({round(float(latest.get('rzche',0))/1e8, 2)} 亿元)")
                if str(latest.get('opDate')) == '20261103':
                    print(">>> SUCCESS: 2026-11-03 SSE MARGIN DATA IS OUT! <<<")
                    return True
                else:
                    print(">>> 2026-11-03 data NOT published yet. Latest is still 2026-11-02. <<<")
                    return False
    except Exception as e:
        print("Error checking SSE:", e)
        return False

if __name__ == '__main__':
    check()
