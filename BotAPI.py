import telebot
import CarRecBot

result = ""
if __name__ == '__main__':
    bot = telebot.TeleBot('6001012585:AAFeLLydQ06dW8byI_3C1zK1fppxPse_TEk');
    @bot.message_handler(content_types=['text','audio'])
    def get_text_messages(message):
            if message.text == "Привет":
                bot.send_message(message.from_user.id, "Приветствую")
            elif message.text == "/help":
                bot.send_message(message.from_user.id, "Данный бот способен распознавать автомобильные номера (пока только российские). \n "
                                                       "Для того, чтобы бот распознал номера - загрузите фотографию боту и он выдаст ответ")
            else:
                bot.send_message(message.from_user.id, "Заглушка")
    @bot.message_handler(content_types=['photo'])
    def photo_id(message):
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)

        with open("image.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
            result = CarRecBot.MainRecognition('image.jpg')
        if (result):
            bot.send_message(message.from_user.id, "Результат: " + result)
        else:
            bot.send_message(message.from_user.id, "Результат: не найден")
    bot.polling(none_stop=True, interval=0)