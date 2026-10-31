import sys
sys.path.append(r'd:/AKFile/其他/投资/星耀数智')
import config
import AmazingData as ad
import pandas as pd

config.init_amazing_data()
base = ad.BaseData()
try:
    adj_comm = base.get_backward_factor(['515880.SH', '588200.SH'])
    print("Adj factor type:", type(adj_comm))
    if isinstance(adj_comm, dict):
        for k, v in adj_comm.items():
            print(k, v.tail(5))
    elif isinstance(adj_comm, pd.DataFrame):
        print(adj_comm.tail(5))
except Exception as e:
    print(f"Error getting adj factor: {e}")
