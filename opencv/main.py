import cv2
import matplotlib.pyplot as plt

def main():
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

def demo1():
    img_path = "../test_img/demo1.png"
    print("path:",img_path)

    img = cv2.imread(img_path,0)
    # cv2.imshow("image",img)
    # cv2.waitKey(0)
    plt.imshow(img)
    plt.show()

if  __name__ == "__main__" :
    main()