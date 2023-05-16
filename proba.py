import config

# token = '5907180411:AAGG_L1KNqmIj-3SeuqGBNPYFUe0hL82Dk8'

import time
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telebot.types import InputMediaPhoto
from config import *

bot = telebot.TeleBot('5907180411:AAGG_L1KNqmIj-3SeuqGBNPYFUe0hL82Dk8')

keyb_start = types.InlineKeyboardMarkup()
keyb_start.add(*(types.InlineKeyboardButton('Меню', callback_data='menu'),
                 types.InlineKeyboardButton('Рабочая зона', callback_data='work')))

def menu_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    menu1 = config.menu
    for key in menu1:
        b1 = types.InlineKeyboardButton(text=key, callback_data=key)
        keyboard.add(b1)
    return keyboard



# keyd.add(*(types.KeyboardButton(a[0]) for a in list_of_lists[1:]))
dishes = []
for key in config.menu:
    for item in menu[key]:
        dishes.append(item[0])
user = {}

def keyb_admin():
    keyb_admin = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(text="Категория на стоп или ран", callback_data="category")
    keyb_admin.add(b1)
    b2 = types.InlineKeyboardButton(text="Блюдо на стоп или ран", callback_data="dish")
    keyb_admin.add(b2)
    return keyb_admin
def stop_or_run(word):
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

def next(name = 0,d = 0):
    if name == 1 and d == 0:
        next = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(text="Заказ сделан",callback_data="Заказ сделан")
        next.add(b1)
    elif d ==1 and name==1:
        next = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(text="Заказ доставлен", callback_data="Заказ доставлен")
        next.add(b1)
    elif name == 0 and d ==1:
        next = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(text="Заказ доставлен", callback_data="Заказ сделан")
        next.add(b1)
        b2 = types.InlineKeyboardButton(text="Пока что все", callback_data="Пока что все")
        next.add(b2)
    elif name == 0 and d ==0:
        next = types.InlineKeyboardMarkup()
        b1 = types.InlineKeyboardButton(text="Заказ сделан", callback_data="Заказ сделан")
        next.add(b1)
        b2 = types.InlineKeyboardButton(text="Пока что все", callback_data="Пока что все")
        next.add(b2)
    return next
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        if message.chat.id not in config.users:
            tekst = 'Вы еще не зарегистрированы у нас, хотите зарегистрироваться для псоледующего заказа?'
            yes = types.InlineKeyboardMarkup()
            b1 = types.InlineKeyboardButton(text="yes", callback_data="yes")
            yes.add(b1)
            bot.send_message(message.chat.id, tekst , reply_markup=yes)
    elif message.text =='cook':
        bot.send_message(message.chat.id, 'Если хотите ввести номер приготовленного заказа нажмите на кнопку',reply_markup=next(1))
    elif message.text =='delivery':
        bot.send_message(message.chat.id, 'Если хотите ввести номер доставленного заказа нажмите на кнопку',reply_markup=next(1,1))
    elif message.text =='admin':
        bot.send_message(message.chat.id, 'Нажмите, что хотите остановить или возообновить',reply_markup=keyb_admin())
    else:
        bot.send_message(message.chat.id, 'hello', reply_markup=keyb_start)


def ask_number(message):
    user['name'] = message.text
    number = bot.send_message(message.chat.id, "Напишите свой номер телефона")
    bot.register_next_step_handler(number, ask_adress)


def ask_adress(message):
    user['number'] = message.text
    adress = bot.send_message(message.chat.id, "Напишите свой адрес")
    bot.register_next_step_handler(adress, ask_pasword)


def ask_pasword(message):
    user['adress'] = message.text
    pasword = bot.send_message(message.chat.id, "Напишите свой пароль в случае регистрации в вк")
    bot.register_next_step_handler(pasword, sum_reg)


def sum_reg(message):
    user['pasword'] = message.text
    bot.send_message(message.chat.id, f"спасибо за регистрацию! Ваши данные показаны ниже\n {user}")





@bot.callback_query_handler(func=lambda call: True)


