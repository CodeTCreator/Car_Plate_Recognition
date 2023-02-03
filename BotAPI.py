import time

import telebot
import CarRecBot
import DataBase
result = ""
if __name__ == '__main__':
    bot = telebot.TeleBot('6001012585:AAFeLLydQ06dW8byI_3C1zK1fppxPse_TEk');

    # Ответы на простые предложения
    @bot.message_handler(content_types=['text','audio'])
    def get_text_messages(message):
            if message.text == "Привет":
                bot.send_message(message.from_user.id, "Приветствую")
            elif message.text == "/help":
                bot.send_message(message.from_user.id, "Данный бот способен распознавать автомобильные номера (пока только российские). \n "
                                                       "Для того, чтобы бот распознал номера - загрузите фотографию боту и он выдаст ответ")
            else:
                bot.send_message(message.from_user.id, "Заглушка")

    #Обработка фотографии и выдача результата распознавания
    @bot.message_handler(content_types=['photo'])
    def photo_id(message):
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("image.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
            start_time = time.time()
            result = CarRecBot.MainRecognition('image.jpg')
            print("Номера: " + result)
            #print("--- %s seconds --- step8" % (time.time() - start_time))
            print("Время распознания номера %s " % round(time.time() - start_time,5))
        if (result):
            DataBase.ConnectToDatabase()
            start_time = time.time()
            RequestResult = DataBase.ResponseRequest(result)
            print("Время ответа БД %s " % round(time.time() - start_time, 5))
            DataBase.DisconnectToDatabase()
            if (len(RequestResult) > 0):
                bot.send_message(message.from_user.id, "Результат: ")
                bot.send_message(message.from_user.id, RequestResult)
            else:
                bot.send_message(message.from_user.id, "Результат: ")
                bot.send_message(message.from_user.id, "Регистрационный знак: " + result + "\n" +
                                 "Данные в базе не обнаружены")
        else:
            bot.send_message(message.from_user.id, "Результат: номера не распознаны")
    bot.polling(none_stop=True, interval=0)