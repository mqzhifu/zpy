import pandas as pd
import util.pd as upd

upd.init_pd(pd)

dir = "./1024/merge.cvs"

read_date = pd.read_csv(dir,sep="^",names=['page','url','actor','brand','title','category','tags',"labels","hits"])
print(read_date.info())
# print(read_date.head(1000))
# rr = read_date[ pd.isnull(read_date["tags"])]

# rr = read_date[read_date["tags"] == "【歐美精選】"]
rr = read_date[pd.isnull(read_date["actor"])]
# # rr = read_date[read_date["tags"] == "【欧美精选】"]
#
print(rr)
print(len(rr))