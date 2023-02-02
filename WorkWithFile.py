# функция для создания файла-шаблона, где надо просто заполнить поля
# функция для считывания файла и возврат массива

def CreatingTemplateFile():
    my_file = open("Шаблон заполнения.csv","w+")
    my_file.write("Номер свидетельства:\nГос.номер:\nКем выдано:\n"
                  "ФИО владельца:\nАдрес владельца:\n"
                  "VIN:\nПроизводитель:\nКузов:\nОбъем двигателя:\nМощность:\nЦвет:\n"
                  "Дата выдачи: yyyy-mm-dd\n")
    my_file.close

# Замена названий для работы с БД
def TranslationNames(names):
    if names == "Номер свидетельства":
        names = "number_vrc"
    if names == "Гос.номер":
        names = "car_plate"
    if names == "Кем выдано":
        names = "issued"
    if names == "ФИО владельца":
        names = "fio"
    if names == "Адрес владельца":
        names = "address"
    if names == "VIN":
        names = "vin"
    if names == "Производитель":
        names = "brand_model"
    if names == "Кузов":
        names = "body"
    if names == "Объем двигателя":
        names = "engine_capacity"
    if names == "Мощность":
        names = "car_power"
    if names == "Цвет":
        names = "color"
    if names == "Дата выдачи":
        names = "data_issued"
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