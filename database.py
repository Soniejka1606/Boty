import sqlite3 as sl

"""
SELECT ('столбцы или * для выбора всех столбцов; обязательно')
FROM ('таблица; обязательно')
WHERE ('условие/фильтрация, например, city = 'Moscow'; необязательно')
GROUP BY ('столбец, по которому хотим сгруппировать данные; необязательно')
HAVING ('условие/фильтрация на уровне сгруппированных данных; необязательно')
ORDER BY ('столбец, по которому хотим отсортировать вывод; необязательно')
"""

con = sl.connect('DATABASE.db', check_same_thread=False)

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
with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS MarkDish (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            mark TEXT DEFAULT 4);
    """)

with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS Comments (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            comment TEXT);
    """)


def add_comment(dict_):
    '''
    :param dict_: берет словарь вида {"comment":['dfjvfjnjfjbngj"]}
    :return:  аписывает комментарий
    '''
    try:
        sql_insert = f"INSERT INTO Comments (comment) values(?)"
        with con:
            con.execute(sql_insert, (dict_["comment"]))
        return True
    except Exception as e:
        return e


# print(add_comment({"comment":['все восхитительно, очень классное оформление заказа быстро и понятно']}))
def show_comment():  # Возвращает все комментарии
    commets = []
    try:
        data = con.execute(f"SELECT comment FROM Comments")
        data = data.fetchall()
        for i in data:
            for j in i:
                commets.append(j)
        return commets
    except Exception as e:
        return e


# print(show_comment())
def set_mark(dict_):  # принимает словарь на оценку блюда
    '''
    :param dict_: словарь {dish_name: что-то,mark:5}
    :return: новое среднее значение
    '''
    new_mark = 0
    try:
        mark = 0
        data = con.execute(f"SELECT mark FROM MarkDish WHERE name='{dict_['dish_name'].capitalize()}'")
        data = data.fetchall()

        for i in data:
            for k in i:
                mark = k
        new_mark = (float(mark) + dict_['mark']) / 2
        new_mark = round(new_mark, 2)
        new_mark = str(new_mark)
    except Exception as e:
        print(e)
    try:
        nm = f"UPDATE MarkDish SET mark = {new_mark} WHERE name = '{dict_['dish_name']}' "
        with con:
            con.execute(nm)
    except Exception as e:
        print("Ошибка: ", e)
    return new_mark


# print(set_mark({'dish_name': 'мороженное','mark':5}))

def registration(dict_):
    # print(dict_)
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
                con.execute(sql_insert, (dict_["name"], dict_["phone_number"], dict_["password"], dict_["tg_id"]))
            return True
        except:
            return False
    else:
        try:
            sql_insert = f"INSERT INTO User (name,phone_number,password,vk_id) values(?,?,?,?)"
            with con:
                con.execute(sql_insert, (dict_["name"], dict_["phone_number"], dict_['password'], dict_["vk_id"]))
            return True
        except:
            return False


# registration({"tg_id": 515215,"name": "KAtya","phone_number":55525,"password":"drftgyhfdfgg"})

def ordering(order_dish, order_addreess):
    """
    функция значала заполняет таблицу Orders по адресу и user_id
    потом OrderDish
    :param order_dish, order_addreess,id - cловари {tg_id:fhjmgjmgj}
    :return: заполненные таблицы плюс время ожидание заказа в переменной time
    """
    # забираем с таблицы user значение user_id
    if "tg_id" in order_addreess.keys():
        try:
            data = con.execute(f"SELECT id FROM User WHERE tg_id={order_addreess['tg_id']}")
            data = data.fetchall()
            user_id = 0
            for i in data:
                for k in i:
                    user_id = k
        except:
            return False
    else:
        try:
            data = con.execute(f"SELECT id FROM User WHERE tg_id={order_addreess['vk_id']}")
            data = data.fetchall()
            user_id = 0
            for i in data:
                for k in i:
                    user_id = k
        except:
            return False
    # добавляем адресс и user_id в таблицум Orders, формируя заказ для получения его номера
    try:
        sql_insert = f"INSERT INTO Orders (user_id,address) values(?,?)"
        with con:
            con.execute(sql_insert, (user_id, order_addreess["address"]))
    except Exception as e:
        return print(e)
    # поиск последнего добавленного заказа по user_id, находим order_id, чтобы потом заполнять OrderDish
    try:
        order_id = con.execute(f"SELECT id FROM Orders WHERE user_id={user_id} ORDER BY id DESC LIMIT 1")
        order_id = order_id.fetchall()
        for i in order_id:
            for k in i:
                order_id = k
    except:
        return False
    # заполнение OrderDish поля order_id,dish,count
    for dish, count in order_dish.items():
        dish_id = con.execute(f"SELECT id FROM Dish WHERE name='{dish}'")
        dish_id = dish_id.fetchall()
        for i in dish_id:
            for k in i:
                dish_id = k
        # return dish_id
        try:
            print(dish_id, count, order_id)
            orderdish = f"INSERT INTO Order_dish (dish_id,count,order_id) values(?,?,?)"
            with con:
                con.execute(orderdish, (dish_id, count, order_id))
        except Exception as e:
            print("Ошибка: ", e)
            return False

    # добавление коментария
    try:
        # com = f"INSERT INTO Orders (comment_to_order) values(?) WHERE id = {order_id} "
        com = f"UPDATE Orders SET comment_to_order = ? WHERE Id = ?"
        with con:
            con.execute(com, (order_addreess["comment"], order_id))
    except Exception as e:
        print("Ошибка: ", e)
        return False
    # подсчет времени на готовку
    return "done"


