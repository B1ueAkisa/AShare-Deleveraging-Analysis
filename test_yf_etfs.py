import yfinance as yf
import pandas as pd
import numpy as np

print("Testing yfinance for 515880.SS (通信ETF) and 588200.SS (科创芯片ETF)...")

try:
    df_comm_yf = yf.download('515880.SS', start='2026-05-01', end='2026-11-01', progress=False)
    print("515880.SS yfinance shape:", df_comm_yf.shape)
    if not df_comm_yf.empty:
        print(df_comm_yf.tail(5))
except Exception as e:
    print(f"Error fetching 515880.SS via yfinance: {e}")

try:
    df_chip_yf = yf.download('588200.SS', start='2026-05-01', end='2026-11-01', progress=False)
    print("588200.SS yfinance shape:", df_chip_yf.shape)
    if not df_chip_yf.empty:
        print(df_chip_yf.tail(5))
except Exception as e:
    print(f"Error fetching 588200.SS via yfinance: {e}")
