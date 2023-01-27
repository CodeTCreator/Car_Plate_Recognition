import pytesseract
import cv2
import numpy as np
from imutils import contours


def getting_cont(line):
    image = cv2.imread(line)
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    image = cv2.filter2D(image, -1, kernel)
    blurred = cv2.GaussianBlur(image, (3, 3), 0)
    img_grey = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('origin1', img_grey)
    # set a thresh
    thresh = 150

    # get threshold image
    ret, thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)

    # find contours
    contr, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # create an empty image for contours
    for cont in contr:
            #сглаживание и определение количества углов
            sm = cv2.arcLength(cont, True)
            apd = cv2.approxPolyDP(cont, 0.02*sm, True)
            #выделение контуров
            if len(apd) == 4:
                cv2.drawContours(image, [apd], -1, (0,255,0), 4)
    cv2.imshow('res', image)  # выводим итоговое изображение в окно
    cv2.waitKey()
    img_contours = np.uint8(np.zeros((image.shape[0], image.shape[1])))


    #cv2.imwrite("result.png",cv2.drawContours(img_contours, contr, -1, (255, 255, 255), 1))
    # cv2.imshow('origin', image) # выводим итоговое изображение в окно
    cv2.imshow('res', img_contours)  # выводим итоговое изображение в окно

    cv2.waitKey()
    cv2.destroyAllWindows()
    return img_contours

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
def get_string_num(line):
    image = cv2.imread(line)
    height, width, _ = image.shape
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('res', gray)  # выводим итоговое изображение в окно
    cv2.waitKey()
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts, _ = contours.sort_contours(cnts[0])

    for c in cnts:
        area = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        if area > 5000:
            img = image[y:y + h, x:x + w]
            result = pytesseract.image_to_string(img, lang="rus+eng")
            if len(result) < 7:
                print(result)


# if __name__ == '__main__':
#     #ex = getting_cont('image/car.jpg')
#    # get_string_num('image/3.jpg')
#     # ex = getting_cont('image/car1.jpg')
#     # ex = getting_cont('image/car2.jpg')
#     # ex = getting_cont('image/car3.jpg')
#     # ex = getting_cont('image/car5.jpg')
#     # ex = getting_cont('image/car6.jpg')
#     # ex = getting_cont('image/car7.jpg')
#     # ex = getting_cont('image/car8.jpg')
#     # get_string_num('image/car.jpg')
#     # ex = getting_cont('image/number.jpg')
#     # getting_cont('/car1.JPG')
#     # getting_cont('/car2.JPG')
#     # getting_cont('/car3.JPG')
#     # getting_cont('/car4.JPG')
#     # getting_cont('/car5.JPG')
#     # get_string_num('/car.JPG')
#     number = 2345
#     a = number // 1000
#     c = (number // 100) % 10
#     b = (number // 10) % 10
#
#     print(a,b,c)