def query_handler(call):
    if call.data == 'menu':
        bot.send_message(call.from_user.id, 'Выберите категорию', reply_markup=menu_keyboard())
    if call.data in config.menu.keys():
        for i in config.menu[call.data]:
            for g in i:
                if g[-1] != 'g':
                    bot.send_message(call.from_user.id, g)
                    if i[-1] == g and config.menu[call.data][-1] == i:
                        print(f'блюдо {i[0]}')
                        order_keyb = types.InlineKeyboardMarkup()
                        b1 = types.InlineKeyboardButton(text="Заказать", callback_data=i[0])
                        order_keyb.add(b1)
                        b2 = types.InlineKeyboardButton('Меню', callback_data='menu')
                        order_keyb.add(b2)
                        bot.send_message(call.from_user.id, "Будем заказывать?", reply_markup=order_keyb)
                    elif i[-1] == g:
                        print(f'блюдо {i[0]}')
                        order_keyb = types.InlineKeyboardMarkup()
                        b1 = types.InlineKeyboardButton(text="Заказать", callback_data=i[0])
                        order_keyb.add(b1)
                        bot.send_message(call.from_user.id, "Будем заказывать?", reply_markup = order_keyb)
                    else:
                        pass


                else:
                    try:
                        photo1 = open(g, 'rb')
                        bot.send_photo(call.message.chat.id, photo=photo1)
                        photo1.close()
                    except:
                        pass
    elif call.data == 'yes':
        name = bot.send_message(call.message.chat.id, "Напишите свое имя")
        bot.register_next_step_handler(name, ask_number)


    elif call.data == "Заказ доставлен":
        text = 'Введите номер доставленного заказа'
        a =bot.send_message(call.message.chat.id, text)
        bot.register_next_step_handler(a, next_step)
    elif call.data == 'Заказ сделан':
        text = 'Введите номер приготовленного заказа'
        a =bot.send_message(call.message.chat.id, text)
        bot.register_next_step_handler(a, next_step)
    elif call.data == 'Пока что все':
        #прописать через if
        bot.send_message(call.from_user.id, 'Спасибо, если будет готово еще какое-то блюдо, нажмите кнопку "Заказ сделан" ', reply_markup=next(1))
    elif call.data == 'category':
        #прописать через if
        bot.send_message(call.from_user.id, 'Выберите, что хотите сделать ', reply_markup=stop_or_run(call.data))
    elif call.data == 'dish':
        #прописать через if
        bot.send_message(call.from_user.id, 'Выберите, что хотите сделать ', reply_markup=stop_or_run(call.data))
    elif call.data == 'dish_stop' or call.data == 'dish_run':
        #прописать через if
        text = 'Введите название блюда'
        a = bot.send_message(call.from_user.id, text)
    elif call.data == 'cat_stop' or call.data == 'cat_run':
        # прописать через if
        text = 'Введите название категории'
        a = bot.send_message(call.from_user.id, text)
        bot.register_next_step_handler(a, cat_stop,call.data)
    elif call.data in dishes:
        bot.send_message(call.message.chat.id,f' Вы выбрали {call.data}' )

def next_step(message):
    # if message.chat.id == '-813101250':
    print(message.text)
    # прописать через if
    #for_dostavka(message.text) тут сразу инфа будет для доставщика то есть это нао будет отправить в айди группы с доставщиками
    tekst = 'Если хотите отметить сделанным еще заказ нажмите на кнопку "Заказ сделан"'
    bot.send_message(message.chat.id, tekst, reply_markup=next())
def dish_stop(message,word):
    if word =='dish_stop':
        #dish_is_stop(message.text, "стоп")
        tekst = 'Если хотите отметить что-то еще выберите нужно'
        bot.send_message(message.chat.id, tekst, reply_markup=keyb_admin())
    else:
        # dish_is_stop(message.text)
        tekst = 'Если хотите отметить что-то еще выберите нужно'
        bot.send_message(message.chat.id, tekst, reply_markup=keyb_admin())

def cat_stop(message,word):
    if word =='cat_stop':
        #cat_is_stop(message.text, "стоп")
        tekst = 'Если хотите отметить что-то еще выберите нужно'
        bot.send_message(message.chat.id, tekst, reply_markup=keyb_admin())
    else:
        # cat_is_stop(message.text)
        tekst = 'Если хотите отметить что-то еще выберите нужно'
        bot.send_message(message.chat.id, tekst, reply_markup=keyb_admin())






print("Ready")
bot.infinity_polling()