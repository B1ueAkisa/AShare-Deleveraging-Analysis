import yfinance as yf
import pandas as pd

t_comm = yf.Ticker('515880.SS')
hist_comm = t_comm.history(start='2026-05-01', end='2026-11-01')
print("--- 515880.SS History Columns & Sample ---")
print("Columns:", hist_comm.columns)
print(hist_comm[['Open', 'High', 'Low', 'Close', 'Stock Splits', 'Dividends']].loc['2026-06-20':'2026-07-25'])

t_chip = yf.Ticker('588200.SS')
hist_chip = t_chip.history(start='2026-05-01', end='2026-11-01')
print("\n--- 588200.SS History Columns & Sample ---")
print(hist_chip[['Open', 'High', 'Low', 'Close', 'Stock Splits', 'Dividends']].loc['2026-06-20':'2026-07-25'])
