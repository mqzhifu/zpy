import pandas as pd
import util.pd as upd

upd.init_pd(pd)

read_data = pd.read_csv("./data/book/books.csv")
read_data = read_data.drop(["isbn","isbn13","image_url","small_image_url"],axis=1)
print(read_data.head(10))
print(read_data.info())


notNullYear = read_data[pd.notnull(read_data["original_publication_year"])]
ageCnt = notNullYear.groupby(by='original_publication_year')["title"].count().sort_values(ascending=False)
# ageCnt = read_data.groupby(by='original_publication_year')["title"].count().sort_values(ascending=False)
print(ageCnt.head(10))

