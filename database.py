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
            is_canceled BOOLEAN DEFAULT 0,
            is_done BOOLEAN DEFAULT 0,
            is_start_cook BOOLEAN DEFAULT 0,
            is_cooked BOOLEAN DEFAULT 0);
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
            is_stop BOOLEAN DEFAULT 0);
    """)

with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS CategoryDish (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            is_stop BOOLEAN DEFAULT 0);
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

# print(show_dish("Десерты"))

def for_cook():
    '''
    функция ищет заказы которые не начались готовиться берет номер заказа и список блюд с количеством и выводит текстом
    после этого везде заменяет на то что началось готовиться is_start_cook= True
    :return:
    '''
    with con:
        data = con.execute(f'''SELECT  Orders.id, Dish.name, Order_dish.count  FROM Dish 
                                        JOIN Order_dish ON 
                                        Dish.id = Order_dish.dish_id 
                                        JOIN Orders ON 
                                        Order_dish.order_id = Orders.id  
                                        WHERE Orders.is_start_cook = 0 ''')
        data = data.fetchall() # данные повару первая цифра номер заказа потом блюдо и количество
        orders_ids = []
        for i in data:
            orders_ids.append(i[0])
        orders_ids = set(orders_ids) # id заказов чтобы обозначить что началось готовиться
        orders_ids = tuple(orders_ids)
        try:
            orderdish = f"UPDATE Orders SET is_start_cook = 1 WHERE Id IN {orders_ids}"
            with con:
                con.execute(orderdish)
        except Exception as e:
            print("Ошибка: ", e)
        return data
# print(for_cook())

def for_dostavka(order_id):
    '''
    :param order_id:
    :return: записывает is_cooked = True, и передает всю нужную информацию доставщику
    '''
    # заменяет на то что уже готово
    try:
        orderdish = f"UPDATE Orders SET is_cooked = 1 WHERE Id = '{order_id}'"
        with con:
            con.execute(orderdish)
    except Exception as e:
        print("Ошибка: ", e)
    # формирование информации для доставщика
    try:
        with con:
            data = con.execute(f'''SELECT  Orders.id, Orders.address,Orders.comment_to_order, 
                                            User.phone_number, SUM(Order_dish.count*Dish.costs)
                                            FROM User 
                                            JOIN Orders ON 
                                            User.id = Orders.user_id 
                                            JOIN Order_dish ON 
                                            Orders.id = Order_dish.order_id  
                                            JOIN Dish ON 
                                            Dish.id = Order_dish.dish_id
                                            WHERE Orders.id = {order_id}''')
            data = data.fetchall()

    except Exception as e:
        print(e)
    # запрос на все заказанные блюда с количеством
    try:
        with con:
            data1 = con.execute(f'''SELECT Dish.name,Order_dish.count FROM Dish 
                                                JOIN Order_dish ON 
                                                Dish.id = Order_dish.dish_id 
                                                WHERE Order_dish.order_id = {order_id}''')
            data1 = data1.fetchall()
    except Exception as e:
        print(e)
    dishes = []
    for i in data1:
        for d in i:
            dishes.append(d)
    text_dict = {} # Текст для доставщика
    for i in data:
        text_dict["id заказа"] = i[0]
        text_dict["адрес"] = i[1]
        text_dict["комментарий"] = i[2]
        text_dict["номер телефона"] = i[3]
        text_dict["стоимость заказа"] = i[4]
        text_dict["блюда"] = dishes
    return  text_dict
# print(for_dostavka(2))


def is_done(order_id):
    '''
    :param order_id:  номер заказа
    :return: отмечает is-done = True ==> заказ доставлен
    '''
    try:
        orderdish = f"UPDATE Orders SET is_done = 1 WHERE Id = '{order_id}'"
        with con:
            con.execute(orderdish)
        return True
    except Exception as e:
        print("Ошибка: ", e)
# print(is_done(1))

def is_canceled(order_id):
    '''

    :param order_id:
    :return: ставит галочку is_canceled, что заказ отменен возвращает номер заказа
    '''
    try:
        orderdish = f"UPDATE Orders SET is_canceled = 1 WHERE Id = '{order_id}'"
        with con:
            con.execute(orderdish)
        return order_id
    except Exception as e:
        print("Ошибка: ", e)
# print(is_canceled(1))

def cat_is_stop(name_cat, word):
    '''
    :param name_cat:
    :param word: если стоп то меняет is_stop = 1, если другое то возвращает 0 и говорит что категория доступна
    :return:
    '''
    if word == "стоп":
        try:
            orderdish = f"UPDATE CategoryDish SET is_stop = 1 WHERE name = '{name_cat}'"
            with con:
                con.execute(orderdish)
            return True
        except Exception as e:
            print("Ошибка: ", e)
    else:
        try:
            orderdish = f"UPDATE CategoryDish SET is_stop = 0 WHERE name = '{name_cat}'"
            with con:
                con.execute(orderdish)
            return True
        except Exception as e:
            print("Ошибка: ", e)
# print(cat_is_stop("Десерты", "нестоп"))

def dish_is_stop(name_dish, word):
    '''
    :param name_cat:
    :param word: если стоп то меняет is_stop = 1, если другое то возвращает 0 и говорит что блюдо доступна
    :return:
    '''
    if word == "стоп":
        try:
            orderdish = f"UPDATE Dish SET is_stop = 1 WHERE name = '{name_dish}'"
            with con:
                con.execute(orderdish)
            return True
        except Exception as e:
            print("Ошибка: ", e)
    else:
        try:
            orderdish = f"UPDATE Dish SET is_stop = 0 WHERE name = '{name_dish}'"
            with con:
                con.execute(orderdish)
            return True
        except Exception as e:
            print("Ошибка: ", e)
# print(dish_is_stop("Мороженное", "стоп"))


def menu_main():
    '''
    :return: генерирует словарь типа {категория:[[все о блюде 1],[все о блюде 2]]}
    '''
    try:
        with con:
            data = con.execute(f'''SELECT CategoryDish.name, Dish.id,Dish.name,Dish.picture,Dish.costs,Dish.ingridients
                                    FROM CategoryDish
                                    JOIN Dish ON 
                                    Dish.category_id = CategoryDish.id
                                    WHERE CategoryDish.is_stop = 0 AND Dish.is_stop = 0 ''')
            data = data.fetchall()
            #return data
    except Exception as e:
        print(e)
    menu = {}
    for i in data:
        if i[0] not in menu.keys():
            a = []
            for s in i[1:]:
                a.append(s)
            menu[i[0]] = [a]
        else:
            a = []
            for s in i[1:]:
                a.append(s)
            menu[i[0]].append(a)
    return menu
print(menu_main())