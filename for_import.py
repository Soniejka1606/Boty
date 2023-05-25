import json
import os
import datetime
import time
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import *

bot = telebot.TeleBot('6236696473:AAH_OGgS5jBhtDC7ZRA8lJwXHHZkQCfxZwg')
def otpravka (cook):
    bot.send_message(-813101250, cook)


def new_com(text):
    keybo = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(text="Принять комментарий", callback_data='GoodComment')
    keybo.add(b1)
    b2 = types.InlineKeyboardButton(text="Отклонить комментарий", callback_data='BadComment')
    keybo.add(b2)

    com = text
    bot.send_message(-891527106, com, reply_markup=keybo)

