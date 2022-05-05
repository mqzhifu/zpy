import pandas as pd
import matplotlib.pyplot as plt


# df1 = pd.DataFrame(
# {
#     'var1':1,
#     'var2':[1,2,3,4],
#     'var4':'cons'
# }
# )
#
# print(df1)
#
# df1 = pd.DataFrame( data = [ [1,"test"] ,[2,"tt2"] ,[3,"tt2"] ,[4,"tt2"]  ],columns = ["z1","z2"]
# )
#
# print(df1)

filename = "/Users/wangdongyan/Downloads/hero.csv"
df = pd.read_csv(filename,encoding = "utf8")
print(df.head())
print(df.info())


# plt.scatter(df2)
# plt.show()

#/Users/wangdongyan/opt/anaconda3/pkgs/matplotlib-base-3.3.4-py38h8b3ea08_0/lib/python3.8/site-packages/matplotlib/mpl-data
#/Users/wangdongyan/opt/anaconda3/lib/python3.8/site-packages/matplotlib/mpl-data

gg = df.groupby("hero_type")["hero_type"].count().sort_values()
gg2 = df.groupby("hero_type")["power_recovery"].sum().sort_values()
print(gg)
# print(gg2)

columns = list(gg.index)
print("columns:",columns,list(gg))


print("min:",gg.min(),"max:",gg.max(),"mean:",gg.mean(),"median:",gg.median(),"sum:",gg.sum())


plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['font.size'] = 12  # 字体大小
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

## 饼图
e = list()
for i in range(len(gg)):
    e.append(0)
e[len(gg)-1] = 0.1

labels = columns
plt.pie(gg,labels=labels,autopct = "%.2f%%",explode= e)




## 折线
# plt.xticks(rotation=300) #X轴汉字变坚体展示
# plt.plot(columns,gg,label="count",marker='o')
# plt.plot(columns,gg2,label="sum",marker='*')
# plt.legend()
# plt.xlabel('分类')
# plt.ylabel('值')

# # 直方
# plt.hist(gg)
# plt.xlabel("数量")
# plt.ylabel("分类")

## 条形图
# y_pos = (1,2,3,4,5,6)
# plt.bar(y_pos, list(gg), align='center', alpha=0.7)
# plt.xticks(y_pos,columns)
# plt.ylabel('Usage')


plt.title("测试图")
plt.show()