# print(ordering({"Котлета": 2, "Щи": 2}, {'address': "Лебедева8", 'tg_id': 423423423423, "comment": 'Вилки и ножи'}))


def time_costs(order_dish):  # Собобщение для клиента перед подтверждением заказа
    '''
    :param order_dish: {словарь блюдо:количество}
    :return: время готовки стоимость и список блюд
    '''
    dishes = 'Заказанные блюда:\n'
    time = 30
    cost = 0
    for dish, count in order_dish.items():
        try:
            time_cook = con.execute(f'''SELECT {count} * Dish.time_of_cook,
                                                {count} * Dish.costs
                                            FROM Dish
                                            WHERE Dish.name = '{dish}' ''')
            time_cook = time_cook.fetchall()
            # print(time_cook)
            dishes += f'{dish} в количестве {count} шт.\n'
            for i in time_cook:
                time += i[0]
                cost += i[1]
        except Exception as e:
            print(e)
    if time > 60:
        hours = time // 60
        minutes = time % 60
        time_of_cook = f"{hours} часов {minutes} минут"
    else:
        time_of_cook = f"{time} минут"
    kartoczka = f'Заказ на сумму {cost} руб. будет доставлен через {time_of_cook}\n'
    kartoczka += dishes
    return kartoczka


# print(time_costs({"Чизкейк":1,"Котлета":1}))


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
        data = data.fetchall()  # данные повару первая цифра номер заказа потом блюдо и количество
        orders_ids = []
        for i in data:
            orders_ids.append(i[0])
        orders_ids = set(orders_ids)  # id заказов чтобы обозначить что началось готовиться
        orders_ids = list(orders_ids)
        orders_ids.append(2)
        orders_ids = tuple(orders_ids)
        # print(orders_ids)
        try:
            orderdish = f"UPDATE Orders SET is_start_cook = 1 WHERE Id in {orders_ids}"
            with con:
                con.execute(orderdish)
        except Exception as e:
            print("Ошибка: ", e)
        kartoczka = []
        dict_ = {}
        for i in data:
            if i[0] not in dict_.keys():
                dict_[i[0]] = f'Блюдо: {i[1]} в количестве {i[2]} шт.\n'
            else:
                dict_[i[0]] += f'Блюдо: {i[1]} в количестве {i[2]} шт.\n'
        for k, v in dict_.items():
            kartoczka.append(f'Заказ номер - {k}:\n{v} ')

        return kartoczka


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
    # print(f'data ----- {data1}')
    dish_list = ':\n'
    for i in data1:
        dish_list += f' {i[0]} в количестве {i[1]} шт \n '
        # for d in i:
        #     # print(d)
        #     # dish_list += f'{d}  шт \n'
        #     # dishes.append(d)
    # print(dish_list)
    text_dict = {}  # Текст для доставщика
    data_text = ''
    for i in data:
        data_text += "id заказа - " + str(i[0]) + '\n'
        data_text += "адрес - " + str(i[1]) + '\n'
        data_text += "комментарий - " + str(i[2]) + '\n'
        data_text += "номер телефона - " + str(i[3]) + '\n'
        data_text += "стоимость заказа - " + str(i[4]) + 'руб. \n'
        data_text += "блюда" + str(dish_list) + "--------"

    return data_text


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

def cat_is_stop(name_cat, word="run"):
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
            return False
    else:
        try:
            orderdish = f"UPDATE CategoryDish SET is_stop = 0 WHERE name = '{name_cat}'"
            with con:
                con.execute(orderdish)
            return True
        except Exception as e:
            print("Ошибка: ", e)
            return False


# print(cat_is_stop("Десерты", "нестоп"))

def dish_is_stop(name_dish, word="run"):
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
            return False
    else:
        try:
            orderdish = f"UPDATE Dish SET is_stop = 0 WHERE name = '{name_dish}'"
            with con:
                con.execute(orderdish)
            return True
        except Exception as e:
            print("Ошибка: ", e)
            return False


# print(dish_is_stop("Мороженное", "стоп"))

