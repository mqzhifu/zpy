import pandas as pd
import util.pd as upd
import util.common as uc
import matplotlib.pyplot as plt
#data source https://www.kaggle.com/datasets/starbucks/store-locations

upd.init_pd(pd)
uc.process_font(plt)
saveImgPath = "../test_img/"

def main():
    read_data = pd.read_csv("../data/directory.csv")
    # uc.ppp(read_data.groupby(by=["Brand"]).count())
    plt.figure(figsize=(20,8),dpi=80)

    ax1 = plt.subplot(221)
    ax2 = plt.subplot(222)
    ax3 = plt.subplot(212)

    country = read_data.groupby(by=['Country'])["Country"].count().sort_values(ascending=False).head(10)
    p1 = ax1.bar  (country.index ,country.values,width=0.5)
    ax1.bar_label(p1,label_type="edge")

    ax1.set_xlabel("国家",fontsize='large')
    ax1.set_ylabel("开店数",fontsize='large')
    ax1.set_title("星巴克 - 世界国家开店总数")

    plt.grid()

    CountryProvince =read_data.groupby(by=['Country','State/Province'])["Country"].count().sort_values(ascending=False)
    # cn = read_data.groupby(by=['Country'])["Country"].count().sort_values(ascending=False).head(10)
    # uc.ppp(cn["CN"])
    p2 = ax2.bar  (CountryProvince["CN"].index ,CountryProvince["CN"].values,width=0.5,color="r")
    ax2.bar_label(p2,label_type="edge")

    ax2.set_xlabel("中国 - 省(id)",fontsize='large')
    ax2.set_ylabel("开店数",fontsize='large')
    ax2.set_title("星巴克 - 中国各省开店总数")

    plt.grid()


    p3 = ax3.bar  (CountryProvince["US"].index ,CountryProvince["US"].values,width=0.5,color="g")
    ax3.bar_label(p3,label_type="edge")

    ax3.set_xlabel("美国 - 省(id)",fontsize='large')
    ax3.set_ylabel("开店数",fontsize='large')
    ax3.set_title("星巴克 - 美国各省开店总数")

    plt.grid()


    path = saveImgPath + "demo1.png"
    print("save pah:",path)
    plt.savefig(path)

if  __name__ == "__main__" :
    main()