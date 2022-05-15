import util.common as uc
import matplotlib.pyplot as plt
import pandas as pd

class USArea :
    data_path = ""
    img_path = ""
    data = None
    # data_file_name = "stock.cvs"
    def __init__(self,data_path,img_path):
        self.data_path = data_path
        self.img_path = img_path

        uc.set_pd_base(pd)
        uc.set_plt_font(plt)
        #州-缩写
        read_data_abbrevs = pd.read_csv(self.data_path + "/state-abbrevs.csv")
        print(read_data_abbrevs.head())
        # uc.ppp(read_data_abbrevs.info())
        #州-大小面积
        read_data_areas = pd.read_csv(self.data_path + "/state-areas.csv")
        print(read_data_areas.head())
        #人口
        read_data_population = pd.read_csv(self.data_path + "/state-population.csv")
        print(read_data_population.head())

        abbrevs_population = pd.merge(read_data_population,read_data_abbrevs,left_on="state/region",right_on="abbreviation",how="outer")
        abbrevs_population.drop(["abbreviation"],inplace=True,axis=1)
        # print(abbrevs_population.head())
        print(abbrevs_population.info())
        # print(abbrevs_population.isnull())
        #处理 state 缺失值，先看下 哪些数据造成了缺失：['PR' 'USA']
        # ss = abbrevs_population [ abbrevs_population["state"].isnull() ]["state/region"].unique()

        stateNullIndex = abbrevs_population [ abbrevs_population["state/region"] == "PR" ]["state"].index
        abbrevs_population.loc[stateNullIndex,"state"] = "Puerto Rico"

        stateNullIndex = abbrevs_population [ abbrevs_population["state/region"] == "USA" ]["state"].index
        abbrevs_population.loc[stateNullIndex,"state"] = "United States "

        # 全并 缩写 与 面积表，貌似没啥用
        # abbrevs_areas = pd.merge(read_data_abbrevs,read_data_areas,on="state")
        # print(abbrevs_areas.head())

        abbrevs_population_areas = pd.merge(abbrevs_population,read_data_areas,on="state",how="outer")
        # print(abbrevs_population_areas.info())
        # print(abbrevs_population_areas.head())
        #发现列缺失值

        # areaNullIndex = abbrevs_population_areas["area (sq. mi)"].isnull().index
        areaNullIndex = abbrevs_population_areas.loc[abbrevs_population_areas["area (sq. mi)"].isnull()].index
        abbrevs_population_areas.drop(labels=areaNullIndex, axis=0,inplace=True)

        # print(abbrevs_population_areas["ages"])
        ss = abbrevs_population_areas.query(' ages == "total" & year == 2010 ')
        # print(ss)

        abbrevs_population_areas["midu"] = abbrevs_population_areas["population"] / abbrevs_population_areas["area (sq. mi)"]
        print(abbrevs_population_areas.head())
        # abbrevs_population_areas[  ]