import sys
sys.path.append(r'd:/AKFile/其他/投资/星耀数智')
import config
import AmazingData as ad

config.init_amazing_data()
info = ad.InfoData()
try:
    # Check if there is queryTableMaxNumAndTime or similar in info
    print("Methods in info:", [m for m in dir(info) if 'margin' in m.lower() or 'time' in m.lower() or 'table' in m.lower()])
except Exception as e:
    print("Error:", e)
