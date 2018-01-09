import config
import telebot
from SQLighter import  SQLighter
import utils
import random
from telebot import types

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['game'])
def game(message):
    #подключаемся к бд
    print(message.chat.id)

    db_worker = SQLighter(config.database_name)

    #Получаем случайную строку из БД из интервала от 1 до количества записей в бд
    choose_random = random.randint(1, utils.get_rows_count())
    print(choose_random)
    row = db_worker.select_single(choose_random)


    #формируем разметку
    markup = utils.generate_markup(row[1].strip(), row[5])#strip - очищаем от пробелов
    print(row[1])

    #отправляем фотку с вариантом ответа
    bot.send_photo(message.chat.id, row[3], reply_markup=markup)#работает

    #включаем игровой режим
    utils.set_user_game(message.chat.id, row[1])

    #отсоединяемся от БД
    db_worker.close()

    #как только юзер начинает игру - мы заносим его id  в хранилище и предполагаем
    # что следующий ответ  - ответ на вопрос
    #напишем хэндлер который реагирует на все сообщения

@bot.message_handler(func = lambda message: True, content_types=['text'])
def chek_answer(message):
    #Если функция возвращает None -> человек не в игре
    answer = utils.get_answer_for_user(message.chat.id)
    #answer может быть либо текст либо none
    #если None
    if not answer:
        bot.send_message(message.chat.id, 'Чтобы начать учиться узнавать актеров выберите команду /game')
    else:
        #Уберем клавиатуру с вариантами ответа
        keyboard_hider = types.ReplyKeyboardRemove()

        #Если ответ правильный/неправильный
        if message.text == answer.strip():
            bot.send_message(message.chat.id, 'Верно! Еще-> /game', reply_markup=keyboard_hider)
        else:
            bot.send_message(message.chat.id, 'Неверно. Это же '+answer+'\n Учить дальше -> /game', reply_markup=keyboard_hider)
            print('Неверно. Это же '+answer+'\n Учить дальше -> /game')
        #Удаляем юзера из хранилища (игра закончена)
        utils.finish_user_game(message.chat.id)


if __name__ == '__main__':
    utils.count_rows()
    random.seed()
    bot.polling(none_stop=True)

