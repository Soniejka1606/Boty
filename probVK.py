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

settings1 = dict(one_time=False, inline=False)
settings2 = dict(one_time=False, inline=True)

admin = '134828772'

"""Все id"""

id_all_dict = {}


def all_id():
    global id_all_dict
    with open("id_user_vk.json", "r", encoding='utf-8') as read_file:
        id_all_dict = json.load(read_file)


all_id()
HI = ["start", "Start", "начать", "Начало", "Начать", "начало", "Бот", "бот", "Старт", "старт", "скидки", "Скидки"]

# Основное меню


menu = menu_main()
print(menu)
cat_list = list(menu.keys())

cat_dish = {}
for k, v in menu.items():
    for i in v:
        if k not in cat_dish.keys():
            cat_dish[k] = [i[1]]
        else:
            cat_dish[k].append(i[1])
dish_opis = {}
for i, v in menu.items():
    for j in v:
        dish_opis[j[1]] = [j[0], j[2], j[3], j[4], j[5]]
print(dish_opis)

""" Клавиатура меню"""


def keyboard_сat(list1, data, inte):
    data = int(data)
    data = data + int(inte)
    keyboard = VkKeyboard(**settings2)
    if data > 0 and data < len(list1) - 1:
        keyboard.add_callback_button(list1[data], color=VkKeyboardColor.PRIMARY,
                                     payload={'type': cat_list[data], "data": str(data)})
        keyboard.add_line()
        keyboard.add_callback_button('Назад', color=VkKeyboardColor.NEGATIVE,
                                     payload={'type': "назад", "data": str(data)})
        keyboard.add_callback_button('Вперед', color=VkKeyboardColor.NEGATIVE,
                                     payload={'type': "вперед", "data": str(data)})
    elif data == 0:
        keyboard.add_callback_button(list1[data], color=VkKeyboardColor.PRIMARY,
                                     payload={'type': cat_list[data], "data": str(data)})
        keyboard.add_line()
        keyboard.add_callback_button('Вперед', color=VkKeyboardColor.NEGATIVE,
                                     payload={'type': "вперед", "data": str(data)})
    elif data == len(list1) - 1:
        keyboard.add_callback_button(list1[data], color=VkKeyboardColor.PRIMARY,
                                     payload={'type': cat_list[data], "data": str(data)})
        keyboard.add_line()
        keyboard.add_callback_button('Назад', color=VkKeyboardColor.NEGATIVE,
                                     payload={'type': "назад", "data": str(data)})

    return keyboard


def keyboard_dish(list1, data, inte, cat_name):
    data = int(data)
    data = data + int(inte)
    keyboard = VkKeyboard(**settings2)
    if len(list1) == 1:
        keyboard.add_callback_button(list1[data], color=VkKeyboardColor.PRIMARY,
                                     payload={'type': list1[data], "data": str(data), "cat": cat_name})
        keyboard.add_line()
        keyboard.add_callback_button('Меню', color=VkKeyboardColor.NEGATIVE, payload={'type': "меню"})
    elif data > 0 and data < len(list1) - 1:
        keyboard.add_callback_button(list1[data], color=VkKeyboardColor.PRIMARY,
                                     payload={'type': list1[data], "data": str(data), "cat": cat_name})
        keyboard.add_line()
        keyboard.add_callback_button('Назад', color=VkKeyboardColor.NEGATIVE,
                                     payload={'type': "назад1", "data": str(data), "cat": cat_name})
        keyboard.add_callback_button('Вперед', color=VkKeyboardColor.NEGATIVE,
                                     payload={'type': "вперед1", "data": str(data), "cat": cat_name})
        keyboard.add_line()
        keyboard.add_callback_button('Меню', color=VkKeyboardColor.NEGATIVE, payload={'type': "меню"})
    elif data == 0:
        keyboard.add_callback_button(list1[data], color=VkKeyboardColor.PRIMARY,
                                     payload={'type': list1[data], "data": str(data), "cat": cat_name})
        keyboard.add_line()
        keyboard.add_callback_button('Вперед', color=VkKeyboardColor.NEGATIVE,
                                     payload={'type': "вперед1", "data": str(data), "cat": cat_name})
        keyboard.add_callback_button('Меню', color=VkKeyboardColor.NEGATIVE, payload={'type': "меню"})
    elif data == len(list1) - 1:
        keyboard.add_callback_button(list1[data], color=VkKeyboardColor.PRIMARY,
                                     payload={'type': list1[data], "data": str(data), "cat": cat_name})
        keyboard.add_line()
        keyboard.add_callback_button('Назад', color=VkKeyboardColor.NEGATIVE,
                                     payload={'type': "назад1", "data": str(data), "cat": cat_name})
        keyboard.add_callback_button('Меню', color=VkKeyboardColor.NEGATIVE, payload={'type': "меню"})
    return keyboard


