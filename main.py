import analyse.user
import analyse.stock
import analyse.us_area

import numpy as np
import cv2
import math
import random

import os



def main():
    pwd = os.getcwd()
    data_path = pwd + "/data"
    img_path = pwd + "/test_img"

    print("im in main ,  path:",pwd)


    # user = analyse.user.User(data_path,img_path)
    # user.start()

    # stock = analyse.stock.Stock(data_path,img_path)
    # stock.start()



if  __name__ == "__main__" :
    main()

