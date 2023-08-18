from paddleocr import PaddleOCR, draw_ocr
from PIL import Image

import id_card_straight


class IdCard:
    # img = ""
    # def __init__(self):
    #     self.img = "aaaa"

    def scanner(self,img_path):
        print("start orc:")
        ocr = PaddleOCR(use_angle_cls=True, lang="ch")

        result = ocr.ocr(img_path, cls=True)

        self.show(result)

        self.idcard(result)


    def showImg(self,result,img_path):
        result = result[0]
        image = Image.open(img_path).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores)
        im_show = Image.fromarray(im_show)
        im_show.save('result.jpg')

    def show(self,result):
        for row in result[0]:
            print("===========")
            print(row)
            # print(row[1][0])

    def idcard(self,result):
        txtArr = []
        for line in result[0]:
            txt = line[1][0]
            # 发现朝鲜文、彝文的身份证
            if (("姓" in txt and "性" in txt and "住" in txt) or ("名" in txt and "别" in txt and "生" in txt)) and \
                    line[1][1] < 0.75:
                continue
            else:
                txtArr.append(txt)

        postprocessing = id_card_straight.IdCardStraight(txtArr)
        # 将结果送入到后处理模型中
        id_result = postprocessing.run()
        print(id_result)

IdCard = IdCard()
IdCard.scanner("./../id_3.jpg")