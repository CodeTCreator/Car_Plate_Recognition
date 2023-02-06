
import re
import time

import cv2
import pytesseract

from threading import Thread


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
carplate_haar_cascade = cv2.CascadeClassifier('XML_files/haarcascade_russian_plate_number.xml')
car_haar_cascade = cv2.CascadeClassifier('XML_files/cars.xml')

resultImages = []           #Массив изображений, с диапазоном разворота от -10 до 10
massResultString = []       #Массив, куда записываются результаты обработки тессерактом
resultCarPlates = []

# Обнаружение автомобилей
def carDetect(image):
    car_overlay = image.copy()
    car_rects = car_haar_cascade.detectMultiScale(car_overlay, scaleFactor=1.3, minNeighbors=8)
    for x, y, w, h in car_rects:
        cv2.rectangle(car_overlay, (x, y), (x + w, y + h), (255, 0, 0), 5)

    return car_overlay


# Обнаружение номеров
def carplateDetect(image):
    carplate_rects = carplate_haar_cascade.detectMultiScale(image, scaleFactor=1.3, minNeighbors=12)
    for x, y, w, h in carplate_rects:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 5)
    return image


# вырезание номеров
def carplateExtract(image):
    carplate_rects = carplate_haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=12)
    result = 0
    for x, y, w, h in carplate_rects:
        if(w > 150 and h > 50):
            result = image[y + 10:y + h - 10,
                           x + 10:x + w - 20]  # Adjusted to extract specific region of interest i.e. car license plate
        else:
            result = image[y + 10:y + h - 5,
                     x + 10:x + w - 5]
    return result


