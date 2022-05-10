import pandas as pd
import util.pd as upd

upd.init_pd(pd)

dir = "./1024/merge.cvs"

read_date = pd.read_csv(dir,sep="^",names=['page','url','actor','brand','title','category','tags',"labels"])
# print(read_date.head(100))
# rr = read_date[ pd.isnull(read_date["tags"])]
rr = read_date[read_date["tags"] == "【歐美精選】"]
# rr = read_date[read_date["tags"] == "【欧美精选】"]

print(rr)