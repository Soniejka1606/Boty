import datetime
import os

import vk_api
from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json


from database import *

# GROUP_ID = '219364665'
# GROUP_TOKEN = 'vk1.a.Udr_3z5uGE0H0VcDsiUrnxXt8YXuiYaQZPdLIYC1YrzbFTxRZvvelbhTEFiB0-0cdRJ21Xy2M31lVbaXR3HWI0AWBQz74S0p8cjDs1A2BM6DGzIcirs90Jw0kyp2sbFuDkecVixcmfEY4FbN01pD7MR6520v-GN5Zfzm8GpP4xbaDPsC7IBlszgiaLxLo65XLAzAAp4Efm-tBI-N4n9mbQ'
# API_VERSION = '5.120'

GROUP_ID = '219364686'
GROUP_TOKEN = 'vk1.a.QTSvYwYIGmfz5_ArnSV2oTR5huKn3q6WMihaJGgqKGHld1VbQDJQBJyJy98spHmmW0DYlpvS9C92A8OnnEVETV1rOggZS31H0Iz_XIVxFnZh69lwJdLn2eZsgJ8u2sdnjTZbgKAC3d9uRqi-0fp_89WuRJTJbU83w31KBONTF21XCzXqEk1QSrOv1Y3347zubaxf9NEa5XHwh24X0eeY8Q'
API_VERSION = '5.120'

# Запускаем бот
vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
vk = vk_session.get_api()
upload = vk_api.VkUpload(vk)
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)

settings2 = dict(one_time=False, inline=True)
def set_comment():
    keyboard = VkKeyboard(**settings2)
    keyboard.add_callback_button('Да', color=VkKeyboardColor.NEGATIVE,
                                 payload={'type': "Оставить коммент"})

    keyboard.add_callback_button('Нет', color=VkKeyboardColor.NEGATIVE, payload={'type': "Не оставить коммент"})


    return keyboard

def comment_after_order(adress):
    vk.messages.send(
        user_id=adress,
        random_id=get_random_id(),
        peer_id=adress,
        message=f"Хотите оставить комментарий?",
        keyboard=set_comment().get_keyboard())

def send_mess(adress,text):
    vk.messages.send(
        user_id=adress,
        random_id=get_random_id(),
        peer_id=adress,
        message=text)