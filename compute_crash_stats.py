import pandas as pd
import numpy as np

print("--- Calculating Historical Crash Statistics ---")

# Helper to load yfinance csv
def load_yf_csv(path):
    df = pd.read_csv(path, skiprows=2)
    df = df.iloc[:, :6]
    df.columns = ['date', 'close', 'high', 'low', 'open', 'volume']
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    df = df.dropna(subset=['date', 'close']).sort_values('date').reset_index(drop=True)
    return df

# 1. 2026 Current Shuangchuang (Double Innovation) Crash
df_market = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/merged_market_data.csv')
df_market['kline_time'] = pd.to_datetime(df_market['kline_time'])

def get_crash_stats(df, col_name, start_date=None, end_date=None, label=""):
    sub = df.copy()
    if start_date:
        sub = sub[sub['date'] >= pd.to_datetime(start_date)]
    if end_date:
        sub = sub[sub['date'] <= pd.to_datetime(end_date)]
    sub = sub.sort_values('date').reset_index(drop=True)
    
    peak_val = sub[col_name].iloc[0]
    peak_date = sub['date'].iloc[0]
    trough_val = sub[col_name].min()
    trough_idx = sub[col_name].idxmin()
    trough_date = sub['date'].iloc[trough_idx]
    
    # only up to trough
    sub_crash = sub.iloc[:trough_idx+1].copy()
    days = len(sub_crash)
    total_drop = (trough_val - peak_val) / peak_val * 100
    daily_velocity = total_drop / max(1, (days - 1))
    
    # max 5-day and 10-day drop
    sub_crash['pct_5d'] = (sub_crash[col_name] / sub_crash[col_name].shift(5) - 1) * 100
    sub_crash['pct_10d'] = (sub_crash[col_name] / sub_crash[col_name].shift(10) - 1) * 100
    max_5d = sub_crash['pct_5d'].min()
    max_10d = sub_crash['pct_10d'].min()
    
    return {
        'label': label,
        'peak_date': peak_date.strftime('%Y-%m-%d'),
        'trough_date': trough_date.strftime('%Y-%m-%d'),
        'peak_val': round(peak_val, 3),
        'trough_val': round(trough_val, 3),
        'total_drop_pct': round(total_drop, 2),
        'trading_days': days,
        'daily_velocity_pct': round(daily_velocity, 2),
        'max_5d_drop_pct': round(max_5d if not np.isnan(max_5d) else 0, 2),
        'max_10d_drop_pct': round(max_10d if not np.isnan(max_10d) else 0, 2)
    }

results = []

# Current 2026 Shuangchuang
df_market['date'] = df_market['kline_time']
results.append(get_crash_stats(df_market, 'chinext_close', '2026-06-25', '2026-10-30', '2026双创: 创业板指全波段'))
results.append(get_crash_stats(df_market, 'chinext_close', '2026-10-19', '2026-10-30', '2026双创: 创业板指10月急跌浪'))

results.append(get_crash_stats(df_market, 'star50_close', '2026-06-30', '2026-10-30', '2026双创: 科创50全波段'))
results.append(get_crash_stats(df_market, 'star50_close', '2026-10-23', '2026-10-30', '2026双创: 科创50近期急跌浪'))

results.append(get_crash_stats(df_market, 'comm_etf_close', '2026-08-18', '2026-10-30', '2026科技: 通信ETF主跌浪'))
results.append(get_crash_stats(df_market, 'chip_etf_close', '2026-08-18', '2026-10-30', '2026科技: 科创芯片ETF主跌浪'))

# 2. 2015 A-share Crash
df_2015_cy = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/hist_2015_399006.SZ.csv')
df_2015_cy['date'] = pd.to_datetime(df_2015_cy['kline_time'])
results.append(get_crash_stats(df_2015_cy, 'close', '2015-06-05', '2015-07-08', '2015股灾: 创业板指第一波踩踏'))
results.append(get_crash_stats(df_2015_cy, 'close', '2015-06-05', '2015-09-02', '2015股灾: 创业板指双头出清'))

df_2015_sh = pd.read_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/hist_2015_000001.SH.csv')
df_2015_sh['date'] = pd.to_datetime(df_2015_sh['kline_time'])
results.append(get_crash_stats(df_2015_sh, 'close', '2015-06-12', '2015-07-09', '2015股灾: 上证指数第一波暴跌'))
results.append(get_crash_stats(df_2015_sh, 'close', '2015-08-18', '2015-08-26', '2015股灾: 上证指数第二波暴跌'))

# 3. 2008 A-share Crash
df_2008 = load_yf_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/hist_2008_000001.csv')
results.append(get_crash_stats(df_2008, 'close', '2007-10-16', '2008-10-28', '2008股灾: 上证综指全周期(6124->1664)'))
results.append(get_crash_stats(df_2008, 'close', '2008-01-14', '2008-04-22', '2008股灾: 上证最快主跌浪'))

# 4. 2000 Dot-Com Crash
df_dotcom = load_yf_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/hist_nasdaq_2000.csv')
results.append(get_crash_stats(df_dotcom, 'close', '2000-03-10', '2000-04-14', '2000科网泡沫: 纳斯达克第一波断崖下杀'))
results.append(get_crash_stats(df_dotcom, 'close', '2000-03-10', '2002-10-09', '2000科网泡沫: 纳斯达克全周期破裂'))

# 5. 2020 COVID Crash
df_covid_sp = load_yf_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/hist_sp500_2020.csv')
results.append(get_crash_stats(df_covid_sp, 'close', '2020-02-19', '2020-03-23', '2020美股流动性危机: 标普500暴跌'))

df_covid_nas = load_yf_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/hist_nasdaq_2020.csv')
results.append(get_crash_stats(df_covid_nas, 'close', '2020-02-19', '2020-03-23', '2020美股流动性危机: 纳斯达克暴跌'))

# 6. 2018 US Crash
df_2018_nas = load_yf_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/hist_nasdaq_2018.csv')
results.append(get_crash_stats(df_2018_nas, 'close', '2018-08-29', '2018-12-24', '2018美股流动性紧缩: 纳斯达克下杀'))

res_df = pd.DataFrame(results)
res_df.to_csv(r'd:/AKFile/其他/投资/去杠杆与暴跌速度对比分析/historical_crash_comparison.csv', index=False)
print("=== Historical Crash Comparison Table ===")
print(res_df.to_string())
