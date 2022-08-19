import psycopg2

conn = psycopg2.connect(database="personal_info", user="postgres", password="overlord")
cur = conn.cursor()

def create_db():
    conn = psycopg2.connect(database="personal_info", user="postgres", password="overlord")
    cur = conn.cursor()

    cur.execute("""
            DROP TABLE Phone_num;
            DROP TABLE Base_info;
            """)



    cur.execute("CREATE TABLE IF NOT EXISTS Base_info ("
            "   id SERIAL PRIMARY KEY,"
            "   name VARCHAR(40) NOT NULL,"
            "   second_name VARCHAR(40) NOT NULL,"
            "   email VARCHAR(100) NOT NULL UNIQUE);"
            "CREATE TABLE IF NOT EXISTS Phone_num ("
            #Номера начинаются с +7, поэтому не INTEGER а VARCHAR
            "   num VARCHAR(12) UNIQUE,"
            "   base_id INTEGER REFERENCES Base_info(id));")

    conn.commit()
    cur.close()
    conn.close()


def default_info():
    conn = psycopg2.connect(database="personal_info", user="postgres", password="overlord")
    cur = conn.cursor()

    cur.execute("""
            INSERT INTO Base_info(name, second_name, email)
            VALUES('Джон', 'Рэмбо', 'johnrambo@yandex.ru'),
                  ('Хан', 'Соло', 'hansolo@mail.ru'),
                  ('Тайлер', 'Дерден', 'taylerdarden@gmail.com');
            """)

    conn.commit()



    cur.execute("""
            INSERT INTO Phone_num(num, base_id)
            VALUES(88005553535, 1),
                  (+79123456789, 2),
                  (2222222, 2);
            """)
    conn.commit()
    cur.close()
    conn.close()


def add_client():
    conn = psycopg2.connect(database="personal_info", user="postgres", password="overlord")
    cur = conn.cursor()

    name = input('Введите имя: ')
    second_name = input('Введите фамилию: ')
    email = input('Введите email: ')
    cur.execute("""
                INSERT INTO Base_info(name, second_name, email)
                VALUES(%s, %s, %s);
                """, (name, second_name, email))
    conn.commit()
    i = 1
    while i == 1:
        i = int(input("""1-Да
2-Нет
Желаете добавить номер?: """))
        if i == 1:
            num = input('Введите номер: ')
            cur.execute("""
                        SELECT MAX(id) FROM Base_info;
                        """)
            last_num = cur.fetchall()
            base_id = last_num[0][0]

            cur.execute("""
                        INSERT INTO Phone_num(num, base_id)
                        VALUES(%s, %s);
                        """, (num, base_id))
            conn.commit()
    cur.execute("""
                SELECT * FROM Base_info bi
                LEFT JOIN Phone_num pn ON bi.id = pn.base_id
                """)
    return print(cur.fetchall())

def add_phone():
    conn = psycopg2.connect(database="personal_info", user="postgres", password="overlord")
    cur = conn.cursor()

    num = input('Введите номер:')
    cur.execute("""
                SELECT * FROM Base_info bi
                LEFT JOIN Phone_num pn ON bi.id = pn.base_id
                """)
    print(cur.fetchall())
    base_id = int(input('Введите id клиента: '))
    cur.execute("""
                INSERT INTO Phone_num(num, base_id)
                VALUES(%s, %s);
                """,(num, base_id))
    cur.execute("""
                SELECT * FROM Base_info bi
                LEFT JOIN Phone_num pn ON bi.id = pn.base_id
                """)
    return print(cur.fetchall())

