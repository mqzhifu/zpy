import pandas as pd
import matplotlib.pyplot as plt

filename = "/Users/wangdongyan/Downloads/area_weather.csv"
df = pd.read_csv(filename,encoding = "utf8")

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['font.size'] = 12  # 字体大小
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


gbProvince = df.groupby(["province","weather"])["weather"].count()



print (gbProvince)
print("min:",gbProvince.min(),"max:",gbProvince.max(),"mean:",gbProvince.mean(),"median:",gbProvince.median(),"sum:",gbProvince.sum())


for iterating_var in gbProvince.index:
    print(iterating_var)

# plt.title("测试图")
# plt.show()