def keyb_infa(cat_name, name_dish):
    keyboard = VkKeyboard(**settings2)
    keyboard.add_callback_button('Заказать', color=VkKeyboardColor.NEGATIVE,
                                 payload={'type': "Заказать", "name_dish": name_dish})
    keyboard.add_line()
    keyboard.add_callback_button('Меню', color=VkKeyboardColor.NEGATIVE, payload={'type': "меню"})
    keyboard.add_callback_button('Назад в категорию', color=VkKeyboardColor.NEGATIVE,
                                 payload={'type': "Назад в категорию", "data": cat_name})

    return keyboard


def keyb_count(dish_name, data, inte):
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    data = int(data) + int(inte)
    keyboard = VkKeyboard(**settings2)
    if data > 0 and data < len(a) - 1:
        keyboard.add_callback_button(str(a[data]), color=VkKeyboardColor.NEGATIVE,
                                     payload={'type': "кол-во выбрано", "dish": dish_name, "count": str(a[data])})
        keyboard.add_line()
        keyboard.add_callback_button('+', color=VkKeyboardColor.NEGATIVE,
                                     payload={'type': "+", "dish": dish_name, "data": str(data)})
        keyboard.add_callback_button('-', color=VkKeyboardColor.NEGATIVE,
                                     payload={'type': "-", "dish": dish_name, "data": str(data)})
    elif data == 0:
        keyboard.add_callback_button(str(a[data]), color=VkKeyboardColor.NEGATIVE,
                                     payload={'type': "кол-во выбрано", "dish": dish_name, "count": str(a[data])})
        keyboard.add_line()
        keyboard.add_callback_button('+', color=VkKeyboardColor.NEGATIVE,
                                     payload={'type': "+", "dish": dish_name, "data": str(data)})
    elif data == len(a) - 1:
        keyboard.add_callback_button(str(a[data]), color=VkKeyboardColor.NEGATIVE,
                                     payload={'type': "кол-во выбрано", "dish": dish_name, "count": str(a[data])})
        keyboard.add_line()
        keyboard.add_callback_button('-', color=VkKeyboardColor.NEGATIVE,
                                     payload={'type': "-", "dish": dish_name, "data": str(data)})
    return keyboard


def do_order():
    keyboard = VkKeyboard(**settings2)
    keyboard.add_callback_button('Меню', color=VkKeyboardColor.NEGATIVE, payload={'type': "меню"})
    keyboard.add_callback_button('Оформить заказ', color=VkKeyboardColor.NEGATIVE,
                                 payload={'type': "Оформить заказ"})
    keyboard.add_line()
    keyboard.add_callback_button('Отменить заказ', color=VkKeyboardColor.NEGATIVE,
                                 payload={'type': "Отменить заказ"})
    return keyboard


def buy_order():
    keyboard = VkKeyboard(**settings2)
    keyboard.add_callback_button('Подтвердить заказ', color=VkKeyboardColor.NEGATIVE,
                                 payload={'type': "Подтвердить заказ"})
    keyboard.add_callback_button('Отменить заказ', color=VkKeyboardColor.NEGATIVE,
                                 payload={'type': "Отменить заказ"})
    return keyboard

# Основное меню
keyboard_1 = VkKeyboard(**settings1)
keyboard_1.add_button(label='HELP', color=VkKeyboardColor.NEGATIVE, payload={"type": "text"})
keyboard_1.add_line()
keyboard_1.add_button(label='Зарегистрироваться!', color=VkKeyboardColor.PRIMARY, payload={"type": "text"})

keyboard_2 = VkKeyboard(**settings1)
keyboard_2.add_button(label='HELP', color=VkKeyboardColor.NEGATIVE, payload={"type": "text"})
keyboard_2.add_line()
keyboard_2.add_button(label='Начать', color=VkKeyboardColor.PRIMARY, payload={"type": "text"})

# keyb_reg = VkKeyboard(**settings2)
# keyb_reg.add_callback_button(label='Зарегистрироваться!', color=VkKeyboardColor.NEGATIVE, payload={"type": "reg"})
# keyb_reg.add_line()
# keyb_reg.add_callback_button(label='HELP', color=VkKeyboardColor.NEGATIVE, payload={"type": "help"})

