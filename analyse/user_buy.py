import pandas as pd
import util.pd as upd
import util.common as uc
import matplotlib.pyplot as plt
import numpy as np

upd.init_pd(pd)
uc.process_font(plt)

saveImgPath = "../test_img/"


def main():
    read_data = pd.read_csv("../data/user_buy.txt", sep="\s+", names=["uid","date","orders_num","price"])

    read_data["date"] = pd.to_datetime(read_data["date"],format="%Y%m%d")
    read_data["date_month"] = read_data["date"].astype("datetime64[M]")

    # cnt1(read_data)
    # cnt2(read_data)
    RFM(read_data)

    #
    # user_buy_cnt = read_data.groupby(by=["uid"])["num"].count()
    # user_buy_price = read_data.groupby(by=["uid"])["price"].sum()
    #
    # cc = pd.concat([user_buy_cnt,user_buy_price],axis=1)
    # ccNum = cc.sort_values(by="price",ascending=False)
    # ccNum["avge"] = ccNum["price"] / ccNum["num"]
    # uc.ppp(ccNum.head(100))


    # print(cc.head())


    # print(read_data.head(10000))

def RFM(read_data):
    agg = read_data.pivot_table(index="uid",values=["date","orders_num","price"],
                          aggfunc={
                              "date":"max","orders_num":"sum","price":"sum"
                          }
                          )
    # print(agg.head())
    agg["date_distance"] = ( agg["date"].max() - agg["date"].min() ) / np.timedelta64(1,"D")
    agg["date_distance"] =  agg["date_distance"].astype("int")
    agg["price"] =  agg["price"].astype("int")
    agg["orders_num"] =  agg["orders_num"].astype("int")
    print(agg.head())
    # uc.ppp( agg["orders_num"] )
    # uc.ppp(agg["orders_num"].values)
    # print(len(agg["price"].index)," ", len(agg["price"].values) )
    # aggFinal = pd.DataFrame(   { agg["orders_num"].values , agg["price"].values } , index=agg["orders_num"].index  )
    # print("aggFinal:",aggFinal.head())

    orders_num_mean = agg["orders_num"].mean()
    price_mean = agg["price"].mean()
    date_distance_mean = agg["date_distance"].mean()

    print("mean:" , orders_num_mean,price_mean,date_distance_mean)

    agg["price_flag"] = agg["price"]
    agg["price_flag"].where( agg["price"] > price_mean,0,inplace=True)
    agg["price_flag"].where( agg["price"] <= price_mean,1,inplace=True)

    agg["orders_num_flag"] = agg["orders_num"]
    agg["orders_num_flag"].where( agg["orders_num"] > price_mean,0,inplace=True)
    agg["orders_num_flag"].where( agg["orders_num"] <= price_mean,1,inplace=True)

    agg["date_distance_flag"] = agg["date_distance"]
    agg["date_distance_flag"].where( agg["date_distance"] > price_mean,0,inplace=True)
    agg["date_distance_flag"].where( agg["date_distance"] <= price_mean,1,inplace=True)

    # agg["RFM"] = agg["date_distance_flag"].str + "" + agg["orders_num_flag"].str + "" + agg["price_flag"].str
    agg["RFM"] = agg["date_distance_flag"].map(str)  + agg["orders_num_flag"].map(str) + agg["price_flag"].map(str)
    print(  agg.head(100) )
    # print(aggFinal.head())

if  __name__ == "__main__" :
    main()