def change_info():
    conn = psycopg2.connect(database="personal_info", user="postgres", password="overlord")
    cur = conn.cursor()
    cur.execute("""
                SELECT * FROM Base_info bi
                LEFT JOIN Phone_num pn ON bi.id = pn.base_id
                 """)
    print(cur.fetchall())

    change_id = int(input('Введите id пользователя: '))
    name = input('Введите новое имя: ')
    second_name = input('Введите новую фамилию: ')
    email = input('Введите новый email: ')

    cur.execute("""
                UPDATE Base_info
                SET name=%s, second_name=%s, email=%s
                WHERE id=%s
                """, (name, second_name, email, change_id))

    num_change = int(input("""1-Да
2-Нет"
Хотите поменять номер телефона?: """))

    if num_change == 1:
        num = input('Введите новый номер: ')
        cur.execute("""
                    UPDATE Phone_num
                    SET num=%s
                    WHERE base_id=%s
                    """, (num, change_id))

    cur.execute("""
                    SELECT * FROM Base_info bi
                    LEFT JOIN Phone_num pn ON bi.id = pn.base_id
                     """)
    return print(cur.fetchall())

def delete_phone():
    conn = psycopg2.connect(database="personal_info", user="postgres", password="overlord")
    cur = conn.cursor()
    cur.execute("""
                SELECT * FROM Base_info bi
                LEFT JOIN Phone_num pn ON bi.id = pn.base_id
                 """)
    print(cur.fetchall())

    change_id =input('Введите id пользователя: ')
    cur.execute("""
                DELETE FROM Phone_num WHERE base_id=%s
                """, (change_id))

    cur.execute("""
                SELECT * FROM Base_info bi
                LEFT JOIN Phone_num pn ON bi.id = pn.base_id
                 """)
    return print(cur.fetchall())

def delete_person():
    conn = psycopg2.connect(database="personal_info", user="postgres", password="overlord")
    cur = conn.cursor()
    cur.execute("""
                    SELECT * FROM Base_info bi
                    LEFT JOIN Phone_num pn ON bi.id = pn.base_id
                     """)
    print(cur.fetchall())

    change_id = input('Введите id пользователя: ')

    cur.execute("""
                DELETE FROM Phone_num WHERE base_id=%s
                """, (change_id))
    cur.execute("""
                DELETE FROM Base_info WHERE id=%s
                """, (change_id))

    cur.execute("""
                SELECT * FROM Base_info bi
                LEFT JOIN Phone_num pn ON bi.id = pn.base_id
                """)
    return print(cur.fetchall())

def search_person():
    conn = psycopg2.connect(database="personal_info", user="postgres", password="overlord")
    cur = conn.cursor()
    ###Этого кода нет в реализации. Он нужен что бы вам было легче проверять#####
    cur.execute("""
                       SELECT * FROM Base_info bi
                       LEFT JOIN Phone_num pn ON bi.id = pn.base_id
                        """)
    print(cur.fetchall())
    #############################################################################
    choise = int(input("""1-Имя
2-Фамилия
3-Email
4-Телефон
По какому кретерию вы хотите найти информацию?: """))

    if choise == 1:
        name = input("Введите имя: ")
        cur.execute("""
                    SELECT * FROM Base_info bi
                    LEFT JOIN Phone_num pn ON bi.id = pn.base_id
                    WHERE name IN (%s);
                    """,(name,))
        return print(cur.fetchall())

    if choise == 2:
        second_name = input("Введите фамилию: ")
        cur.execute("""
                       SELECT * FROM Base_info bi
                       LEFT JOIN Phone_num pn ON bi.id = pn.base_id
                       WHERE second_name IN (%s);
                       """, (second_name,))
        return print(cur.fetchall())

    if choise == 3:
        email = input("Введите Email: ")
        cur.execute("""
                       SELECT * FROM Base_info bi
                       LEFT JOIN Phone_num pn ON bi.id = pn.base_id
                       WHERE email IN (%s);
                       """, (email,))
        return print(cur.fetchall())

    if choise == 4:
        phone_num = input("Введите Email: ")
        cur.execute("""
                       SELECT * FROM Base_info bi
                       LEFT JOIN Phone_num pn ON bi.id = pn.base_id
                       WHERE num IN (%s);
                       """, (phone_num,))
        return print(cur.fetchall())
cur.close()
conn.close()

create_db()
default_info()
# add_client()
# add_phone()
# change_info()
# delete_phone()
# delete_person()
search_person()