# with open(f'orders/{message.from_user.id}.json', 'w', encoding='utf-8') as file:
#     json.dump(order_dish[message.from_user.id], file, ensure_ascii=False)

order_dish = {}

state_list = {}
reg_dict = {}

# Запускаем бот
vk_session = VkApi(token=GROUP_TOKEN, api_version=API_VERSION)
vk = vk_session.get_api()
upload = vk_api.VkUpload(vk)
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)

CALLBACK_TYPES = ('show_snackbar', 'open_link', 'open_app', 'text', 'callback')

reser = ['запустить бота', 'меню', 'заказать', 'запустить бота', 'help', 'Зарегистрироваться!', 'HELP']



def upload_photo(photo):
    response = upload.photo_messages(photo)[0]

    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']

    return f'photo{owner_id}_{photo_id}_{access_key}'


def proverka():
    try:
        orders_list_id = os.listdir('orders')
        for order in orders_list_id:
            with open(f'orders/{order}', 'r', encoding='utf-8') as file:
                data = json.load(file)
            order_dish[int(data['vk_id'])] = data
            if data['state'] == 1:
                text = ''
                for ky, val in data['dishs'].items():
                    text += f'Выбрано блюда - {ky} в количестве {val} шт. \n'
                text += 'Если хотите оформить заказ - нажмите "Оформить заказ",для продолжения - "Меню"'
                vk.messages.send(user_id=134828772,
                                 random_id=get_random_id(),
                                 peer_id=134828772,
                                 message=text,
                                 keyboard=do_order().get_keyboard()
                                 )
            elif data['state'] == 2:
                text = f"Ваш адрес - {data['addres']} \n Добавьте комментарий"
                vk.messages.send(user_id=134828772,
                                 random_id=get_random_id(),
                                 peer_id=134828772,
                                 message=text)
            elif data['state'] == 3:
                text = f"Ваш комментарий добавлен - {data['comment']} \n Подтвердите заказ"
                vk.messages.send(user_id=134828772,
                                 random_id=get_random_id(),
                                 peer_id=134828772,
                                 message=text)
    except:
        pass


