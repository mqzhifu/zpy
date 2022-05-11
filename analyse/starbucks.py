import pandas as pd
import util.pd as upd
#data source https://www.kaggle.com/datasets/starbucks/store-locations

upd.init_pd(pd)

read_data = pd.read_csv("./data/directory.csv")
print(read_data.head())
# cc = read_data.groupby("Country")["Store Name"].count().sort_values(ascending=False)
# print(cc.head())
#
# cn = read_data[read_data["Country"] == "CN"]
# cnProvinceCnt = cn.groupby(by="State/Province")["Store Name"].count().sort_values(ascending=False)
# print(cnProvinceCnt.head())

cc =read_data.groupby(by=['Country','State/Province'])["Country"].count()
print(cc)
