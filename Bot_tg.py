import json
import os
import datetime
import telebot
from telebot import types
from database import for_dostavka, menu_main, cat_is_stop, dish_is_stop, is_done, registration, find_id_user, \
    add_comment, show_my_orders, ordering, is_canceled, show_comment, time_costs, set_mark, for_cook, stat

bot = telebot.TeleBot('6236696473:AAH_OGgS5jBhtDC7ZRA8lJwXHHZkQCfxZwg')

"""Все id"""
id_all = []
id_all_dict = {}


def all_id():
    global id_all
    global id_all_dict
    with open("id_user.json", "r", encoding='utf-8') as read_file:
        id_all_dict = json.load(read_file)
    id_all = [x for sublist in list(id_all_dict.values()) for x in sublist]
    print(id_all)


all_id()

"""Переменная для регистрации"""
reg = {}
"""Переменная для заказа"""
order_dish = {}
"""Переменная для меню"""
menu_ = menu_main()

"""Кнопки"""
"""Для отмены заказа"""
keyb_my_orders = types.InlineKeyboardMarkup()
keyb_my_orders.add(*(types.InlineKeyboardButton('Меню', callback_data='menu'),
                     types.InlineKeyboardButton('Отменить заказ', callback_data='del_orders')))
"""Для администрации"""
keyb_start_users = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyb_start_users.add(*(types.KeyboardButton('Меню'),
                       types.KeyboardButton('Мои заказы'),
                       types.KeyboardButton('Отзывы')))

"""Для регистрации"""
keyb_reg = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyb_reg.add(types.KeyboardButton('Зарегистрироваться'))

"""Для меню категорий"""


def menu_cat(val):
    if val == 'menu':
        keyb_menu = types.InlineKeyboardMarkup()
        keyb_menu.add(*(types.InlineKeyboardButton(a, callback_data='m' + a) for a in menu_.keys()))
        return keyb_menu
    elif val == 'ocenka':
        keyb_menu = types.InlineKeyboardMarkup()
        keyb_menu.add(*(types.InlineKeyboardButton(a, callback_data='o' + a) for a in menu_.keys()))
        return keyb_menu


"""Добавление блюд"""


def keyb_add_dish():
    key_d = types.InlineKeyboardMarkup()
    key_d.add(*(types.InlineKeyboardButton('Да', callback_data=f'menu'),
                types.InlineKeyboardButton('Нет', callback_data=f'finish_dish')))
    return key_d


def keyb_finish_order():
    key_d = types.InlineKeyboardMarkup()
    key_d.add(*(types.InlineKeyboardButton('Да', callback_data=f'finish_order'),
                types.InlineKeyboardButton('Нет', callback_data=f'cancel_order')))
    return key_d


"""Для блюд"""


def dishs(category, message_id, val):
    if val == 'dish':
        for dish in menu_[category]:
            text = ''
            photo1 = ''
            for info in dish:
                if info == dish[1]:
                    text += f'Название - {info}\n'
                elif info == dish[3]:
                    text += f'Стоимость - {info}\n'
                elif info == dish[5]:
                    text += f'Время готовки - {info}\n'
                elif info == dish[2]:
                    photo1 = open(f'img/{info}', 'rb')
                elif info == dish[4]:
                    text += f'Состав - {info}\n'
            bot.send_photo(message_id, photo=photo1, caption=text)
            keyb_ = types.InlineKeyboardMarkup()
            keyb_.add(types.InlineKeyboardButton('Заказать', callback_data=f'*{dish[1]}'))
            bot.send_message(message_id, '👇', reply_markup=keyb_)
    elif val == 'comment':
        for dish in menu_[category]:
            text = ''
            photo1 = ''
            for info in dish:
                if info == dish[1]:
                    text += f'Название - {info}\n'
                elif info == dish[2]:
                    photo1 = open(f'img/{info}', 'rb')
                elif info == dish[4]:
                    text += f'Состав - {info}'
            bot.send_photo(message_id, photo=photo1, caption=text)
            keyb_ = types.InlineKeyboardMarkup()
            keyb_.add(types.InlineKeyboardButton('Оценить', callback_data=f'@{dish[1]}'))
            bot.send_message(message_id, 'Для оценки жми "Оценить"\n Оценка блюда от 1 до 5', reply_markup=keyb_)


