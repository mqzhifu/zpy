# import spider.lagou
# import spider.lagou_selenium
import os
import spider.lagou_third

def main():
    pwd = os.getcwd()
    data_path = pwd + "/"
    # img_path = pwd + "/test_img"

    print("im in spider main ,  path:",pwd)

    # c = spider.lagou.Lagou(data_path)
    # c.start()

    # c = spider.lagou_selenium.LagouSelenium(data_path)
    # c.start()
    # lagou = spider.lagou_third.lagou()
    # lagou.run()

if  __name__ == "__main__" :
    main()
