import util.common as uc
import matplotlib.pyplot as plt
import pandas as pd
import tushare as ts

class Stock :
    data_path = ""
    img_path = ""
    data = None
    data_file_name = "stock.cvs"
    def __init__(self,data_path,img_path):
        self.data_path = data_path
        self.img_path = img_path

        uc.set_pd_base(pd)
        uc.set_plt_font(plt)

        # self.init_data()

        read_data = pd.read_csv(self.data_path + "/" + self.data_file_name)
        # print(read_data.head())
        read_data["date"] = pd.to_datetime(read_data["date"])
        #重置索引，将date转化成索引
        read_data.set_index("date",inplace=True)
        # read_data["date_month"] = read_data["date"].astype("datetime64[M]")

        # print(read_data.head())
        # print(read_data.info())
        # 查看 缺失值
        # all(pd.isnull)

        self.data = read_data

    def start(self):
        print(self.data_path,self.img_path)
        self.total_list()
        # self.first_last()

    def init_data(self):
        #源数据是从 tushare 中获取，请先下载保存，下次使用，直接调用文件即可
        data = ts.get_k_data(code="600519",start="2000-01-01")
        print( "data len:",len( data["open"] ) )
        print(data.head())
        # date   open  close   high    low    volume    code
        pdData = pd.DataFrame(data)
        pdData = pdData.drop(["code"],axis=1)
        print(pdData["open"].head())
        savePath = self.data_path + "/" + self.data_file_name
        pdData.to_csv(savePath,index=0)

        uc.ppp("finish.")

    def total_list(self):
        print(3)
        r = self.data["2019":"2020"]
        print(r.head())
        l = r.resample("M").first()
        print(l)