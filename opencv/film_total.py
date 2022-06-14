import cv2 as cv
def file_total(path_file_name):
    video = cv.VideoCapture(path_file_name)
    fpt = video.get(propId=cv.CAP_PROP_FPS)
    width = video.get(propId=cv.CAP_PROP_FRAME_WIDTH)
    height = video.get(propId=cv.CAP_PROP_FRAME_HEIGHT)
    frame_cnt = video.get(propId=cv.CAP_PROP_FRAME_COUNT)

    print("fpt:",fpt , " width:",width , " height:",height , " frameCnt:",frame_cnt)

def img_total(path_file_name):
    img = cv.imread(path_file_name)
    print(img.shape)
