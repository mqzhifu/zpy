# import analyse.user
# import analyse.stock
# import analyse.us_area

# import numpy as np
# import cv2
# import math
# import random

import  os

# import  autotest.parser_swagger

import autotest.apitest

def main():
    pwd = os.getcwd()
    # data_path = pwd + "/data"
    # img_path = pwd + "/test_img"
    #
    print("im in main ,  pwd:",pwd)


    # user = analyse.user.User(data_path,img_path)
    # user.start()

    # stock = analyse.stock.Stock(data_path,img_path)
    # stock.start()

    # autotest.parser_swagger

    apiTest = autotest.apitest.ApiTest("127.0.0.1","1111","http","D:/project/zpy/data/swagger.json")
    apiTest.run()


if  __name__ == "__main__" :
    main()

