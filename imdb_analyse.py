import numpy as np
import pandas as pd
import util.pd as upd
import matplotlib.pyplot as plt
upd.init_pd(pd)

#https://www.kaggle.com/code/damianpanek/sunday-eda/data
read_data = pd.read_csv("./data/imdb_top_1000.csv")
drop_col = ["Certificate","Poster_Link","Overview"]
read_data = read_data.drop(drop_col,axis=1)

print(read_data.head())

print("--")
#demo1 评分最高的前10部电影的平均伊
# sortRate = read_data.sort_values(by=["IMDB_Rating","Meta_score"],ascending=False).head(10)
# # print(sortRate)
# sortRateMean = sortRate["IMDB_Rating"].mean(0)
# print("sortRateMean:" ,sortRateMean)

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

#demo3 取出 电影的分类 字符串，然后切割成一个数组
genreListPre = read_data["Genre"].str.split(",").tolist()
genreList = []
for i in genreListPre:
    row = []
    for j in i:
        e = j.strip(" ")
        # print(e)
        row.append(e)

    genreList.append(row)

# print(genreList)
# exit(1)

categoryList = set (i.strip(" ") for j in genreList for i in j)
# print("categoryList:",categoryList,len(categoryList))




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

zero_df = pd.DataFrame(np.zeros((read_data.shape[0],len(categoryList))),columns=categoryList)

for i in range(read_data.shape[0]):
    zero_df.loc[i,genreList[i]] = 1

g_cnt = zero_df.sum(axis=0).sort_values(ascending=False)
print(g_cnt.head())
