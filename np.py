#测试numpy

import numpy as np

my_list = np.random.normal(0,1,(8,4))
print(my_list)

max = my_list.max()#整个矩阵的最大值
min = my_list.min()#整个矩阵的最小值

axis_max = my_list.max(axis=1)#整个矩阵的每一行最大值
axis_min = my_list.min(axis=1)#整个矩阵的每一行最小值


print("max:",max, " min:",min)
print("axis_max:",axis_max, " axis_min:",axis_min)


# bool_my_list = my_list >2
# print("bool_my_list:",bool_my_list)

# my_list[my_list >2] = 1
# print("my_re_list:",my_list)

# npwhere = np.where(my_list > 2,999,-999)
# print("npwhere:",npwhere)

# npWhereAnd = np.where(np.logical_and(my_list >-1 ,my_list < 1),999,-999)