proverka()
print('Ready VK')

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.obj.message['text'] != '':
            if event.from_user:
                if event.obj.message['text']:
                    user_id = event.obj.message['from_id']
                    if user_id not in id_all_dict['users']:
                        try:
                            if len(state_list[user_id]) > 0 and 'st3' in state_list[user_id]:
                                if event.obj.message['text'] not in reser:
                                    reg_dict[user_id].setdefault('password', event.obj.message['text'])
                                    id_all_dict['users'].append(user_id)
                                    with open('id_user_vk.json', 'w', encoding='utf-8') as file:
                                        json.dump(id_all_dict, file, ensure_ascii=False)
                                    all_id()
                                    print(reg_dict[user_id])
                                    registration(reg_dict[user_id])
                                    state_list[user_id].clear()
                                    reg_dict[user_id].clear()
                                    vk.messages.send(
                                        user_id=event.obj.message['from_id'],
                                        random_id=get_random_id(),
                                        peer_id=event.obj.message['from_id'],
                                        message=f"Поздравляем вы зарегистрировались",
                                        keyboard=keyboard_2.get_keyboard())
                                else:
                                    vk.messages.send(
                                        user_id=event.obj.message['from_id'],
                                        random_id=get_random_id(),
                                        peer_id=event.obj.message['from_id'],
                                        message=f"Вы некорректно ввели пароль. \n Попробуйте снова")
                            elif len(state_list[user_id]) > 0 and 'st2' in state_list[user_id]:
                                if event.obj.message['text'].isdigit():
                                    reg_dict[user_id].setdefault('phone_number', event.obj.message['text'])
                                    state_list[user_id].append('st3')
                                    vk.messages.send(
                                        user_id=event.obj.message['from_id'],
                                        random_id=get_random_id(),
                                        peer_id=event.obj.message['from_id'],
                                        message=f"Ваш номер телефона {event.obj.message['text']}. \n Введите пароль")
                                else:
                                    vk.messages.send(
                                        user_id=event.obj.message['from_id'],
                                        random_id=get_random_id(),
                                        peer_id=event.obj.message['from_id'],
                                        message=f"Вы некорректно ввели номер телефона. \n Попробуйте снова")
                            elif len(state_list[user_id]) > 0 and 'st1' in state_list[user_id]:
                                if event.obj.message['text'] not in reser:
                                    reg_dict[user_id] = {'name': event.obj.message['text']}
                                    reg_dict[user_id].setdefault('vk_id', user_id)
                                    state_list[user_id].append('st2')
                                    vk.messages.send(
                                        user_id=event.obj.message['from_id'],
                                        random_id=get_random_id(),
                                        peer_id=event.obj.message['from_id'],
                                        message=f"Ваш логин {event.obj.message['text']}\n Введите номер телефона")
                                else:
                                    vk.messages.send(
                                        user_id=event.obj.message['from_id'],
                                        random_id=get_random_id(),
                                        peer_id=event.obj.message['from_id'],
                                        message=f"Вы некорректно ввели логин. \n Попробуйте снова")
                        except:
                            if event.obj.message['text'] == 'Зарегистрироваться!':
                                vk.messages.send(
                                    user_id=event.obj.message['from_id'],
                                    random_id=get_random_id(),
                                    peer_id=event.obj.message['from_id'],
                                    message=f"Введите логин",
                                    keyboard=keyboard_1.get_keyboard())
                                state_list[user_id] = ['st1']
                            elif event.obj.message['text'] == 'HELP':
                                vk.messages.send(
                                    user_id=event.obj.message['from_id'],
                                    random_id=get_random_id(),
                                    peer_id=event.obj.message['from_id'],
                                    message='Краткий текст помощи')
                            elif event.obj.message['text']:
                                print(event.obj)
                                vk.messages.send(
                                    user_id=event.obj.message['from_id'],
                                    random_id=get_random_id(),
                                    peer_id=event.obj.message['from_id'],
                                    message='Здравствуйте вам надо зарегистрироваться',
                                    keyboard=keyboard_1.get_keyboard())
                    if user_id in order_dish.keys():
                        if order_dish[user_id]['state'] == 2:
                            order_dish[user_id]['address'] = event.obj.message["text"]
                            with open(f'orders/{user_id}vk.json', 'w', encoding='utf-8') as file:
                                json.dump(order_dish[user_id], file, ensure_ascii=False)
                            order_dish[user_id]['state'] = 3
                            vk.messages.send(
                                user_id=event.obj.message['from_id'],
                                random_id=get_random_id(),
                                peer_id=event.obj.message['from_id'],
                                message=f'Ваш адрес - {event.obj.message["text"]} \n Добавьте комментарий.'
                                )
                        elif order_dish[user_id]['state'] == 3:
                            order_dish[user_id]['comment'] = event.obj.message["text"]
                            with open(f'orders/{user_id}vk.json', 'w', encoding='utf-8') as file:
                                json.dump(order_dish[user_id], file, ensure_ascii=False)
                            order_dish[user_id]['state'] = 4
                            text_ = time_costs(order_dish[user_id]['dishs'])
                            vk.messages.send(
                                user_id=event.obj.message['from_id'],
                                random_id=get_random_id(),
                                peer_id=event.obj.message['from_id'],
                                message=text_,
                                keyboard=buy_order().get_keyboard()
                                )

                    elif event.obj.message['text'] in HI:
                        vk.messages.send(
                            user_id=event.obj.message['from_id'],
                            random_id=get_random_id(),
                            peer_id=event.obj.message['from_id'],
                            message=f"Выбирайте",
                            keyboard=keyboard_сat(cat_list, 0, '0').get_keyboard(), )
                    elif event.obj.message['text'] == 'HELP':
                        vk.messages.send(
                            user_id=event.obj.message['from_id'],
                            random_id=get_random_id(),
                            peer_id=event.obj.message['from_id'],
                            message='Краткий текст помощи')
                    try:
                        if len(state_list[user_id]) > 0 and state_list[user_id] == ['com']:
                            if event.obj.message['text'] not in reser:
                                state_list[user_id].clear()
                                from for_import import new_com
                                new_com(event.obj.message['text'])
                                vk.messages.send(
                                    user_id=event.obj.message['from_id'],
                                    random_id=get_random_id(),
                                    peer_id=event.obj.message['from_id'],
                                    message=f"Спасибо за ваш отзыв")
                        else:
                            vk.messages.send(
                                user_id=event.obj.message['from_id'],
                                random_id=get_random_id(),
                                peer_id=event.obj.message['from_id'],
                                message=f"У вас не было заказа")
                    except:
                        pass
    elif event.type == VkBotEventType.MESSAGE_EVENT:
        if event.object.payload.get('type') in CALLBACK_TYPES:
            vk.messages.sendMessageEventAnswer(
                event_id=event.object.event_id,
                user_id=event.object.user_id,
                peer_id=event.object.peer_id,
                event_data=json.dumps(event.object.payload))
        elif event.object.payload.get('type') == 'help':
            last_id = vk.messages.edit(
                peer_id=event.obj.peer_id,
                message=f"Справочная информация по регистрации",
                conversation_message_id=event.obj.conversation_message_id)
            # Клавиатура
        elif event.object.payload.get('type') == "назад":
            kb = keyboard_сat(cat_list, event.object.payload.get('data'), '-1')
            last_id = vk.messages.edit(
                peer_id=event.obj.peer_id,
                message='Выбирай категорию',
                conversation_message_id=event.obj.conversation_message_id,
                keyboard=kb.get_keyboard())


        elif event.object.payload.get('type') == "вперед":
            # print(event.object.payload.get('data'))
            kb = keyboard_сat(cat_list, event.object.payload.get('data'), '1')
            last_id = vk.messages.edit(
                peer_id=event.obj.peer_id,
                message='Выбирай категорию',
                conversation_message_id=event.obj.conversation_message_id,
                keyboard=kb.get_keyboard()
            )
        elif event.object.payload.get('type') in cat_list:
            list1 = cat_dish[event.object.payload.get('type')]
            cat_name = event.object.payload.get('type')
            kb = keyboard_dish(list1, 0, '0', cat_name)
            last_id = vk.messages.edit(
                peer_id=event.obj.peer_id,
                message='Выбирай блюдо',
                conversation_message_id=event.obj.conversation_message_id,
                keyboard=kb.get_keyboard()
            )
        elif event.object.payload.get('type') == "назад1":
            list1 = cat_dish[event.object.payload.get('cat')]
            kb = keyboard_dish(list1, event.object.payload.get('data'), '-1', event.object.payload.get('cat'))
            last_id = vk.messages.edit(
                peer_id=event.obj.peer_id,
                message='Выбирай блюдо',
                conversation_message_id=event.obj.conversation_message_id,
                keyboard=kb.get_keyboard())


        elif event.object.payload.get('type') == "вперед1":
            list1 = cat_dish[event.object.payload.get('cat')]
            kb = keyboard_dish(list1, event.object.payload.get('data'), '1', event.object.payload.get('cat'))
            last_id = vk.messages.edit(
                peer_id=event.obj.peer_id,
                message='Выбирай блюдо',
                conversation_message_id=event.obj.conversation_message_id,
                keyboard=kb.get_keyboard()
            )
        elif event.object.payload.get('type') == "меню":
            last_id = vk.messages.edit(
                peer_id=event.obj.peer_id,
                message='Выбирай категорию',
                conversation_message_id=event.obj.conversation_message_id,
                keyboard=keyboard_сat(cat_list, 0, '0').get_keyboard()
            )
        elif event.object.payload.get('type') in dish_opis.keys():
            a = dish_opis[event.object.payload.get('type')]

            text = f"{event.object.payload.get('type')} \nЦена:{a[2]} руб.\nСостав: {a[3]}\nремя приготовления:{a[4]}"

            last_id = vk.messages.edit(
                peer_id=event.obj.peer_id,
                attachment=upload_photo(f'img/{a[1]}'),
                message=text,
                conversation_message_id=event.obj.conversation_message_id,
                keyboard=keyb_infa(event.object.payload.get('cat'), event.object.payload.get('type')).get_keyboard()
            )
        elif event.object.payload.get('type') == "Назад в категорию":
            list1 = cat_dish[event.object.payload.get('data')]
            cat_name = event.object.payload.get('data')
            kb = keyboard_dish(list1, 0, '0', cat_name)

            last_id = vk.messages.edit(
                peer_id=event.obj.peer_id,
                message='Выбирай блюдо',
                conversation_message_id=event.obj.conversation_message_id,
                keyboard=kb.get_keyboard()
            )

        elif event.object.payload.get('type') == "Заказать":
            kb = keyb_count(event.object.payload.get('name_dish'), '0', '0')

            last_id = vk.messages.edit(
                peer_id=event.obj.peer_id,
                message='Выберите количество',
                conversation_message_id=event.obj.conversation_message_id,
                keyboard=kb.get_keyboard()
            )
        elif event.object.payload.get('type') == "+":

            kb = keyb_count(event.object.payload.get('dish'), event.object.payload.get('data'), '1')
            last_id = vk.messages.edit(
                peer_id=event.obj.peer_id,
                message='Выберите количество',
                conversation_message_id=event.obj.conversation_message_id,
                keyboard=kb.get_keyboard()
            )
        elif event.object.payload.get('type') == "-":
            kb = keyb_count(event.object.payload.get('dish'), event.object.payload.get('data'), '-1')
            last_id = vk.messages.edit(
                peer_id=event.obj.peer_id,
                message='Выберите количество',
                conversation_message_id=event.obj.conversation_message_id,
                keyboard=kb.get_keyboard()
            )
        elif event.object.payload.get('type') == "кол-во выбрано":
            dish_ = event.object.payload.get("dish")
            count_dish = int(event.object.payload.get("count"))
            from_id_vk = event.obj.peer_id
            if from_id_vk not in order_dish:
                order_dish[from_id_vk] = {}
                order_dish[from_id_vk].setdefault('vk_id', from_id_vk)
                order_dish[from_id_vk].setdefault('dishs', {dish_: count_dish})

            else:
                order_dish[from_id_vk]['dishs'].setdefault(dish_, count_dish)
            text = ''
            for k, v in order_dish[from_id_vk].items():
                if k == 'dishs':
                    for ky, val in v.items():
                        text += f'Выбрано блюда - {ky} в количестве {val} шт. \n'
            text += 'Если хотите оформить заказ - нажмите "Оформить заказ",для продолжения - "Меню"'
            order_dish[from_id_vk]['state'] = 1
            with open(f'orders/{from_id_vk}vk.json', 'w', encoding='utf-8') as file:
                json.dump(order_dish[from_id_vk], file, ensure_ascii=False)
            last_id = vk.messages.edit(
                peer_id=event.obj.peer_id,
                message=text,
                conversation_message_id=event.obj.conversation_message_id,
                keyboard=do_order().get_keyboard()
            )
        elif event.object.payload.get('type') == "Отменить заказ":
            try:
                order_dish.pop(event.obj.peer_id)
                os.remove(f'orders/{event.obj.peer_id}vk.json')
                last_id = vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message='Ваш заказ отменен\n Если хотите что-то еще выбирайте',
                    conversation_message_id=event.obj.conversation_message_id,
                    keyboard=keyboard_сat(cat_list, 0, '0').get_keyboard())
            except:
                last_id = vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message='У Вас нет заказа',
                    conversation_message_id=event.obj.conversation_message_id)

        elif event.object.payload.get('type') == "Оформить заказ":
            try:
                order_dish[event.obj.peer_id]['state'] = 2
                last_id = vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message='Введите адрес',
                    conversation_message_id=event.obj.conversation_message_id)
            except:
                last_id = vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message='У Вас нет заказа',
                    conversation_message_id=event.obj.conversation_message_id)
        elif event.object.payload.get('type') == "Подтвердить заказ":
            print("работает подтвердить заказ")
            try:
                ordering(order_dish[event.obj.peer_id]['dishs'], order_dish[event.obj.peer_id])
                order_dish[event.obj.peer_id].pop('state')
                os.remove(f'orders/{event.obj.peer_id}vk.json')
                cooks = for_cook()
                date_order = datetime.date.today()
                try:
                    os.mkdir(f'orders_add/{date_order}')
                except:
                    pass
                for cook in cooks:
                    from for_import import otpravka
                    otpravka(cook)
                    with open(f'orders_add/{date_order}/{event.obj.peer_id}_{cook.split(":")[0]}vk.json', 'w',
                              encoding='utf-8') as file:
                        json.dump(cook, file, ensure_ascii=False)
                order_dish.pop(event.obj.peer_id)
                last_id = vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message='Ваш заказ принят',
                    conversation_message_id=event.obj.conversation_message_id)
            except:
                last_id = vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message='У Вас нет заказа',
                    conversation_message_id=event.obj.conversation_message_id)

        elif event.object.payload.get('type') == "Не оставить коммент":
                last_id = vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message='Спасибо, что воспользовались нашим приложением!!!!!!!',
                    conversation_message_id=event.obj.conversation_message_id,
                    keyboard=keyboard_сat(cat_list, 0, '0').get_keyboard())
        elif event.object.payload.get('type') == "Оставить коммент":
                state_list[event.obj.peer_id] = ['com']

                last_id = vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message='Введите комментарий',
                    conversation_message_id=event.obj.conversation_message_id)
