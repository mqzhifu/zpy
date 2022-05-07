#测试 pandas

import pandas as pd
import numpy as np

#demo1 随机数
# data = np.random.normal(0,1,(8,5))
# print("np.random.normal data:",data)
#
# line_total = data.shape[0]
# column_total = data.shape[1]
#
# print(line_total,column_total)
#
# every_line_label = ["股票{}".format(i+1) for i in range(line_total)]
# every_column_label = pd.date_range("20220401",periods=column_total,freq='B')
#
# # print(every_column_label)
#
# pdDataFrame = pd.DataFrame(data,index=every_line_label,columns=every_column_label)
# print(pdDataFrame)
#
# # print(pdDataFrame.shape,pdDataFrame.index,pdDataFrame.columns,pdDataFrame.values)
#
# # 行转列 列转行
# print(pdDataFrame.T)
#

#demo2 读文件

#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100)
#列名如果使用中文，print输出的时候，会不对齐
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

field_map = {
    "hero_name":"名称","hero_type":"类型","hero_price":"价格","hero_pos":"位置",
    "hero_attr_live":"生存星数","hero_attr_attack":"攻击星数","hero_attr_ability":"能力星数","hero_attr_difficulty":"难度星数",
    "max_life":"最大血量","max_power":"最大力量","physical_attack":"物理攻击力","magic_attack":"魔法攻击",
    "physical_defense":"物理防御","physical_reduction":"物理减伤","magic_defense":"魔法防御","magic_reduction":"魔法减伤",
    "move_speed":"移速","physical_penetration":"物理穿透","magic_penetration":"魔法穿透",
    "attack_speed":"攻速","critical_hit":"暴击率","critical_effect":"critical_effect","physical_suck":"物理吸血","magic_suck":"法术吸血",
    "cooling_reduction":"冷却缩减","attack_range":"攻击范围","toughness":"韧性","life_recovery":"生命恢复","power_recovery":"力量恢复",
              }

# print(field_map)

field_drop = ["hero_attr_live","hero_attr_attack","hero_attr_ability","hero_attr_difficulty",
              "max_life","max_power","physical_attack",
              "magic_attack","physical_defense","physical_reduction","magic_defense","magic_reduction",
              "attack_speed","physical_penetration","critical_hit","magic_penetration","magic_penetration",
              "critical_effect","physical_suck","magic_suck",
              "cooling_reduction","toughness","life_recovery","power_recovery"
              ]

final_field = []
for i in field_map:
    hasSearch = 0
    for j in field_drop:
        if (i == j):
            hasSearch = 1
            break

    if (hasSearch == 0):
        final_field.append(field_map[i])


# every_column_label = list(field_map.values())
# print(every_column_label)
filename = "./data/wangzhe_hefo.csv"
pdDataOriginal = pd.read_csv(filename,encoding = "utf8")
pdData = pdDataOriginal.drop(field_drop,axis=1)
pdData.columns = final_field

print(pdData.head())
# print(df.info())

line_total = pdData.shape[0]
column_total = pdData.shape[1]

print("line_total:",line_total,"column_total:",column_total)

priceColumns = pdData['价格']

c = 0
priceBuyCategoryList = []
for i in priceColumns:
    # print("loop:",pdData['名称'][c], " " ,i)
    priceStr = i.strip(' ')
    priceList = priceStr.split('/')
    #
    priceBuyCategory = {"name": pdData['名称'][c],"gold":0,"rmb":0,"diamond":0,"special":"","type":""}
    if (len(priceList) == 1):
        priceBuyCategory["special"] = priceList[0]
        priceBuyCategory["type"] = "活动"
        # print(priceBuyCategory)
        c = c + 1
        priceBuyCategoryList.append(priceBuyCategory)
        continue

    for p in priceList:
        find_index = p.find("金币")
        if (find_index != -1):
            priceBuyCategory["gold"] = p[0:find_index]
            priceBuyCategory["type"] = "金币"

        find_index = p.find("钻石")
        if (find_index != -1):
            priceBuyCategory["diamond"] = p[0:find_index]
            if (priceBuyCategory["type"]):
                priceBuyCategory["type"] = priceBuyCategory["type"] + "/钻石"
            else:
                priceBuyCategory["type"] = "钻石"

        find_index = p.find("点券")
        if (find_index != -1):
            priceBuyCategory["rmb"] = p[0:find_index]
            if (priceBuyCategory["type"]):
                priceBuyCategory["type"] = priceBuyCategory["type"] + "/点卷"
            else:
                priceBuyCategory["type"] = "点卷"


    priceBuyCategoryList.append(priceBuyCategory)

    # print(priceBuyCategory,i)

    c = c + 1

pdDataNew = pdData.drop("价格",axis=1)

goldList = []
rmdList = []
diamondList = []
specialList = []
for i in priceBuyCategoryList:
    goldList.append(i["gold"])
    rmdList.append(i["rmb"])
    diamondList.append(i["diamond"])
    specialList.append(i["special"])




pdDataNew.loc[:,"金币"] = goldList
pdDataNew.loc[:,"点卷"] = rmdList
pdDataNew.loc[:,"钻石"] = diamondList
pdDataNew.loc[:,"特殊"] = specialList

pdDataNew["金币"] = pdDataNew["金币"].astype(int)
pdDataNew["点卷"] = pdDataNew["点卷"].astype(int)
pdDataNew["钻石"] = pdDataNew["钻石"].astype(int)

# print(pdDataNew.head())
# print(pdDataNew.info())
pp = pdDataNew.sort_values(by=["金币","点卷","钻石"],ascending=False)
print(pp.describe())

# print(priceBuyCategoryList)