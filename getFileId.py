#при смене токена надо проделать эту операцию еще раз. т.к. идентификаторы уникальны для каждого бота по отдельности
import telebot
import os
import time
import config


bot = telebot.TeleBot(config.token)

#нам нужно получить уникальные id от телеграмма, для этого надо вспомнить как получать сообщения в телеграмме
#логика такая: - отправляем файл, получаем его id, формируем словарь: id:[telegram_id] - потом эти данные вносим в словарь

#научимся принимать сообщения


#почемуто не работает - решено: бот не любит имен файлов набранных кириллицей
@bot.message_handler(commands=['test'])
def find_file_ids(message):
    file_id_dict = {}
    for file in os.listdir('bdt_actor_photo_180x180/'):
        if file.split('.')[-1] == 'jpg':
            file_name = str(file)
            f = open('bdt_actor_photo_180x180/'+file, 'rb')
            bot.send_message(message.chat.id, file)
            msg = bot.send_photo(message.chat.id, f, None)
            # а теперь отправим вслед за ним его файл id
            bot.send_message(message.chat.id, msg.photo[1].file_id,
                              reply_to_message_id = msg.message_id)

            file_rec = {file_name[0:-4] : msg.photo[1].file_id}
            file_id_dict.update(file_rec)
            #print(file_id_dict.txt)


        time.sleep(3)
    print(file_id_dict)




if __name__=='__main__':
    bot.polling(none_stop=True)