"""Admin"""


def next1(name=0, d=0):
    next1 = types.InlineKeyboardMarkup()
    if name == 1 and d == 0:
        b1 = types.InlineKeyboardButton(text="Заказ сделан", callback_data="Заказ сделан")
        next1.add(b1)
    elif d == 1 and name == 1:
        b1 = types.InlineKeyboardButton(text="Заказ доставлен", callback_data="Заказ доставлен")
        next1.add(b1)
    elif name == 0 and d == 1:
        b1 = types.InlineKeyboardButton(text="Заказ доставлен", callback_data="Заказ сделан")
        next1.add(b1)
        b2 = types.InlineKeyboardButton(text="Пока что все", callback_data="Пока что все")
        next1.add(b2)
    elif name == 0 and d == 0:
        b1 = types.InlineKeyboardButton(text="Заказ сделан", callback_data="Заказ сделан")
        next1.add(b1)
        b2 = types.InlineKeyboardButton(text="Пока что все", callback_data="Пока что все")
        next1.add(b2)
    return next1


def keyb_admin():
    keyb_admin = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(text="Категория на стоп или ран", callback_data="category")
    keyb_admin.add(b1)
    b2 = types.InlineKeyboardButton(text="Блюдо на стоп или ран", callback_data="dish")
    keyb_admin.add(b2)
    return keyb_admin


def stop_or_run(word=0):
    if word == "category":
        keyb_admin = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(text="стоп", callback_data="cat_stop")
        keyb_admin.add(b1)
        b2 = types.InlineKeyboardButton(text="возообновить", callback_data="cat_run")
        keyb_admin.add(b2)
    else:
        keyb_admin = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(text="стоп", callback_data="dish_stop")
        keyb_admin.add(b1)
        b2 = types.InlineKeyboardButton(text="возообновить", callback_data="dish_run")
        keyb_admin.add(b2)
    return keyb_admin


""""""


@bot.message_handler(
    content_types=['sticker', 'voice', 'audio', 'document', 'photo', 'video', 'caption', 'contact', 'location',
                   'venue'])
def spam(message):
    print(message.from_user.id)
    bot.send_message(message.chat.id, f'не ломай бота пж')


@bot.message_handler(content_types=['text'])
def start(message):
    global menu_
    if message.text == '/update' and message.chat.id in id_all_dict["super_admin"]:
        menu_ = menu_main()
        bot.send_message(message.chat.id, f'Обновленная информация выглядит так {str(menu_)}')
    if message.text == 'Запиши' and message.chat.id in id_all_dict['dostavka']:
        if message.from_user.id not in id_all_dict['members_of_dostavka']:
            id_all_dict['members_of_dostavka'].append(message.from_user.id)
            with open('id_user.json', 'w', encoding='utf-8') as file:
                json.dump(id_all_dict, file, ensure_ascii=False)
            all_id()
            bot.send_message(message.chat.id, 'Спасибо, что присоеденились в группу "Доставка"')
    if message.text == '/start':
        if message.chat.id not in id_all:
            bot.send_message(message.chat.id, 'Здравствуйте! \n Вам надо зарегистрироваться', reply_markup=keyb_reg)
        else:
            bot.send_message(message.chat.id, 'Здравствуйте!', reply_markup=keyb_start_users)
    if message.text == 'Зарегистрироваться':
        bot.send_message(message.chat.id, 'Регистрация')
        mesg = bot.send_message(message.chat.id, 'Введите логин')
        bot.register_next_step_handler(mesg, login)
    if message.text == '/run':
        if message.chat.id in id_all_dict['povars']:
            bot.send_message(message.chat.id, 'Если хотите ввести номер приготовленного заказа нажмите на кнопку',
                             reply_markup=next1(1))
        if message.chat.id in id_all_dict['dostavka']:
            bot.send_message(message.chat.id, 'Если хотите ввести номер доставленного заказа нажмите на кнопку',
                             reply_markup=next1(1, 1))
        if message.chat.id in id_all_dict['super_admin']:
            bot.send_message(message.chat.id, 'Нажмите, что хотите остановить или возообновить',
                             reply_markup=keyb_admin())
    if message.text == 'Меню':
        bot.send_message(message.from_user.id, 'Выберите категорию', reply_markup=menu_cat('menu'))
    if message.text == 'Мои заказы':
        orders = show_my_orders(message.chat.id)
        for order in orders:
            bot.send_message(message.chat.id, order)
        bot.send_message(message.chat.id,
                         f'Если хотите отменить заказ нажмите отменить или возвращайтесь в стартовое меню',
                         reply_markup=keyb_my_orders)
    if message.text == 'Отзывы':
        comments = show_comment()
        comments = comments[:10]
        comments_message = ''
        for comment in comments:
            comments_message += comment + '\n'
        bot.send_message(message.from_user.id, comments_message)
    if message.text == '/rating':
        bot.send_message(message.from_user.id, 'Выберите категорию', reply_markup=menu_cat('ocenka'))
    if message.text == '/statis':
        if message.chat.id in id_all_dict["super_admin"]:
            statist = stat()
            bot.send_message(message.chat.id, statist)


