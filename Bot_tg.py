import json

import config

token = '6236696473:AAH_OGgS5jBhtDC7ZRA8lJwXHHZkQCfxZwg'

import time
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telebot.types import InputMediaPhoto
from config import *

bot = telebot.TeleBot(Token)
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
reg = dict()

"""Кнопки"""
"""Для зарегистрированных пользователей"""
keyb_start_users = types.InlineKeyboardMarkup()
keyb_start_users.add(types.InlineKeyboardButton('Меню', callback_data='menu'))
"""Для администрации"""
keyb_start_admin = types.InlineKeyboardMarkup()
keyb_start_admin.add(*(types.InlineKeyboardButton('Меню', callback_data='menu'),
                       types.InlineKeyboardButton('Рабочая зона', callback_data='work')))

"""Для регистрации"""
keyb_reg = types.ReplyKeyboardMarkup()
keyb_reg.add(types.KeyboardButton('Зарегистрироваться'))

"""Для меню"""
keyb_menu = types.InlineKeyboardMarkup()
keyb_menu.add(*(types.InlineKeyboardButton(a, callback_data='m' + a) for a in config.menu.keys()))

"""Для блюд"""
def dishs(category, massage_id):
    for dish in config.menu[category]:
        for info in dish:
            if info == dish[0]:
                bot.send_message(massage_id, f'Название - {info}')
            elif info == dish[1]:
                bot.send_message(massage_id, f'Стоймость - {info}')
            elif info == dish[2]:
                photo1 = open(info, 'rb')
                bot.send_photo(massage_id, photo=photo1)
            elif info == dish[3]:
                bot.send_message(massage_id, f'Состав - {info}')
""""""


# keyd.add(*(types.KeyboardButton(a[0]) for a in list_of_lists[1:]))


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        if message.chat.id not in id_all:
            bot.send_message(message.chat.id, 'hellow')
            bot.send_message(message.chat.id, 'Вам надо зарегистрироваться', reply_markup=keyb_reg)
        if message.chat.id in id_all_dict['users']:
            bot.send_message(message.chat.id, 'hellow', reply_markup=keyb_start_users)
        if message.chat.id in id_all_dict['super_admin'] or message.chat.id in id_all_dict['admin']:
            bot.send_message(message.chat.id, 'hellow', reply_markup=keyb_start_admin)
    if message.text == 'Зарегистрироваться':
        bot.send_message(message.chat.id, 'Регистрация')
        mesg = bot.send_message(message.chat.id, 'Введите логин')
        bot.register_next_step_handler(mesg, login)


def login(message):
    bot.send_message(message.chat.id, "ваш логин - " + message.text)
    reg.setdefault(message.chat.id, dict())
    reg[message.chat.id].setdefault('login', message.text)
    mesg = bot.send_message(message.chat.id, 'Введите телефон')
    bot.register_next_step_handler(mesg, phone)


def phone(message):
    if message.text.isdigit():
        bot.send_message(message.chat.id, "ваш телефон - " + message.text)
        reg[message.chat.id].setdefault('phone', message.text)
        mesg = bot.send_message(message.chat.id, 'Введите пароль мин. 6 символов')
        bot.register_next_step_handler(mesg, password)


def password(message):
    if len(message.text) < 6:
        bot.send_message(message.chat.id, "мало символов")
        mesg = bot.send_message(message.chat.id, 'Введите пароль мин. 6 символов')
        bot.register_next_step_handler(mesg, password)
    else:
        bot.send_message(message.chat.id, "ваш пароль - " + message.text)
        reg[message.chat.id].setdefault('password', message.text)
        id_all_dict['users'].append(message.chat.id)
        with open('id_user.json', 'w', encoding='utf-8') as file:
            json.dump(id_all_dict, file, ensure_ascii=False)
        all_id()
        reg = {}
        bot.send_message(message.chat.id, "Вы успешно зарегистрировались")
        bot.send_message(message.chat.id, "Для начала заказа нажмите меню", reply_markup=keyb_start_users)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'menu':
        bot.send_message(call.from_user.id, 'Выберите категорию', reply_markup=keyb_menu)
    elif call.data[0] == 'm':
        massage_id = call.from_user.id
        dishs(call.data[1:], massage_id)





print("Ready")
bot.infinity_polling()
