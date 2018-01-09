#запишем полученные photo_id из файла file_id_dict в нашу базу данных
import sqlite3
import random

conn = sqlite3.connect('actors_bdt_db.db')
cur = conn.cursor()


def write_photo_id_to_bd():  #запишем полученные photo_id из файла file_id_dict в нашу базу данных
    file = open('file_id_dict.txt', 'r')
    my_string = file.read()

    dict = eval(my_string)

    for item in dict:
        cur.execute('''
            UPDATE Actor
            SET photo=? 
            WHERE id=?''', (dict.get(item),item)
                    )
    conn.commit()

#получилось

#вылезает ошибка из-за кривой базы
#почемуто айдишники идут не по порядку

#исправляем

def make_right_ids():
    cur.executescript('''
    DROP TABLE IF EXISTS Actors;

    CREATE TABLE Actors (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE,
        sex TEXT,
        photo INTEGER UNIQUE,
        photo_name INTEGER,
        wrong_answers TEXT,
        link TEXT
        
        );

    INSERT INTO Actors (name, sex, photo, photo_name, wrong_answers)
    SELECT name, sex, photo, id, wrong_answers FROM Actor;

    DROP TABLE IF EXISTS Actor;

    ALTER TABLE Actors RENAME TO Actor
    ''')
    conn.commit()

