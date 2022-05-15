import util.common as uc
import matplotlib.pyplot as plt
import pandas as pd

class User :
    data_path = ""
    img_path = ""
    data = None
    def __init__(self,data_path,img_path):
        self.data_path = data_path
        self.img_path = img_path

        uc.set_pd_base(pd)
        uc.set_plt_font(plt)

        read_data = pd.read_csv(self.data_path + "/user_buy.txt", sep="\s+", names=["uid","date","orders_num","price"])
        # print(read_data.head())
        read_data["date"] = pd.to_datetime(read_data["date"],format="%Y%m%d")
        read_data["date_month"] = read_data["date"].astype("datetime64[M]")

        # 查看 缺失值
        # all(pd.isnull)

        self.data = read_data

    def start(self):
        print(self.data_path,self.img_path)
        # self.total_list()
        self.first_last()

    def first_last(self):
        #用户第一次下单时间
        first_buy = self.data.groupby(by=["uid"])["date"].min()
        #用户最后一次下单时间
        last_buy = self.data.groupby(by=["uid"])["date"].max()

        #以 天 为维度，统计 每天 下单中，第一次下单的用户总数
        first_buy_everyday = first_buy.value_counts().sort_index()

        #以 天 为维度，统计 每天 下单中，最后一次下单的用户总数
        last_buy_everyday = last_buy.value_counts().sort_index()


        plt.figure(figsize=(20,8),dpi=80)
        ax1 = plt.subplot(221)
        ax2 = plt.subplot(222)

        ax1.plot(first_buy_everyday.index , first_buy_everyday,linestyle='--',label="用户首次下单")
        ax1.plot(last_buy_everyday.index , last_buy_everyday,linestyle='-',label="用户末次下单")

        ax1.legend(loc="best")
        ax1.grid()
        ax1.set_title("用户首/末次下单情况(天)")
        ax1.set_xlabel("天")
        ax1.set_ylabel("下单数")

        # 统计:只下单一次的用户， 注：一个用户可能一天下了2单，但按照这种方式，是统计 成一次的
        user_only_buy_one = self.data.groupby(by="uid")["uid"].count()
        user_only_buy_one_cnt = user_only_buy_one [ user_only_buy_one == 1 ].count()
        other_user = len (self.data.groupby(by="uid")["uid"]) - user_only_buy_one_cnt
        print("user_only_buy_one_cnt:",user_only_buy_one_cnt , " other: ",other_user)
        ax2.pie([user_only_buy_one_cnt,other_user],labels=["首次",'其它'])

        ax2.set_title("只消费一次占比")
        # user_by_one_data = self.data[ self.data["uid"].isin(  user_only_buy_one.index ) ]
        # ax1.plot(first_buy_everyday.index , first_buy_everyday,linestyle='--',label="用户首次下单")

        # # print(user_by_one_data)
        # user_by_one_data_by_month = user_by_one_data.groupby(by="date_month")["uid"].count()
        # user_by_one_data_by_day = user_by_one_data.groupby(by="date")["uid"].count()
        # uc.ppp(user_by_one_data_by_day)
        #
        path = self.img_path + "/demo2.png"
        print("save pah:",path)
        plt.savefig(path)

    #比较总概的一些数据统计
    def total_list(self):
        #统计每个月的 下单 用户总数
        total_users = self.data.groupby(by=["date_month"])["uid"].count()
        #统计每个月的 下单总数
        total_orders = self.data.groupby(by=["date_month"])["orders_num"].sum()
        #统计每个月的 下单 总金额
        total_price = self.data.groupby(by=["date_month"])["price"].sum()
        #将上面3列合并成一个二维表
        total_list = pd.concat([total_users,total_orders,total_price],axis=1)
        #增加新列 用户 平均 下单数
        total_list["user_order_avge"] = total_list["orders_num"] / total_list["uid"]
        total_list["price"] = total_list["price"] / 10
        #增加新列 用户平均每单多少钱
        total_list["order_price_avge"] = total_list["price"] / total_list["orders_num"]
        # uc.ppp(total_list)
        #开始 画图

        #创建一张画面
        plt.figure(figsize=(20,8),dpi=80)

        ax1 = plt.subplot(221)
        ax2 = plt.subplot(222)
        ax3 = plt.subplot(212)


        ax1.plot(total_list.index , total_list["user_order_avge"],label="用户平均订单数")
        ax1.grid()

        ax2.plot(total_list.index , total_list["order_price_avge"] * 10,label="用户平均订单金额")
        ax2.grid()


        ax3.plot(total_list.index , total_list["uid"]       ,linestyle='--',label="用户数")
        ax3.plot(total_list.index , total_list["orders_num"],label="订单数")
        #这里阶以10，不然数字太大，几条线不好看了
        ax3.plot(total_list.index , total_list["price"]      ,label="总金额")
        #
        # plt.plot(cc.index , cc["user_order_avge"],label="用户平均下单数")
        # # plt.plot(cc.index , cc["order_price_avge"],label="订单平均价格")
        #
        # 为每个点添加数值标签
        for a,b in zip(total_list.index,total_list['uid']):
            ax3.text(a,b+50,'%.0f'%b,ha = 'center',va = 'bottom',fontsize=12)

        for a,b in zip(total_list.index,total_list['orders_num']):
            ax3.text(a,b+50,'%.0f'%b,ha = 'center',va = 'bottom',fontsize=12)

        for a,b in zip(total_list.index,total_list['price']):
            ax3.text(a,b+50,'%.0f'%b,ha = 'center',va = 'bottom',fontsize=12)
        #
        # for a,b in zip(cc.index,cc['user_order_avge']):
        #     plt.text(a,b+50,'%.0f'%b,ha = 'center',va = 'bottom',fontsize=12)
        #
        # # for a,b in zip(cc.index,cc['order_price_avge']):
        # #     plt.text(a,b+50,'%.0f'%b,ha = 'center',va = 'bottom',fontsize=12)
        #
        #
        #
        #
        ax3.legend(loc="best")
        #
        ax3.set_title("月份 - 购买情况")
        ax3.set_xlabel("月份")
        ax3.set_ylabel("统计数值")

        ax3.grid()

        # # plt.show()

        path = self.img_path + "/demo1.png"
        print("save pah:",path)
        plt.savefig(path)