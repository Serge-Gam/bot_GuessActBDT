#идея такова: чтобы не дергать постоянно базу мы при обращении к базе за файлом заодно сохраняем правильный ответ
#после того как юзер даст ответ мы сравниваем его с правильным и очищаем хранилище (не базу, а хранилище!)
# -*- coding: utf-8 -*-
import shelve
from SQLighter import SQLighter
from config import shelve_name, database_name
from random import shuffle
from telebot import types

def count_rows():
    '''
    данный метод считает количество строк в базе данных,
    и сохраняет его в хранилище
    затем из этого количества мы будем
    выбирать
    '''

    db = SQLighter(database_name)
    rowsnum = db.count_raws()#это должно работать!
    with shelve.open(shelve_name) as storage:#with - используем для того чтобы не запариваться об
        #открытии бд и закрытии
        storage['row_count'] = rowsnum
        #print(storage['row_count'])

def get_rows_count():
    '''
    Получает из хранилища количество строк в базе данных
    :return: (int) количество строк
    '''
    with shelve.open(shelve_name) as storage:
        rowsnum = storage['row_count']
        print(rowsnum)
    return rowsnum

def set_user_game(chat_id, estimated_answer):
    """
    Записываем юзера в игроки и запоминаем что он должен ответить
    :param chat_id:  id  юзера
    :param estimated_answer: правильный ответ (из БД)
    :return:
    """
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = estimated_answer

def finish_user_game(chat_id):
    """
    Заканчиваем игру текущего юзера и удаляем правильный ответ из хранилища
    :param caht_id: id  юзера
    """
    with shelve.open(shelve_name) as storage:
        del storage[str(chat_id)]

def get_answer_for_user(chat_id):
    """
    Получаем правильный ответ для текущего юзера
    в случае если человек просто ввел какие то символы, не начав игру, возвращаем None
    :param chat_id: id юзера
    :return: (str)  правильный ответ /None
    """
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        #если человек не играет - ничего не возвращаем
        except KeyError:
            return None


#добавим клавиатуру с вариантами ответов
def generate_markup(right_answer, wrong_answers):
    """
    Создаем кастомную клвиатуру для выбора правильного ответа
    :param right_answer: Правильный ответ
    :param wrong_answer: Набор неправильных ответов
    :return: Объект кастомной клавиатуры
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
    #Склеиваем правильный ответ с неправильными
    all_answers = "{},{}".format(right_answer, wrong_answers)
    #создаем массив и записываем в него все элементы
    list_items = []
    for item in all_answers.split(','):
        list_items.append(item)
    #хорошенько перемешаем эти элементы
    shuffle(list_items)
    #заполним разметку перемешанными элементами
    for item in list_items:
        markup.add(item)
    return markup
