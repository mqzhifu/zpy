#测试 matplotlib

import random

import matplotlib.pyplot as plt
import numpy as np
import util.common as uc

uc.process_font(plt)

saveImgPath = "./test_img/"
#demo 1 生成一个最简单的线图
# plt.figure(figsize=(20,8),dpi=100)
#
# x = [1,22,15,48,47]
# y = [10,20,30,40,52]
#
#
# plt.plot(x,y)
#

# plt.savefig(saveImgPath + "demo1.png")

#demo 2 生成折线图
x = range(60)#生成一个列表（迭代器）,包含60个元素
y_shanghai = [random.uniform(10,15) for i in x]
y_beijing =  [random.uniform(1,3) for i in x]

plt.figure(figsize=(20,8),dpi=100)

plt.plot(x,y_shanghai,label="上海")
#color , r:red g:green y:yellow...  linestyle,-:实线 --:虚线
plt.plot(x,y_beijing,label="北京",color="r",linestyle="--")
#显示上面图例：上海  北京，在 best(最好) 的位置
plt.legend(loc="best")

#默认情况：XY的刻度由给定XY值自动生成，如：值为Y轴的值是10~15，刻度就是10~15的范围
#现在自定义刻度
y_tickts = range(40)
plt.yticks(y_tickts[::5])

x_tickts_lables = ["11点{}分".format(i) for i in x]
plt.xticks(x[::5],x_tickts_lables[::5])

plt.xlabel("时间")
plt.ylabel('温度')
plt.title("demo2-一小时温度",fontsize=20)
#添加网格
plt.grid(True,linestyle="--",alpha=0.7)

plt.savefig(saveImgPath + "demo2.png")
# plt.show()

#一次画多张图
#plt.subplot


#demo3 画一个sin函数
x = np.linspace(-10,10,1000)
y = np.sin(x)

plt.figure(figsize=(20,8),dpi=100)
plt.plot(x,y)
plt.savefig(saveImgPath + "demo3.png")

#demo4 画一个直方图
x = np.random.uniform(-1,1,10000)
plt.figure(figsize=(20,8),dpi=100)

plt.hist(x=x,bins=100)

plt.savefig(saveImgPath + "demo4.png")

#demo5 画一个 正太分布图
x = np.random.normal(1.7,1,100)
plt.figure(figsize=(20,8),dpi=100)
plt.hist(x,bins=100)

plt.savefig(saveImgPath + "demo5.png")