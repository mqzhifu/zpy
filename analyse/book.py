import pandas as pd
import util.pd as upd
import util.common as uc
import matplotlib.pyplot as plt

upd.init_pd(pd)
uc.process_font(plt)

saveImgPath = "../test_img/"


def main():
    read_data = pd.read_csv("../data/book/books.csv")
    uc.ppp(read_data.head())

    plt.figure(figsize=(20,8),dpi=80)

    #将画面分成 3 X 3 格局
    ax1 = plt.subplot(321)#第一行，分成2列，取第1个格子
    ax2 = plt.subplot(322)#第一行，分成2列，取第2个格子
    ax3 = plt.subplot(312)#这里重新规划了画布，改成了3 x 1 ，那么上面两个格子就被定义成一个大格子，现在取第2个格子
    ax4 = plt.subplot(313)#取第3行，第3个格子

    read_data = read_data.drop([ "best_book_id","original_title", "isbn","isbn13","image_url","small_image_url"],axis=1)
    # uc.ppp(read_data.head(10))

    notNullYear = read_data[pd.notnull(read_data["original_publication_year"])]
    notNullYear = read_data[ read_data["original_publication_year"] > 0   ]
    ageCnt = notNullYear.groupby(by='original_publication_year')["title"].count().sort_values(ascending=False).head(20)

    p1 = ax1.bar  (ageCnt.index ,ageCnt.values,width=0.5,color="#ff7f0e")
    ax1.bar_label(p1,label_type="edge")

    ax1.set_xlabel("年份",fontsize='large')
    ax1.set_ylabel("书籍数",fontsize='large')
    ax1.set_title("书籍出版数")

    ax1.grid()


    authors = read_data[pd.notnull(read_data["authors"])].groupby(by="authors")["id"].count().sort_values(ascending=False).head(10)

    p1 = ax3.bar  (authors.index ,authors.values,width=0.5,color="#17becf")
    ax3.bar_label(p1,label_type="edge")

    ax3.set_xlabel("作者",fontsize='large')
    ax3.set_ylabel("书籍数",fontsize='large')
    ax3.set_title("作者书籍数")

    ax3.grid()

    language_code = read_data[pd.notnull(read_data["language_code"])].groupby(by="language_code")["id"].count().sort_values(ascending=False).head(5)
    p2 = ax2.barh  (language_code.index ,language_code.values,height=0.5,color="#8c564b")
    ax2.bar_label(p2,label_type="edge")

    ax2.grid()

    ax4.plot(ageCnt.values , ageCnt.index , color="y" )
    ax4.grid()

    path = saveImgPath + "demo1.png"
    print("save pah:",path)
    plt.savefig(path)


if  __name__ == "__main__" :
    main()