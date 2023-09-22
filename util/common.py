def ppp(  *args ):
    print(*args)
    exit(1)


def set_plt_font(plt):
    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.rcParams['font.size'] = 12  # 字体大小
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # import matplotlib
    # 查看字体存放位置，下载SimHei.tff，并放到此位置下
    # 查看字体缓存位置，删除
    # print(matplotlib.matplotlib_fname(),matplotlib.get_cachedir())
    # exit(11)


def set_pd_base(pd):
    pd.set_option('display.width', 1000)
    #显示所有列
    pd.set_option('display.max_columns', None)
    #显示所有行
    pd.set_option('display.max_rows', None)
    #设置value的显示长度为100，默认为50
    pd.set_option('max_colwidth',100)
    #列名如果使用中文，print输出的时候，会不对齐
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)


    pd.set_option('display.float_format',lambda x : '%.2f' % x)

#判断一个字典是否包含某个keys，如果存在返回该值，否则返回空
def key_exist_return_value(dist,key):
    if (key in dist.keys()):
        return dist[key]

    return ""

# 一维 map 转 string ，用于方便输出
def map_to_str(continer):
    str = "["
    for k,v in continer.items():
        str += k + ":" + v + ","

    return str + "]"