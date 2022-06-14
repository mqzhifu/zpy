import numpy as np
from sklearn.datasets import  load_iris
import pandas as pd
import util.common as uc
import math


def main():
    iris = load_iris()
    prefix = "鸢尾花-"
    # print(prefix + "描述：",iris["DESCR"])
    # print(prefix + "数据集：",iris.data)
    print(prefix + "数据集-形状：",iris.data.shape)
    print(prefix + "特征集-名称：",iris.feature_names)
    print(prefix + "目标值-名称：",iris.target_names)


def aaa():
    uc.set_pd_base(pd)
    th = ["电影名称" , "搞笑镜头" , "拥抱镜头","打斗镜头","电影类型"]
    # 电影名称 , 搞笑镜头 , 拥抱镜头,打斗镜头,电影类型
    data = pd.read_csv("./film.txt",names=th,header=None)

    missingRow = ["唐人街探案",23,3,17,"",0]
    # missingRow = {"电影名称":"唐人街探案","搞笑镜头":23,"拥抱镜头":3,"拥抱镜头":17,"电影类型":"","距离":""}

    distanceList = []
    for index, row in data.iterrows():
        distancePow  = my_pow(missingRow[1] - row["搞笑镜头"]) + my_pow(missingRow[2] - row["拥抱镜头"]) + my_pow(missingRow[3] - row["打斗镜头"])
        distance = round ( math.sqrt(distancePow) ,2)
        distanceList.append(distance)

    # distanceList.append(0)
    data["距离"] = distanceList

    sort_data = data.sort_values(by="距离").reset_index()
    print(sort_data)

    k = 5
    for s in range(k):
        line = sort_data.loc[s]
        print(line["距离"], line['电影类型'])


    # # 把搜索这行，再添加到列表中
    # insertNewLineNum = len( data["搞笑镜头"] )
    # sort_data.loc[insertNewLineNum] = missingRow

    # print(data)

def my_pow(s ):
    return  math.pow(s,2)

if  __name__ == "__main__" :
    main()
