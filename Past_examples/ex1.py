import cv2
def ex1(line):
    src = cv2.imread(line)
    gr = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gr, (3, 3), 0)
    canny = cv2.Canny(blurred, 10, 250)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)
    contours = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    for cont in contours:
            #сглаживание и определение количества углов
            sm = cv2.arcLength(cont, True)
            apd = cv2.approxPolyDP(cont, 0.02*sm, True)
            #выделение контуров
            if len(apd) == 4:
                cv2.drawContours(src, [apd], -1, (0,255,0), 4)
    cv2.imshow('res', src)  # выводим итоговое изображение в окно
    cv2.waitKey()