def login(message):
    bot.send_message(message.chat.id, "ваш логин - " + message.text)
    reg.setdefault(message.chat.id, dict())
    reg[message.chat.id].setdefault("name", message.text)
    mesg = bot.send_message(message.chat.id, 'Введите телефон')
    bot.register_next_step_handler(mesg, phone)


def phone(message):
    if message.text.isdigit():
        bot.send_message(message.chat.id, "ваш телефон - " + message.text)
        reg[message.chat.id].setdefault('phone_number', message.text)
        reg[message.chat.id].setdefault('tg_id', message.chat.id)
        mesg = bot.send_message(message.chat.id, 'Введите пароль мин. 6 символов')
        bot.register_next_step_handler(mesg, password)


def password(message):
    if len(message.text) < 6:
        bot.send_message(message.chat.id, "мало символов")
        mesg = bot.send_message(message.chat.id, 'Введите пароль мин. 6 символов')
        bot.register_next_step_handler(mesg, password)
    else:
        bot.send_message(message.chat.id, "ваш пароль - " + message.text)
        reg[message.chat.id].setdefault("password", message.text)
        id_all_dict['users'].append(message.chat.id)
        print(reg[message.chat.id])
        with open('id_user.json', 'w', encoding='utf-8') as file:
            json.dump(id_all_dict, file, ensure_ascii=False)
        print(registration(reg[message.chat.id]))
        all_id()
        # функция
        bot.send_message(message.chat.id, "Вы успешно зарегистрировались")
        bot.send_message(message.chat.id, "Для начала заказа нажмите меню", reply_markup=keyb_start_users)


def next_step(message):
    if message.chat.id in id_all_dict['povars']:
        dict_info = for_dostavka(message.text)
        keyb11 = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(text="Принять", callback_data=dict_info.split()[3])
        keyb11.add(b1)
        bot.send_message(id_all_dict['dostavka'][0], dict_info, reply_markup=keyb11)
        tekst = 'Если хотите отметить сделанным еще заказ нажмите на кнопку "Заказ сделан"'
        bot.send_message(message.chat.id, tekst, reply_markup=next1())
    elif message.chat.id in id_all_dict['dostavka']:
        tekst = 'Если хотите отметить сделанным еще заказ нажмите на кнопку "Заказ сделан"'
        bot.send_message(message.chat.id, tekst, reply_markup=next1(0, 1))


def cat_stop(message, word):
    # Нужна проверка по списку блюд или категорий
    cat = menu_.keys()
    cat_tekst = ':\n'
    for i in cat:
        cat_tekst += i + ' \n'
    if word == 'cat_stop':
        if message.text in menu_.keys():
            cat_is_stop(message.text, "стоп")
            tekst = 'Если хотите отметить что-то еще выберите нужно'
            bot.send_message(message.chat.id, tekst, reply_markup=keyb_admin())
        else:
            bot.send_message(message.chat.id,
                             f'Такой категории нет, попробуйте заново используя эти названия {cat_tekst}',
                             reply_markup=keyb_admin())
    else:

        if message.text in menu_.keys():
            cat_is_stop(message.text)
            tekst = 'Если хотите отметить что-то еще выберите нужно'
            bot.send_message(message.chat.id, tekst, reply_markup=keyb_admin())
        else:
            bot.send_message(message.chat.id,
                             f'Такой категории нет, попробуйте заново используя эти названия {cat_tekst}',
                             reply_markup=keyb_admin())


