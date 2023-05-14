import config

token = '6236696473:AAH_OGgS5jBhtDC7ZRA8lJwXHHZkQCfxZwg'

import time
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telebot.types import InputMediaPhoto
from config import *

bot = telebot.TeleBot(Token)

keyb_start = types.InlineKeyboardMarkup()
keyb_start.add(*(types.InlineKeyboardButton('Меню', callback_data='menu'),
                 types.InlineKeyboardButton('Рабочая зона', callback_data='work')))

keyb_menu = types.InlineKeyboardMarkup()
k


# keyd.add(*(types.KeyboardButton(a[0]) for a in list_of_lists[1:]))


@bot.message_handler(content_types=['text'])
def start(message):
    if message.chat.id in config.super_admin:
        if message.text == '/start':
            # if message.chat.id in config.users:
            bot.send_message(message.chat.id, 'hellow', reply_markup=keyb_start)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'menu':
        bot.send_message(call.from_user.id, 'hellow', reply_markup=keyb_start)


# @bot.message_handler(content_types=['text'])
# def stat(message):
#     if message.text == '/stat':
#         id_message = message.chat.id
#         statistic_ = len(stat_dict['user_finish']) / len(stat_dict['all']) * 100
#         bot.send_message(id_message, f'Количество пользователей дошедших до финиша {statistic_}%')
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def query_handler(call):
#     print(call)
#     bot.answer_callback_query(callback_query_id=call.id, )
#     id_message = call.from_user.id
#     flag = call.data[0]
#     num_ = call.data[1:]
#     print('работает')
#     if flag == 'a':
#         if list_of_lists[int(num_)][5] == '':
#             index(list_of_lists, num_, id_message)
#         else:
#             quiz(list_of_lists, num_, id_message)
#     elif flag == 'y':
#         bot.send_message(id_message, list_of_lists[int(num_)][7])
#         keyd_ = types.InlineKeyboardMarkup()
#         keyd_.add(types.InlineKeyboardButton('*', callback_data='a' + str(int(num_) + 1)))
#         bot.send_message(id_message, f'{list_of_lists[int(num_)][11]}', reply_markup=keyd_)
#     elif flag == 'f':
#         bot.send_message(id_message, list_of_lists[int(num_)][8])
#         keyd_ = types.InlineKeyboardMarkup()
#         keyd_.add(types.InlineKeyboardButton('*', callback_data='a' + str(int(num_) + 1)))
#         bot.send_message(id_message, f'{list_of_lists[int(num_)][11]}', reply_markup=keyd_)
#     else:
#         pass


print("Ready")
bot.infinity_polling()
