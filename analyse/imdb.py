import pandas as pd
import util.pd as upd
import util.common as uc
import matplotlib.pyplot as plt

upd.init_pd(pd)
uc.process_font(plt)

saveImgPath = "../test_img/"

def main():
    #source https://www.kaggle.com/code/damianpanek/sunday-eda/data
    read_data = pd.read_csv("../data/imdb_top_1000.csv")
    drop_col = ["Certificate","Poster_Link","Overview"]
    read_data = read_data.drop(drop_col,axis=1)

    # uc.ppp(read_data.head())
    rankTop10Mean(read_data)
# print("--")

#demo1 评分最高的前10部电影的平均值
def rankTop10Mean(data):
    # print(data.head(100))
    # print("*"*100)
    # uc.ppp(data.info())

    data = data.drop(["Released_Year" ,"Genre", "Star1","Star2","Star3","Star4"],axis=1)
    #添加一列，将原Gross字段值中的逗号去掉
    data["Gross_num"] = data["Gross"].str.replace(",","").astype("float")
    #处理掉缺失值
    data[  pd.isnull(data["Gross"]) ] = 0
    data[  pd.isnull(data["Gross_num"]) ] = 0

    # top_k(data)
    # zhifang(data)

    xx = pd.date_range(start="2022-01-01",end="2022-02-01")
    uc.ppp(xx)
    # data["Gross"].index = data["Series_Title"]
    # data["No_of_Votes"].index = data["Series_Title"]
    # print( data["No_of_Votes"] )
    # print(data)
    # aa = pd.DataFrame( ( data["Gross"].values , data["No_of_Votes"].values )  ,columns=  data["Series_Title"].values,index=["Gross","No_of_Votes"] )
    # aa = pd.DataFrame( (data[gr]) )
    # print(aa.pivot() )
    # sortRateMean = sortRate["IMDB_Rating"]
    # print("sortRateMean:" ,sortRate)
    # data.plot(x=data["Series_Title"])
    # data["No_of_Votes"].plot(kind="hist")
    # uc.ppp(saveImgPath)

    # plt.figure(figsize=(20,8),dpi=80)
    # plt.hist((data["No_of_Votes"]),bins=10)
    # plt.grid()
    #
    # plt.savefig(saveImgPath + "demo1.png")

def filterRunetime(x):
    if x == 0 :
        return x
    time = x.split(" ")[0]
    return time
#直方图
def zhifang(data):
    # print(data["Runtime"].head(100))


    data["Runtime_num"] =data["Runtime"].apply(filterRunetime).astype("float")

    runtime_data = data[data["Runtime_num"] > 0 ]

    max =int( runtime_data["Runtime_num"].max() )
    min = int( runtime_data["Runtime_num"].min() )

    groupDistance = int((max - min ) // 10)

    print("max:",max , " min:",min , " ",groupDistance)

    plt.figure(figsize=(20,8),dpi=80)

    plt.hist(runtime_data["Runtime_num"], groupDistance)
    plt.xticks(range(min,max,groupDistance))
    plt.grid()

    plt.savefig(saveImgPath + "demo1.png")

def top_k(data):
    plt.figure(figsize=(20,8),dpi=80)

    ax1 = plt.subplot(121)
    ax2 = plt.subplot(122)

    data_rank = data.sort_values(by=["IMDB_Rating","Meta_score"],ascending=False).head(10)
    # print(data_rank)

    p = ax1.barh( data_rank["Series_Title"],data_rank["IMDB_Rating"],height=0.2)
    ax1.bar_label(p,label_type="edge")

    data_gross = data.sort_values(by=["Gross_num","IMDB_Rating"],ascending=False).head(10)
    p2 = ax2.barh( data_gross["Series_Title"],data_rank["Gross_num"],height=0.2)
    ax2.bar_label(p2,label_type="edge")

    # plt.xlabel ("分数" )
    # plt.ylabel ("电影名" )
    # plt.title("电影-评分-前10")

    ax1.grid()
    ax2.grid()

    path = saveImgPath + "demo1.png"
    print("save pah:",path)
    plt.savefig(path)

#demo2 每年 的电影数 及 平均分
# orderAgeCount = read_data.groupby("Released_Year").agg(cnt=('Series_Title','count'))
# orderAgeMean = read_data.groupby("Released_Year").agg(mean=('IMDB_Rating','mean'))
#
# orderAge = pd.concat([orderAgeCount,orderAgeMean],axis=1).sort_values(by="cnt",ascending=False)
# print(orderAge.head(10))
#
# orderAge.plot()
#
# plt.show()

# #demo3 取出 电影的分类 字符串，然后切割成一个数组
# genreListPre = read_data["Genre"].str.split(",").tolist()
# genreList = []
# for i in genreListPre:
#     row = []
#     for j in i:
#         e = j.strip(" ")
#         # print(e)
#         row.append(e)
#
#     genreList.append(row)
#
# # print(genreList)
# # exit(1)
#
# categoryList = set (i.strip(" ") for j in genreList for i in j)
# # print("categoryList:",categoryList,len(categoryList))




# categoryListCnt = {}
# for i in genreList:
#     for j in i:
#         word = j.strip(" ")
#         if ( word in categoryListCnt.keys() ):
#             categoryListCnt[word] = categoryListCnt[word] + 1
#         else:
#             categoryListCnt[word] = 1
# print(len(categoryListCnt))
#
# pdCategoryListCnt = pd.Series(categoryListCnt)
# pdCategoryListCntSort = pdCategoryListCnt.sort_values(ascending=False)
# print(pdCategoryListCntSort.head())

# zero_df = pd.DataFrame(np.zeros((read_data.shape[0],len(categoryList))),columns=categoryList)
#
# for i in range(read_data.shape[0]):
#     zero_df.loc[i,genreList[i]] = 1
#
# g_cnt = zero_df.sum(axis=0).sort_values(ascending=False)
# print(g_cnt.head())


if  __name__ == "__main__" :
    main()