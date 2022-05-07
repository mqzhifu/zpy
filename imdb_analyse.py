import numpy as np
import pandas as pd
import util.pd as upd

upd.init_pd(pd)

#https://www.kaggle.com/code/damianpanek/sunday-eda/data
read_data = pd.read_csv("./data/imdb_top_1000.csv")
drop_col = ["Poster_Link","Overview"]
read_data = read_data.drop(drop_col,axis=1)

print(read_data.head())