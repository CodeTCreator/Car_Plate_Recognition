# функция для создания файла-шаблона, где надо просто заполнить поля
# функция для считывания файла и возврат массива

def CreatingTemplateFile():
    my_file = open("Шаблон заполнения.csv","w+")
    my_file.write("Номер свидетельства:\nРегистрационный знак:\nКем выдано:\n"
                  "Собственник (владелец):\nАдрес владельца:\n"
                  "VIN:\nМарка, модель:\nКузов:\nОбъем двигателя:\nМощность двигателя:\nЦвет:\n"
                  "Дата выдачи: yyyy-mm-dd\n")
    my_file.close

# Замена названий для работы с БД
def TranslationNames(names):
    if names == "Номер свидетельства":
        names = "number_vrc"
    elif names == "number_vrc":
        names = "Номер свидетельства"
    if names == "Регистрационный знак":
        names = "car_plate"
    elif names == "car_plate":
        names = "Регистрационный знак"
    if names == "Кем выдано":
        names = "issued"
    elif names == "issued":
        names = "Кем выдано"
    if names == "Собственник (владелец)":
        names = "fio"
    elif names == "fio":
        names = "Собственник (владелец)"
    if names == "Адрес владельца":
        names = "address"
    elif names == "address":
        names = "Адрес владельца"
    if names == "VIN":
        names = "vin"
    elif names == "vin":
        names = "VIN"
    if names == "Марка, модель":
        names = "brand_model"
    elif names == "brand_model":
        names = "Марка, модель"
    if names == "Кузов":
        names = "body"
    elif names == "body":
        names = "Кузов"
    if names == "Объем двигателя":
        names = "engine_capacity"
    elif names == "engine_capacity":
        names = "Объем двигателя"
    if names == "Мощность двигателя":
        names = "car_power"
    elif names == "car_power":
        names = "Мощность двигателя"
    if names == "Цвет":
        names = "color"
    elif names == "color":
        names = "Цвет"
    if names == "Дата выдачи":
        names = "date_issued"
    elif names == "date_issued":
        names = "Дата выдачи"
    return names
# Считывание значений для
def ReadingTemplateFile(name_file):
    dictionary = {}
    with open(name_file,'r') as file:
        for line in file:
            key = line[:(line.find(":"))]
            key = TranslationNames(key)
            value = line[(line.find(":")) + 1:]
            value = value.rstrip("\n")
            if value[0] == " ":
                dictionary[key] = value[1:]
            else:
                dictionary[key] = value
    return dictionary
if __name__ == '__main__':
    ReadingTemplateFile("Шаблон заполнения.txt")