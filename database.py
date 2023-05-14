import sqlite3 as sl

"""
SELECT ('столбцы или * для выбора всех столбцов; обязательно')
FROM ('таблица; обязательно')
WHERE ('условие/фильтрация, например, city = 'Moscow'; необязательно')
GROUP BY ('столбец, по которому хотим сгруппировать данные; необязательно')
HAVING ('условие/фильтрация на уровне сгруппированных данных; необязательно')
ORDER BY ('столбец, по которому хотим отсортировать вывод; необязательно')
"""

con = sl.connect('DATABASE.db',check_same_thread=False)

with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone_number INTEGER,
            password TEXT,
            vk_id TEXT,
            tg_id TEXT);
    """)

with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            comment_to_order TEXT,
            address TEXT,
            is_canceled BOOLEAN ,
            is_done BOOLEAN ,
            is_start_cook BOOLEAN);
    """)

with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS Order_dish (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            dish_id INTEGER,
            count INTEGER,
            order_id INTEGER);
    """)

with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS Dish (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category_id INTEGER,
            picture BLOB ,
            time_of_cook INTEGER ,
            is_stop BOOLEAN);
    """)

with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS CategoryDish (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            is_stop BOOLEAN);
    """)

def registration(dict_):
    #  функция принимает в качестве аргумента словарь со значениями, возвращает TRUE при успехе или ошибку при ошибке
    """
    :param Словарь:
    :return: таблицу User c заполненными данными
    vk_id TEXT,
    tg_id TEXT);
    """
    if "tg_id" in dict_.keys():
        try:
            sql_insert = f"INSERT INTO User (name,phone_number,password,tg_id) values(?,?,?,?)"
            with con:
                con.execute(sql_insert,(dict_["name"],dict_["phone_number"],dict_["password"],dict_["tg_id"]))
            return True
        except:
            return False
    else:
        try:
            sql_insert = f"INSERT INTO User (name,phone_number,password,vk_id) values(?,?,?,?)"
            with con:
                con.execute(sql_insert,(dict_["name"],dict_["phone_number"],dict_['password'],dict_["vk_id"]))
            return True
        except:
            return False

# registration({"tg_id": 515215,"name": "KAtya","phone_number":55525,"password":"drftgyhfdfgg"})

def ordering(order_dish,order_addreess,id):
    """
    функция значала заполняет таблицу Orders по адресу и user_id
    потом OrderDish
    :param order_dish, order_addreess,id - cловари {tg_id:fhjmgjmgj}
    :return: заполненные таблицы плюс время ожидание заказа в переменной time
    """
    #забираем с таблицы user значение user_id
    if "tg_id" in id.keys():
        try:
            data = con.execute(f"SELECT id FROM User WHERE tg_id={id['tg_id']}")
            data = data.fetchall()
            user_id = 0
            for i in data:
                for k in i:
                    user_id = k
        except:
            return False
    else:
        try:
            data = con.execute(f"SELECT id FROM User WHERE tg_id={id['vk_id']}")
            data = data.fetchall()
            user_id = 0
            for i in data:
                for k in i:
                    user_id = k
        except:
            return False
    #добавляем адресс и user_id в таблицум Orders, формируя заказ для получения его номера
    try:
        sql_insert = f"INSERT INTO Orders (user_id,address) values(?,?)"
        with con:
            con.execute(sql_insert,(user_id,order_addreess["address"]))
    except:
        return False
    #поиск последнего добавленного заказа по user_id, находим order_id, чтобы потом заполнять OrderDish
    try:
        order_id = con.execute(f"SELECT id FROM Orders WHERE user_id={user_id} ORDER BY id DESC LIMIT 1")
        order_id = order_id.fetchall()
        for i in order_id:
            for k in i:
                order_id = k
    except:
        return False
    # заполнение OrderDish поля order_id,dish,count
    for dish,count in order_dish.items():
        dish_id = con.execute(f"SELECT id FROM Dish WHERE name='{dish}'")
        dish_id = dish_id.fetchall()
        for i in dish_id:
            for k in i:
                dish_id = k
        # return dish_id
        try:
            print(dish_id,count,order_id)
            orderdish = f"INSERT INTO Order_dish (dish_id,count,order_id) values(?,?,?)"
            with con:
                con.execute(orderdish, (dish_id,count,order_id))
        except Exception as e:
            print("Ошибка: ", e)
            return False
    #подсчет времени на готовку
    time = con.execute(f'''SELECT Order_dish.count * Dish.time_of_cook
                                FROM Order_dish
                                INNER JOIN Dish ON Order_dish.dish_id = dish.id
                                WHERE Order_dish.order_id = {order_id}''')
    time = time.fetchall()
    all_time = 0
    for s in time:
        for k in s:
            all_time += k
    all_time += 30
    if all_time > 60:
        hours = all_time // 60
        minutes = all_time % 60

        time_of_cook = f"{hours} часов {minutes} минут"
    return time_of_cook

# print(ordering({"Kokos":2,"Banan":2},{'address':"Minskaya"},{'tg_id':515215}))

def show_category():
    '''
    :param id:
    :return: список категорий
    '''
    try:
        with con:
            data = con.execute(f"SELECT name FROM CategoryDish WHERE is_stop = 0")
            data = data.fetchall()
            list_cat = []
            for i in data:
                for s in i:
                    list_cat.append(s)
        return list_cat
    except Exception as e:
        print(e)

# print(show_category())

def show_dish(name_cat):
    '''
    :param name_cat - название категории:
    :return: список блюд из категории
    '''
    try:
        with con:
            data = con.execute(f'''SELECT Dish.name FROM Dish JOIN CategoryDish ON 
                                Dish.category_id = CategoryDish.id WHERE CategoryDish.name = '{name_cat}' 
                                AND Dish.is_stop = 0
                                                                                        ''')
            data = data.fetchall()
            dish_list = []
            for i in data:
                for s in i:
                    dish_list.append(s)
        return dish_list
    except Exception as e:
        print(e)

print(show_dish("desert"))



# def add_cat():
#     try:
#         sql_insert = f"INSERT INTO CategoryDish (name,is_stop) values(?,?)"
#         with con:
#             con.execute(sql_insert,("Fruits",True))
#         return True
#     except:
#         return False
#
# print(add_cat())



# def add_dish():
#     try:
#         sql_insert = f"INSERT INTO Dish (name,time_of_cook) values(?,?)"
#         with con:
#             con.execute(sql_insert,("Banan",10))
#         return True
#     except:
#         return False

#
# def info_table():# функция берет название таблицы и возвращает ее полность #работает
#     with con:
#         data = con.execute(f"SELECT * FROM Order_dish")
#         # print(data)
#         # print(data.fetchall())
#         return data.fetchall()
# print(add_dish())
# print(info_table())

# def ss():
#     time = con.execute(f'''SELECT Order_dish.count * Dish.time_of_cook
#                             FROM Order_dish
#                             INNER JOIN Dish ON Order_dish.dish_id = dish.id
#                             WHERE Order_dish.order_id = {16}''')
#     time = time.fetchall()
#     all_time = 0
#     for s in time:
#         for k in s:
#             all_time+=k
#     all_time+=30
#     if all_time>60:
#         hours = all_time // 60
#         minutes = all_time % 60
#
#         time_of_cook =f"{hours} часов {minutes} минут"
#     return a
#
# print(ss())

