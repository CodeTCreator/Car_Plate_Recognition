import copy
import re

import numpy as np
import matplotlib.pyplot as plt
import cv2
import pytesseract

from Past_examples.ex1 import ex1
from Past_examples.main import get_string_num

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
carplate_haar_cascade = cv2.CascadeClassifier('XML_files/haarcascade_russian_plate_number.xml')
car_haar_cascade = cv2.CascadeClassifier('XML_files/cars.xml')
#массив xml файлов букв и цифр номеров
symbol_haar_cascade = ['XML_files/XML-letters/A.xml','XML_files/XML-letters/B.xml','XML_files/XML-letters/Y.xml','XML_files/XML-letters/C.xml',
                       'XML_files/XML-letters/E.xml','XML_files/XML-letters/H.xml','XML_files/XML-letters/K.xml','XML_files/XML-letters/M.xml',
                       'XML_files/XML-letters/O.xml','XML_files/XML-letters/P.xml','XML_files/XML-letters/T.xml','XML_files/XML-letters/X.xml']
idea = cv2.CascadeClassifier('XML_files/XML-letters/haarcascade_russian_plate_number_symbol.xml')
symbol_result = []
result = ''

#Обнаружение букв
def letters_detect(image):
    car_overlay = image.copy()
    car_rects = idea.detectMultiScale(car_overlay, scaleFactor=1.1, minNeighbors=3)
    for x, y, w, h in car_rects:
        cv2.rectangle(car_overlay, (x, y), (x + w, y + h), (255, 0, 0), 1)

    return car_overlay

# вырезание номеров
def letters_extract(image):
    cv2.imshow('res', image)
    cv2.waitKey()
    letters = idea.detectMultiScale(image, scaleFactor=1.2, minNeighbors=9)



    #letters = carplate_haar_cascade.detectMultiScale(image, scaleFactor=1.2, minNeighbors=9)

    for x, y, w, h in letters:
            symbol_result.append(image[y + 15:y + h - 10,
                           x + 15:x + w - 20])
#Увеличение масштаба
def enlarge_letters(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    return resized_image


#основная функция
def recognition_letters_on_auto_plate(image):
    carplate_img = image #'image/car8.jpg'


    # обнаружение букв
    detected_letters_img = letters_detect(carplate_img)
    cv2.imshow('!!!!', detected_letters_img)
    cv2.waitKey()

    # вырезание номера
    letters_carplate_extract = letters_extract(detected_letters_img)
    #plt.imshow(carplate_extract_img)
    #plt.show()

    # увеличение номера
    #carplate_extract_img = enlarge_img(carplate_extract_img, 150)
    # plt.imshow(carplate_extract_img)
    # plt.show()


    # # Гауссово размытие
    # #kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # #image = cv2.filter2D(carplate_extract_img_gray, -1, kernel)
    # blurred = cv2.GaussianBlur(carplate_extract_img_gray, (1, 1), 0)
    # cv2.imshow('resGauss', blurred)
    # cv2.waitKey()
    #
    # #Усредненное размытие
    # img_blur_7 = cv2.blur(carplate_extract_img_gray, (7, 7))
    # cv2.imshow('resAveraging', blurred)
    # cv2.waitKey()
    #
    # #Медианное размытие
    # cv2.medianBlur(carplate_extract_img_gray, 1)
    # cv2.imshow('resMedian', carplate_extract_img_gray)
    # cv2.waitKey()
    for letter in symbol_result:
        cv2.imshow('{letter}', letter)
        cv2.waitKey()
