import psycopg2
import WorkWithFile
from psycopg2 import OperationalError

conn = 0
cursor = 0
# Основная функция добавления данных в БД
def AddInDatabase(name_file): # передавать словарь
    global cursor,conn
    data = WorkWithFile.ReadingTemplateFile(name_file)
    AddInTable_Driver(data['fio'],data['address'])
    data['id_driver'] = GetIdDriver(data['fio'],data['address'])
    AddInTable_VRC(data['number_vrc'],data['car_plate'],data['id_driver'],data['issued'])
    data['id_certificate'] = GetIdVRC(data['number_vrc'],data['car_plate'],data['id_driver'],data['issued'])
    AddInTable_Vehicle(data['id_certificate'],data['vin'],data['brand_model'],
                       data['body'],data['engine_capacity'],data['car_power'],data['color'])
    AddInTable_A_VRC(data['id_certificate'],data['data_issued'])
    conn.commit()
    print("Все успешн добавлено")

# Вспомогательные функции добавления данных в каждую таблицу БД
def AddInTable_VRC(number,plate,id_driver,issued):
    cursor.execute(
        "INSERT INTO vrc (number_vrc,car_plate,id_driver,issued) "
        f"VALUES ('{number}','{plate}',{id_driver},'{issued}')"
    )
def AddInTable_A_VRC(id,data_issued):
    cursor.execute(
        "INSERT INTO a_vrc (id_certificate,date_issued) "
        f"VALUES ({id},'{data_issued}')"
    )
def AddInTable_Vehicle(id,vin,brand,body,engine_capacity,power,color):
    cursor.execute(
        "INSERT INTO vehicle (id_certificate,vin,brand_model,body,engine_capacity,car_power,color) "
        f"VALUES ({id}, '{vin}', '{brand}', '{body}', {engine_capacity},{power},'{color}')"
    )
def AddInTable_Driver(fio,address):
    cursor.execute(
        f"INSERT INTO driver (FIO,Address) VALUES ('{fio}','{address}')"
    )

# Получение id владельца авто
def GetIdDriver(fio,address):
    global cursor
    cursor.execute(
        "Select id_driver from driver "
        f"where fio = '{fio}' and address = '{address}' "
    )
    records = cursor.fetchone()
    return records[0]
# Получения id свидетельства
def GetIdVRC(number_vrc,car_plate,id_driver,issued):
    global cursor
    cursor.execute(
        "Select id_certificate from vrc "
        f"where number_vrc = '{number_vrc}' and car_plate = '{car_plate}' and"
        f" id_driver = '{id_driver}' and issued = '{issued}'"
    )
    records = cursor.fetchone()
    return records[0]

# Получение информации из БД по номеру авто (car_plate)
def GetInfobyCarPlate(car_plate):
    global cursor
    dictionary = {}
    cursor.execute(
        "select vrc.number_vrc,vrc.issued,vehicle.vin,vehicle.brand_model,"
        "vehicle.body,vehicle.engine_capacity,vehicle.car_power,"
        "vehicle.color,driver.fio,driver.address,a_vrc.date_issued"
        " from vrc"
        " join vehicle on vehicle.id_certificate = vrc.id_certificate"
        " join a_vrc on a_vrc.id_certificate = vrc.id_certificate "
        " join driver on driver.id_driver = vrc.id_driver "
        f" where vrc.car_plate = '{car_plate}'"
    )
    records = cursor.fetchone()
    if records:
        dictionary['car_plate'] = car_plate
        dictionary['number_vrc'] = records[0]
        dictionary['issued'] = records[1]
        dictionary['vin'] = records[2]
        dictionary['brand_model'] = records[3]
        dictionary['body'] = records[4]
        dictionary['engine_capacity'] = records[5]
        dictionary['car_power'] = records[6]
        dictionary['color'] = records[7]
        dictionary['fio'] = records[8]
        dictionary['address'] = records[9]
        dictionary['date_issued'] = records[10]
    #print(records)
    return dictionary

# Получение таблицы водителей
def PrintTableDriver():
    cursor.execute(
        "Select * from driver"
    )
    records = cursor.fetchall()
    print(records)

# Подключение к базе данных
def ConnectToDatabase():
    global conn,cursor
    conn = psycopg2.connect(dbname='Vehicle_database', user='Admin_VD',
                            password='Admin_VD', host='localhost', port='5432')
    cursor = conn.cursor()
# Отключение от базы данных
def DisconnectToDatabase():
    global conn, cursor
    conn.close
    cursor.close

# Перевод из словаря в текст
def ConvertDictionaryToText(dictionary):
    text = ""
    for key,value in dictionary.items():
        key = WorkWithFile.TranslationNames(key)
        text = text + key + ": " + str(value) + "\n"
    return text

# Ответ на запрос бота
def ResponseRequest(car_plate):
   return ConvertDictionaryToText(GetInfobyCarPlate(car_plate))

if __name__ == '__main__':


    ConnectToDatabase()
    ResponseRequest()
    DisconnectToDatabase()
# 1 - Владельца добавляем
# 2 - Сор ТС
# 3 - дальше всех добавляем

# Сделать получение информации по номеру авто

# Сделать чтобы выдавало русскими словами описание авто
# Поменять обработку текста, а точнее заменять русские символы на английские