def dish_stop(message, word):
    values_list = []
    for cat in menu_.values():
        for dish in cat:
            values_list.append(dish[0])
    dish_tekst = ':\n'
    for i in values_list:
        dish_tekst += i + '\n'

    if word == 'dish_stop':
        dish_is_stop(message.text, "стоп")
        if message.text in values_list:
            tekst = 'Если хотите отметить что-то еще выберите нужно'
            bot.send_message(message.chat.id, tekst, reply_markup=keyb_admin())
        else:
            bot.send_message(message.chat.id,
                             f'Такого блюда нет, попробуйте заново используя эти названия {dish_tekst}',
                             reply_markup=keyb_admin())
    else:
        dish_is_stop(message.text)
        if message.text in values_list:
            tekst = 'Если хотите отметить что-то еще выберите нужно'
            bot.send_message(message.chat.id, tekst, reply_markup=keyb_admin())
        else:
            bot.send_message(message.chat.id,
                             f'Такого блюда нет, попробуйте заново используя эти названия {dish_tekst}',
                             reply_markup=keyb_admin())


def new_com(message, text):
    keybo = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(text="Принять комментарий", callback_data='GoodComment')
    keybo.add(b1)
    b2 = types.InlineKeyboardButton(text="Отклонить комментарий", callback_data='BadComment')
    keybo.add(b2)
    bot.send_message(message.from_user.id, 'Спасибо за ваш отзыв')
    com = message.text + ' @' + text
    bot.send_message(id_all_dict["super_admin"][0], com, reply_markup=keybo)
    bot.delete_message(message.from_user.id, message.message_id)


"""Добавление блюд"""


def add_dish(message, name_dish):
    if message.text.isdigit() and int(message.text) < 15:
        if message.chat.id in order_dish:
            order_dish[message.chat.id]['tg_id'] = message.chat.id
            if 'dishs' in order_dish[message.chat.id]:
                order_dish[message.chat.id]['dishs'][name_dish] = int(message.text)
            else:
                order_dish[message.chat.id].setdefault('dishs', {name_dish: int(message.text)})
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, f'Вы заказали {name_dish} - {message.text} порции')
            bot.send_message(message.chat.id, 'Желаете что-то еше', reply_markup=keyb_add_dish())
        else:
            order_dish.setdefault(message.chat.id, {'tg_id': message.chat.id})
            order_dish[message.chat.id].setdefault('dishs', {name_dish: int(message.text)})
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, f'Вы заказали {name_dish} - {message.text} порции')
            bot.send_message(message.chat.id, 'Желаете что-то еше', reply_markup=keyb_add_dish())
    else:
        msg = bot.send_message(message.chat.id, f'Вы ввели не верное значение\nВведите количество - {name_dish}')
        bot.register_next_step_handler(msg, add_dish, name_dish)


def address_dish(message):
    if len(message.text) < 80:
        order_dish[message.chat.id]['address'] = f'{message.text}'
        order_dish[message.chat.id]['state2'] = 'adress finish'
        with open(f'orders/{message.from_user.id}.json', 'w', encoding='utf-8') as file:
            json.dump(order_dish[message.from_user.id], file, ensure_ascii=False)
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, f'Ваш адрес {message.text}')
        msg = bot.send_message(message.chat.id, f'Добавьте комментарий')
        bot.register_next_step_handler(msg, comment_dish)
    else:
        msg = bot.send_message(message.chat.id, f'Вы ввели не верное значение\nВведите адрес')
        bot.register_next_step_handler(msg, address_dish)