def menu_all():
    '''
    :return: генерирует словарь типа {категория:[[все о блюде 1],[все о блюде 2]]}
    '''
    try:
        with con:
            data = con.execute(f'''SELECT CategoryDish.name, Dish.id,Dish.name,Dish.picture,Dish.costs,Dish.ingridients,Dish.time_of_cook
                                    FROM CategoryDish
                                    JOIN Dish ON 
                                    Dish.category_id = CategoryDish.id
                                    ''')
            data = data.fetchall()
            # return data
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

def menu_main():
    '''
    :return: генерирует словарь типа {категория:[[все о блюде 1],[все о блюде 2]]}
    '''
    try:
        with con:
            data = con.execute(f'''SELECT CategoryDish.name, Dish.id,Dish.name,Dish.picture,Dish.costs,Dish.ingridients,Dish.time_of_cook
                                    FROM CategoryDish
                                    JOIN Dish ON 
                                    Dish.category_id = CategoryDish.id
                                    WHERE CategoryDish.is_stop = 0 AND Dish.is_stop = 0 ''')
            data = data.fetchall()
            # return data
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


# print(menu_main())

def show_my_orders(id):
    '''
    :param id: Принимает id пользователя
    :return: выдут все актуальные заказы
    '''
    kartoczki = []
    dict_ = {}
    try:
        with con:
            data1 = con.execute(f'''SELECT User.name,Orders.id, Dish.name,Order_dish.count,Order_dish.count*Dish.costs
                                    FROM User 
                                                JOIN Orders ON 
                                                User.id = Orders.user_id
                                                JOIN Order_dish ON 
                                                Orders.id = Order_dish.order_id
                                                JOIN Dish ON 
                                                Order_dish.dish_id = Dish.id
                                                WHERE User.tg_id = {id} 
                                                AND Orders.is_canceled = 0 
                                                AND Orders.is_done = 0 ''')
            data1 = data1.fetchall()
            for i in data1:
                if i[1] not in dict_.keys():
                    dict_[i[1]] = [[i[2], i[3], i[4]]]
                else:
                    dict_[i[1]].append([i[2], i[3], i[4]])

            for k, v in dict_.items():
                tekst = f'Заказ номер {k}\n'
                cost = 0
                for i in v:
                    tekst += f'Блюдо {i[0]} в количестве {i[1]} шт. суммой {i[2]} руб.\n'
                    cost += i[2]
                tekst += f'Общая сумма равна {cost} руб'
                # print(tekst)
                kartoczki.append(tekst)

        return kartoczki
    except Exception as e:
        print(e)


# for s in show_my_orders(598388419):
#     print(s+'\n------')
#     print(s.split()[2])

def stat():
    '''
    :return: Статистику всего блюд и отмены и плюс популярность блюд
    '''
    tekst = ''
    try:
        with con:
            data1 = con.execute(f'''SELECT COUNT(*),(SELECT COUNT(*) FROM ORders) FROM ORders
                                                WHERE Orders.is_canceled = 1''')
            data1 = data1.fetchall()
            canc = 0
            for i in data1:
                tekst += f'За сегодня отмененных заказов {i[0]}.\nВсего заказов {i[1]}\n'
    except Exception as e:
        print(e)
    try:
        with con:
            data = con.execute(f'''SELECT Dish.name ,SUM(Order_dish.count) FROM Order_dish
                                            JOIN Dish ON 
                                            Order_dish.dish_id = Dish.id
                                            GROUP BY Dish.name 
                                            ORDER BY SUM(Order_dish.count) DESC ''')
            data = data.fetchall()
            popular = 'Популярность блюд:\n'
            k = 0
            for i in data:
                k += 1
                popular += f'{k}) {i[0]}: заказали {i[1]} шт\n'

    except Exception as e:
        print(e)
    tekst += popular

    return tekst


# print(stat())

def clear_table():
    '''
    :return: Очищение таблиц для ежедневной статистики
    '''
    try:
        clear_ = f'''DELETE FROM Orders'''
        with con:
            con.execute(clear_)
    except Exception as e:
        print(e)
    try:
        clear_ = f'''DELETE FROM Order_dish'''
        with con:
            con.execute(clear_)
    except Exception as e:
        print(e)
    return True


def find_id_user(order_id):
    try:
        with con:
            data = con.execute(f'''SELECT tg_id FROM User
                                            JOIN Orders ON
                                            User.id = Orders.user_id
                                                WHERE Orders.id = {order_id}''')
            data = data.fetchall()
            a = data[0][0]
        return a
    except Exception as e:
        print(e)

# print(find_id_user(1))

def show_marks():
    '''
    :return: генерирует словарь типа {категория:[[все о блюде 1],[все о блюде 2]]}
    '''
    try:
        with con:
            data = con.execute(f'''SELECT name,mark
                                    FROM MarkDish
                                    ''')
            data = data.fetchall()
            # return data
    except Exception as e:
        print(e)
    mark ={}
    for i in data:
        mark[i[0]] = i[1]
    return mark