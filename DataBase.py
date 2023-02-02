import psycopg2
import WorkWithFile
from psycopg2 import OperationalError

conn = 0
cursor = 0
# Основная функция добавления данных в БД
def AddInDatabase(name_file): # передавать словарь
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
    cursor.execute(
        "Select id_driver from driver "
        f"where fio = '{fio}' and address = '{address}' "
    )
    records = cursor.fetchone()
    return records[0]
# Получения id свидетельства
def GetIdVRC(number_vrc,car_plate,id_driver,issued):
    cursor.execute(
        "Select id_certificate from vrc "
        f"where number_vrc = '{number_vrc}' and car_plate = '{car_plate}' and"
        f" id_driver = '{id_driver}' and issued = '{issued}'"
    )
    records = cursor.fetchone()
    return records[0]

# Получение информации из БД по номеру авто (car_plate)
def GetInfobyCarPlate(car_plate):
    dictionary = {}

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


if __name__ == '__main__':

    ConnectToDatabase()
    AddInDatabase("Шаблон заполнения.txt")
    DisconnectToDatabase()
# 1 - Владельца добавляем
# 2 - Сор ТС
# 3 - дальше всех добавляем

# Сделать получение информации по номеру авто