def comment_dish(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Ваш комментарий добавлен -  ' + message.text)
    order_dish[message.chat.id]['comment'] = f'{message.text}'
    order_dish[message.chat.id]['state3'] = 'comment_finish'
    with open(f'orders/{message.from_user.id}.json', 'w', encoding='utf-8') as file:
        json.dump(order_dish[message.from_user.id], file, ensure_ascii=False)
    finish_set = time_costs(order_dish[message.chat.id]['dishs'])
    bot.send_message(message.chat.id, finish_set)
    bot.send_message(message.chat.id, 'Оформить заказ?', reply_markup=keyb_finish_order())


"""Команда для оценки блюда"""


def dish_rating(message, name_dish):
    if message.text.isdigit() and int(message.text) in [1, 2, 3, 4, 5]:
        # {'dish_name': 'мороженное', 'mark': 5}
        info = {'dish_name': name_dish, 'mark': int(message.text)}
        set_mark(info)
        bot.send_message(message.from_user.id, f'Вы оценили {name_dish} в оценку - {message.text}')
    else:
        bot.send_message(message.from_user.id, 'Вы ввели некоректные данные')
        msg = bot.send_message(message.chat.id, f'Поставте оценку от 1 до 5')
        bot.register_next_step_handler(msg, dish_rating, name_dish)


"""Отмена заказа"""


def order_del(message):
    id_order = message.text
    """функция кторая принимает id и ставит его на стоп"""
    is_canceled(int(id_order))
    bot.send_message(message.chat.id, f'Заказ № {id_order} отменен \n Введите /start для возврата в старт меню')


"""Проверка на збой при оформлении заказа"""


def proverka():
    orders_list_id = os.listdir('orders')
    for order in orders_list_id:
        with open(f'orders/{order}', 'r', encoding='utf-8') as file:
            data = json.load(file)
        order_dish[int(data['tg_id'])] = data
        if 'state3' in data.keys():
            bot.send_message(data['tg_id'], 'Оформить заказ?', reply_markup=keyb_finish_order())
        elif 'state2' in data.keys():
            msg = bot.send_message(data['tg_id'], f'Добавьте комментарий')
            bot.register_next_step_handler(msg, comment_dish)
        elif 'state1' in data.keys():
            msg = bot.send_message(data['tg_id'], f'Введите адрес')
            bot.register_next_step_handler(msg, address_dish)
        else:
            bot.send_message(data['tg_id'], 'Произошла ошибка оформите заказ заново', reply_markup=menu_cat('menu'))
            os.remove(f'orders/{order}')


""""""
proverka()


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'menu':
        bot.send_message(call.from_user.id, 'Выберите категорию', reply_markup=menu_cat('menu'))
    elif call.data == 'BadComment':
        bot.send_message(call.message.chat.id, "комментарий НЕ ОПУБЛИКОВАН")
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'GoodComment':
        bot.send_message(call.message.chat.id, "комментарий  ОПУБЛИКОВАН")
        add_comment({'comment': [call.message.text]})
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == 'Хочу коммент':
        text = 'Напишите комментарий'
        a = bot.send_message(call.message.chat.id, text)
        bot.register_next_step_handler(a, new_com, call.from_user.username)
    elif call.data == 'Не хочу коммент':
        text = 'Спасибо, что пользовались нашими услугами'
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, text)
    elif call.data[0] == 'm':
        massage_id = call.from_user.id
        print(call.data[1:])
        dishs(call.data[1:], massage_id, 'dish')
    elif call.data == "Заказ доставлен":
        text = 'Введите номер доставленного заказа'
        a = bot.send_message(call.message.chat.id, text)
        bot.register_next_step_handler(a, next_step)
    elif call.data == 'Заказ сделан':
        text = 'Введите номер приготовленного заказа'
        a = bot.send_message(call.message.chat.id, text)
        bot.register_next_step_handler(a, next_step)
    elif call.data == 'Пока что все':
        if call.message.chat.id in id_all_dict['povars']:
            bot.send_message(call.message.chat.id,
                             'Спасибо, если будет готово еще какое-то блюдо, нажмите кнопку "Заказ сделан" ',
                             reply_markup=next1(1))
        if call.message.chat.id in id_all_dict['dostavka']:
            bot.send_message(call.message.chat.id,
                             'Спасибо, если будет доставлено еще какое-то блюдо, нажмите кнопку "Заказ сделан" ',
                             reply_markup=next1(1, 1))
    elif call.data == 'category':
        # прописать через if
        bot.send_message(call.message.chat.id, 'Выберите, что хотите сделать ', reply_markup=stop_or_run(call.data))
    elif call.data == 'dish':
        # прописать через if
        bot.send_message(call.message.chat.id, 'Выберите, что хотите сделать ', reply_markup=stop_or_run(call.data))
    elif call.data == 'dish_stop' or call.data == 'dish_run':
        # прописать через if
        text = 'Введите название блюда'
        word = call.data
        a = bot.send_message(call.message.chat.id, text)
        bot.register_next_step_handler(a, dish_stop, word)
    elif call.data == 'cat_stop' or call.data == 'cat_run':
        # прописать через if
        word = call.data
        text = 'Введите название категории'
        a = bot.send_message(call.message.chat.id, text)
        bot.register_next_step_handler(a, cat_stop, word)
    elif call.data[0] == '*':
        msg = bot.send_message(call.message.chat.id, f'Введите количество - {call.data[1:]}')
        bot.register_next_step_handler(msg, add_dish, call.data[1:])
    elif call.data == 'finish_dish':
        order_dish[call.from_user.id]['state1'] = 'order finish'
        with open(f'orders/{call.from_user.id}.json', 'w', encoding='utf-8') as file:
            json.dump(order_dish[call.from_user.id], file, ensure_ascii=False)
        msg = bot.send_message(call.message.chat.id, f'Введите адрес')
        bot.register_next_step_handler(msg, address_dish)
    elif call.data == 'finish_order':
        print(order_dish[call.message.chat.id])
        ordering(order_dish[call.message.chat.id]['dishs'], order_dish[call.message.chat.id])
        cook = for_cook()
        cook = list(cook)
        bot.send_message(id_all_dict["povars"][0], str(cook))
        date_order = datetime.date.today()
        try:
            os.mkdir(f'orders_add/{date_order}')
        except:
            pass
        with open(f'orders_add/{date_order}/{call.message.chat.id}___{cook}.json', 'w',
                  encoding='utf-8') as file:
            json.dump(list(cook), file, ensure_ascii=False)
        os.remove(f'orders/{call.message.chat.id}.json')
        order_dish[call.message.chat.id] = {}
        bot.send_message(call.message.chat.id, f'Ваш заказ принят\nЕсли хотите оформить еще заказ жмите меню',
                         reply_markup=keyb_start_users)
    elif call.data == 'cancel_order':
        os.remove(f'orders/{call.message.chat.id}.json')
        order_dish[call.message.chat.id] = {}
        bot.send_message(call.message.chat.id, f'Ваш заказ отменен\nЕсли хотите оформить еще заказ жмите меню',
                         reply_markup=keyb_start_users)
    elif call.data == 'del_orders':
        mseg = bot.send_message(call.message.chat.id, 'Введите id заказа который надо отменить')
        bot.register_next_step_handler(mseg, order_del)
    elif call.data[0] == 'o':
        massage_id = call.from_user.id
        dishs(call.data[1:], massage_id, 'comment')
    elif call.data[0] == '@':
        msg = bot.send_message(call.message.chat.id, f'Поставте оценку от 1 до 5')
        bot.register_next_step_handler(msg, dish_rating, call.data[1:])
    elif int(call.data) in range(1500) and call.message.chat.id in id_all_dict['dostavka']:
        a = call.message.text
        keyb22 = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(text="Доставленно", callback_data=a.split()[3])
        keyb22.add(b1)
        bot.send_message(call.from_user.id, a, reply_markup=keyb22)
        # new
        d = call.message.text + '\n' + 'Заказ принят доставщиком - ' + '@' + call.from_user.username
        bot.send_message(call.message.chat.id, d)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif int(call.data) in range(1500) and call.from_user.id in id_all_dict['members_of_dostavka']:
        # функция что доставленно из базы данных
        # print(f'number ===== {call.data}')
        keyb22 = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(text="Да", callback_data='Хочу коммент')
        keyb22.add(b1)
        b1 = types.InlineKeyboardButton(text="Нет", callback_data='Не хочу коммент')
        keyb22.add(b1)
        b = call.message.text
        b = b.split()[3]
        adress = find_id_user(b)
        bot.send_message(adress, "Хотите оставить комментарий?", reply_markup=keyb22)

        is_done(int(call.data))
        # new
        d = call.message.text + '\n' + 'ЗАКАЗ ДОСТАВЛЕН'
        bot.send_message(call.from_user.id, d)
        bot.send_message(id_all_dict["super_admin"][0], d + f' заказчиком - @{call.from_user.username}')
        bot.delete_message(call.from_user.id, call.message.message_id)


print("Ready")
bot.infinity_polling()
