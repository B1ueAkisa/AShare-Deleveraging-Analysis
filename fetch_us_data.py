import os
import sys
import pandas as pd
import yfinance as yf

# Rule: Set HTTP_PROXY and HTTPS_PROXY to http://127.0.0.1:7890 when calling Google APIs or internet-facing tools.
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

print("Testing yfinance for Nasdaq (^IXIC) and S&P500 (^GSPC)...")
try:
    # 2000 Dot-Com crash
    nasdaq_2000 = yf.download('^IXIC', start='2000-01-01', end='2003-01-01', progress=False)
    print("Nasdaq 2000 shape:", nasdaq_2000.shape)
    nasdaq_2000.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/nasdaq_2000.csv')
    
    # 2020 Covid crash
    sp500_2020 = yf.download('^GSPC', start='2020-01-01', end='2020-06-01', progress=False)
    print("S&P500 2020 shape:", sp500_2020.shape)
    sp500_2020.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/sp500_2020.csv')

    # 2018 US crash
    nasdaq_2018 = yf.download('^IXIC', start='2018-09-01', end='2019-02-01', progress=False)
    print("Nasdaq 2018 shape:", nasdaq_2018.shape)
    nasdaq_2018.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/nasdaq_2018.csv')
    print("Successfully fetched US historical data!")
except Exception as e:
    print(f"Error fetching US data via yfinance: {e}")
