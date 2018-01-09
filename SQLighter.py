# -*- coding: utf-8 -*-
#При каждом создании объекта будет открываться отдельное соединение с бд и впоследствии закрываться - это очень круто
#в этом файле создадим класс, объектом этого класса будет являться соединение с бд, и добавим разные методы
import sqlite3

class SQLighter:

    #инициализируем функцию, подключаем базу данных

    def __init__(self, database):
        self.connection = sqlite3.connect(database)#подключаем базу
        self.cursor = self.connection.cursor()#инициализируем указатель

    def select_all(self):
        """получаем все строки из таблицы актеры"""
        with self.connection:
            return self.cursor.execute('SELECT * FROM Actor').fetchall()

    def select_single(self, rownum):
        '''получаем одну строку с номером  rownum'''
        with self.connection:
            return self.cursor.execute('SELECT * FROM  Actor WHERE id = ?', (rownum,)).fetchall()[0]# запятая после rownum

    def count_raws(self):
        '''считаем количество строк'''
        with self.connection:
            result = self.cursor.execute('SELECT * FROM Actor').fetchall()
            return len(result)#выбираем все и считаем длину

    def close(self):
        ''' закрываем текущее соединение с БД'''
        self.connection.close()