# Увеличение масштаба картинки номеров
def enlargeImg(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    return resized_image


# Проверка корректности строки
def checkCarRecognition(line):
    if (len(re.findall("[A-Za-zА-Яа-я0][' '|'\'|'|'|'/']?([0-9BOОВ/]{3})[' '|'\'|'|'|'/']?([A-Za-zА-Яа-я0]{2})[' '|'\'|'|'|'/']?([0-9BOОВ]{2,3})",line)) > 0) :
        return re.search("[A-Za-zА-Яа-я0][' '|'\'|'|'|'/']?([0-9BOОВ/]{3})[' '|'\'|'|'|'/']?([A-Za-zА-Яа-я0]{2})[' '|'\'|'|'|'/']?([0-9BOОВ]{2,3})",line).group()


# Повороты изображения
def rotation(img,grad):
    (h, w) = img.shape[:2]
    center = (int(w / 2), int(h / 2))
    rotation_matrix = cv2.getRotationMatrix2D(center, grad, 1.0)
    rotated = cv2.warpAffine(img, rotation_matrix, (w, h))
    return rotated


# Размытия фото
def photoBlurring(carplate_extract_img_gray):
    # Гауссово размытие
    # kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # image = cv2.filter2D(carplate_extract_img_gray, -1, kernel)
    #cv2.imshow('beforeGauss', carplate_extract_img_gray)
    #cv2.waitKey()
    photo = cv2.GaussianBlur(carplate_extract_img_gray, (3, 3), 0)
    #cv2.imshow('afterGauss', photo)
    #cv2.waitKey()

    # Усредненное размытие
    """
    photo = cv2.blur(carplate_extract_img_gray, (7, 7))
    # cv2.imshow('resAveraging', blurred)
    # cv2.waitKey()
    """
    # Медианное размытие
    """
    photo = cv2.medianBlur(carplate_extract_img_gray, 3)
    #cv2.imshow('resMedian', carplate_extract_img_gray)
    #cv2.waitKey()
    """
    return photo



def parallel(resImage):
    x = (pytesseract.image_to_string(resImage,
                                     config=f'--psm 8 --oem 3 ', lang="rus+eng"))
    val = checkCarRecognition(x)
    if val is not None:
        massResultString.append(val)

# Работа с тессерактом
def workWithTesseract(img):
    first = -10
    for i in range(20):
        resultImages.append(rotation(img, first))
        first = first + 1
    # Использование тессеракта; многопоточность
    # massThread = []
    # for i in range(20):
    #     massThread.append(Thread(target=parallel, args=(resultImages[i],)))
    # for i in range(20):
    #     massThread[i].start()
    # for i in range(20):
    #     massThread[i].join()

    # Использование тессеракта; без многопоточности
    for i in range(20):
        x = (pytesseract.image_to_string(resultImages[i],
                                        config=f'--psm 8 --oem 3 ', lang="rus+eng"))
        #print(x)
        val = checkCarRecognition(x)
        if val is not None:
            massResultString.append(val)
        # print(checkCarRecognition(x))


# Анализ массива результатов
def lineAnalysis():
    intermediateArray = []
    for var in massResultString:
        var = var.replace(' ', '')
        if re.match("^[A-Za-zА-Яа-я0]([0-9BOОВ]{3})([A-Za-zА-Яа-я0]{2})[' '|'\'|'|'|'/']?([0-9BOОВ]{2,3})$", var):
            var = var.replace('/', '')
            var = var.replace('|', '')
            intermediateArray.append(var)

    # Удаление переходов на строку
    intermediateArray = [line.rstrip() for line in intermediateArray]
    resultString = ''

    # Обработка массива результатов. Используется промежуточный словарь для запоминания возможного значения,
    # в котором находится максимально часто встречающийся элемент. Он и будет результатом
    for val in range(9):
        supportiveArray = {}
        for value in (intermediateArray):
            if val == len(value):
                if '' in supportiveArray:
                    supportiveArray[''] += 1
                else:
                    supportiveArray[''] = 1
            else:
                if value[val] in supportiveArray:
                    supportiveArray[value[val]] += 1
                else:
                    supportiveArray[value[val]] = 1
        if (len(supportiveArray) > 0):
            resultString += max(supportiveArray, key=supportiveArray.get)
            supportiveArray.clear()
    # print(intermediateArray)
    resultString = list(resultString)

    # Замена всех похожих букв на цифры B - 8, O - 0
    if len(resultString) > 0:
        if resultString[0] == '0':
            resultString[0] = 'O'
        if resultString[4] == '0':
            resultString[4] = 'O'
        if resultString[5] == '0':
            resultString[5] = 'O'
        if resultString[1] == 'B' or resultString[1] == 'В':
            resultString[1] = '8'
        if resultString[1] == 'B' or resultString[1] == 'В':
            resultString[2] = '8'
        if resultString[1] == 'B' or resultString[1] == 'В':
            resultString[3] = '8'
        if resultString[1] == 'B' or resultString[1] == 'В':
            resultString[6] = '8'
        if resultString[1] == 'B' or resultString[1] == 'В':
            resultString[7] = '8'
        if len(resultString) == 9:
            if resultString[1] == 'B' or resultString[1] == 'В':
                resultString[9] = '8'
    resultString = ''.join(resultString)

    return resultString
TranslateDictionary = {
    'А':'A',
    'В':'B',
    'Е':'E',
    'К':'K',
    'М':'M',
    'Н':'H',
    'О':'O',
    'Р':'P',
    'С':'C',
    'Т':'T',
    'У':'У',
    'Х':'X'}

# Перевод в английские буквы и верхний регистр
def translateLetters(line):
    if(ord(line[0]) > 1000):
        line = line.replace(line[0],TranslateDictionary[ line[0].title()],1)
    if (ord(line[4]) > 1000):
        line = line.replace(line[4], TranslateDictionary[ line[4].title()], 1)
    if (ord(line[5]) > 1000):
        line = line.replace(line[5], TranslateDictionary[ line[5].title()], 1)
    return line

# Основная функция
def recognition_auto_plate(line):
    resultImages.clear()
    massResultString.clear()
    resultCarPlates.clear()
    carplate_img = cv2.imread(line)  # 'image/car8.jpg'
    carplate_img_rgb = cv2.cvtColor(carplate_img, cv2.COLOR_BGR2RGB)

    # обнаружение номера
    detected_carplate_img = carplateDetect(carplate_img_rgb)
    # plt.imshow(detected_carplate_img)
    # plt.show()

    # вырезание номера
    carplate_extract_img = carplateExtract(detected_carplate_img)
    resultLine = ""
    if (type(carplate_extract_img) is int):
        return ""
    if (len(carplate_extract_img) > 0):
        # plt.imshow(carplate_extract_img)
        # plt.show()

        # увеличение номера
        carplate_extract_img = enlargeImg(carplate_extract_img, 150)
        # plt.imshow(carplate_extract_img)
        # plt.show()
        # cv2.imshow('beforeThresh', carplate_extract_img)
        # cv2.waitKey()
        # Перевод в серый цвет
        carplate_extract_img_gray = cv2.cvtColor(carplate_extract_img, cv2.COLOR_RGB2GRAY)
        carplate_extract_img_gray = cv2.threshold(carplate_extract_img_gray, 0, 255, cv2.THRESH_OTSU)[1]
        # cv2.imshow('afterThresh', carplate_extract_img_gray)
        # cv2.waitKey()
        # plt.imshow(carplate_extract_img_gray)
        # plt.show()

        # Размытие фото
        image = photoBlurring(carplate_extract_img_gray)
        start_time = time.time()
        # Работа с тессерактом

        workWithTesseract(image)
        # workWithTesseract(carplate_extract_img_gray)
        print("Время распознавания номера %s" % (time.time() - start_time))

        start_time = time.time()
        # Обработка массива результатов
        resultLine = lineAnalysis()
        print("Время обработки массива результатов %s " % (time.time() - start_time))
    return resultLine

if __name__ == '__main__':
    resultCarPlate = recognition_auto_plate('image/car.jpg')
    print("Результат: ",resultCarPlate)


