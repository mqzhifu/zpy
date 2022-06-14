import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():
    # path_file_name = "/Users/wangdongyan/Downloads/film/大庆哥爆操短发少妇医院护士贾娜性感调教.mp4"
    # film_total.file_total(path_file_name)
    # demo3()
    # juanji()
    mask()

def mask():
    print("im in mask:")
    file = "../test_img/demo_a3.jpg"
    img = cv2.imread(file)


    hsv = cv2.cvtColor(img,code=cv2.COLOR_BGR2HSV)
    low_blue = np.array([110,50,50])
    up_blue  = np.array([130,255,255])
    mask = cv2.inRange(hsv,low_blue,up_blue)
    cv2.imshow("mask",mask)

    # cv2.imshow("demo_a2",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def demo3():
    img = cv2.imread("./thispersondoesnotexist.jpg")
    face_detector =  cv2.CascadeClassifier("./haarcascade_frontalface_alt.xml")
    face = face_detector.detectMultiScale(img)
    # 识别的时候，有些可能识别不到，或者错误了，加一些参数限定
    # face = face_detector.detectMultiScale(img,scaleFactor=1,minNeighbors=3,minSize=(60,60))
    print(face)

    for x,y,w,h in face:
        print(x,y,w,h)
        cv2.rectangle(img,pt1=(x,y),pt2=(x+w,y+h),color=[0,0,255],thickness=2)

    cv2.imshow("face",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(33)

def juanji():
    img_path = "../test_img/demo_a.jpg"


    img = cv2.imread(img_path)

    print("w:",img.shape[0], " h:",img.shape[1])

    # # kernel = np.ones((5,5),np.float32)  / 25
    # kernel = np.array([ [-1,-1,-1],[-1,8,-1] ,[-1,-1,-1]])
    #
    # dst = cv2.filter2D(img,-1,kernel)

    dst = cv2.boxFilter(img,-1,(5,5),normalize=True)
    cv2.imshow("my_ddd",np.hstack( (img,dst)))

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def demo1():
    img_path = "../test_img/demo1.png"
    print("path:",img_path)

    img = cv2.imread(img_path)
    # 看一下图片的量值，发现是3维的：X Y COLOR(蓝 绿 红)
    #print(img)
    # 正常显示图片
    # cv2.imshow("demo1",img)
    # 改变图片色系(翻转)
    # cv2.imshow("demo1",  img[ : , : , ::200] )
    # 翻转图片
    # cv2.imshow("demo1",  img[ ::-1 , : , :] )
    # 重置图片大小
    img2 = cv2.resize(img,(500,500))
    # 重置图片颜色 - 灰色
    gray = cv2.cvtColor(img2,code=cv2.COLOR_BGR2GRAY)
    cv2.imshow("img2",gray)

    cv2.waitKey(0)
    # plt.imshow(img)
    # plt.show()

    cv2.destroyAllWindows()

def demo2():
    cv2.namedWindow('video',cv2.WINDOW_NORMAL)
    cv2.resizeWindow("video",640,480)

    cap = cv2.VideoCapture(0)

    while True:
        ret,frame = cap.read()
        if not ret:
            break

        cv2.imshow('video',frame)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if  __name__ == "__main__" :
    main()