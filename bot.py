import telebot
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, ReplyKeyboardRemove, CallbackQuery
from info import Info, token
from datasave import save_data, load_data
import random

bot = telebot.TeleBot("6047624895:AAGUBcu4kbuBkMaRl2MM54hsb3YHfteZqyM")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, Info['commands']['start'])


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, Info['commands']['help'])


@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, Info['commands']['info'])


@bot.message_handler(commands=['quest'])
def quest(message):
    inlinemarkup = InlineKeyboardMarkup(row_width=2)
    inlinemarkup.add(InlineKeyboardButton('Да', callback_data='Да'),
                     InlineKeyboardButton('Неа', callback_data='Нет'))
    bot.send_message(message.chat.id, Info['commands']['quest'], reply_markup=inlinemarkup)
    user_progress = {}
    try:
        if user_progress[str(message.chat.id)] in user_progress:
            exit()
    except KeyError:
        user_progress.setdefault(message.chat.id, {

            "progres": 1,  # прогресс по локациям
            "hp": 100,  # здоровье персонажа
            "damage": 10,  # урон наносимый персонажем
            'dc': 10,  # death chance он же шанс смерти
            "life": 1,  # кол-во жизней, если больше 1 то можно возродится на локации а не начинать заново
            "weapon": "Нет",  #
            "jewelery": "Нет",  #
        })
        save_data(user_progress, 'data.json')


@bot.callback_query_handler(func=lambda call: call.data == "Да")
def return1(call):
    with open('data.json') as f:
        user_progress = json.load(f)
    if user_progress[str(call.message.chat.id)]['progres'] == 1:
        bot.answer_callback_query(call.id, "Замечательно")
        bot.send_message(call.message.chat.id, "Отлично начинаю квестирование")
        bot.send_message(call.message.chat.id, f"Вот название первой локации: {Info['stages'][1]['name']}"
                                               f"И её описание: {Info['stages'][1]['description']}")
        action = InlineKeyboardMarkup(row_width=3)
        action.add(InlineKeyboardButton(1, callback_data="выбор1.1"),
                   InlineKeyboardButton(2, callback_data="выбор1.2"),
                   InlineKeyboardButton(3, callback_data="выбор1.3"))
        bot.send_message(call.message.chat.id, f"Ваши действия?\n"
                                               f"1: {Info['stages'][1]['choice_1']}\n"
                                               f"2: {Info['stages'][1]['choice_2']}\n"
                                               f"3: {Info['stages'][1]['choice_3']}",
                         reply_markup=action)
    elif user_progress[str(call.message.chat.id)]['progres'] == 2:
        bot.send_message(call.message.chat.id,
                         "Вы выбрались из первой локации и перед вами предстает выбор: куда идти?")
        bot.send_message(call.message.chat.id, f"1)Имя: {Info['stages'][2][1]['name']}\n"
                                               f"Описание:{Info['stages'][2][1]['description']}")
        bot.send_message(call.message.chat.id, f"2)Имя: {Info['stages'][2][2]['name']}\n"
                                               f"Описание:{Info['stages'][2][2]['description']}")
        bot.send_message(call.message.chat.id, f"3)Имя: {Info['stages'][2][3]['name']}\n"
                                               f"Описание:{Info['stages'][2][3]['description']}")
        loc = InlineKeyboardMarkup(row_width=1)
        loc.add(InlineKeyboardButton("Тропа обречённых", callback_data="loc2.1"),
                InlineKeyboardButton("Ядовитые сточные канавы", callback_data="loc2.2"),
                InlineKeyboardButton("Предместья замка", callback_data="loc2.3"))
        bot.send_message(call.message.chat.id, f"Так куда идем?", reply_markup=loc)
    elif user_progress[str(call.message.chat.id)]['progres'] == 3:
        bot.send_message(call.message.chat.id,
                         "Вы выбрались из второй  локации и перед вами предстает выбор: куда идти?")
        bot.send_message(call.message.chat.id, f"1)Имя: {Info['stages'][3][1]['name']}\n"
                                               f"Описание:{Info['stages'][3][1]['description']}")
        bot.send_message(call.message.chat.id, f"2)Имя: {Info['stages'][3][2]['name']}\n"
                                               f"Описание:{Info['stages'][3][2]['description']}")
        loc = InlineKeyboardMarkup(row_width=1)
        loc.add(InlineKeyboardButton("Тюремные башни", callback_data="loc3.1"),
                InlineKeyboardButton("Древние сточные канавы", callback_data="loc3.2"))
        bot.send_message(call.message.chat.id, f"Так куда идем?", reply_markup=loc)
    elif user_progress[str(call.message.chat.id)]['progres'] == 4:
        bot.send_message(call.message.chat.id, f"Поздравляю вы дошли до финальной локации: {Info['stages'][4]['name']}"
                                               f"описание локации: {Info['stages'][4]['description']}")
        bot.send_message(call.message.chat.id,
                         "На финальной локациии вас ждет битва с боссом если у вас достаточно характеристик вы победите"
                         "так же у вас есть шанс умереть который не зависит от характеристик")
        if user_progress[str(call.message.chat.id)]['hp'] >= 60 and user_progress[str(call.message.chat.id)][
            'damage'] >= 10:
            death = random.randint(1, 100)
            if death <= user_progress[str(call.message.chat.id)]['dc']:
                bot.send_message(call.message.chat.id, "вы умерли от случайности так что вам не повезло")
                user_progress[str(call.message.chat.id)]['progres'] = 0
                save_data(user_progress, 'data.json')
            else:
                bot.send_message(call.message.chat.id, "Поздравляю вас вы победили финального босса и прошли квест")
                user_progress[str(call.message.chat.id)]['progres'] = 0
                save_data(user_progress, 'data.json')
        elif user_progress[str(call.message.chat.id)]['hp'] < 60:
            bot.send_message(call.message.chat.id, "вы умерли из-за недостатка здоровья")
            user_progress[str(call.message.chat.id)]['progres'] = 0
            save_data(user_progress, 'data.json')
        elif user_progress[str(call.message.chat.id)]['damage'] < 10:
            bot.send_message(call.message.chat.id, "вы умерли из-за недостатка урона")
            user_progress[str(call.message.chat.id)]['progres'] = 0
            save_data(user_progress, 'data.json')


@bot.callback_query_handler(func=lambda call: call.data == 'Да')
def questing(call):  # начало квеста
    if call.data == "Да":
        with open('data.json') as f:
            user_progress = json.load(f)
        if user_progress[str(call.message.chat.id)]['progres'] == 1:
            bot.answer_callback_query(call.id, "Замечательно")
            bot.send_message(call.message.chat.id, "Отлично начинаю квестирование")
            bot.send_message(call.message.chat.id, f"Вот название первой локации: {Info['stages'][1]['name']}"
                                                   f"И её описание: {Info['stages'][1]['description']}")
            action = InlineKeyboardMarkup(row_width=3)
            action.add(InlineKeyboardButton(1, callback_data="выбор1.1"),
                       InlineKeyboardButton(2, callback_data="выбор1.2"),
                       InlineKeyboardButton(3, callback_data="выбор1.3"))
            bot.send_message(call.message.chat.id, f"Ваши действия?\n"
                                                   f"1: {Info['stages'][1]['choice_1']}\n"
                                                   f"2: {Info['stages'][1]['choice_2']}\n"
                                                   f"3: {Info['stages'][1]['choice_3']}",
                             reply_markup=action)


@bot.callback_query_handler(func=lambda call: call.data == 'loc2.1' or call.data == 'loc2.2' or call.data == 'loc2.3')
def locvibor(call):  # последствия выбора 2 локации и опции выбора на второй локации
    with open('data.json') as f:
        user_progress = json.load(f)
    if user_progress[str(call.message.chat.id)]['progres'] == 2:
        if call.data == "loc2.1":
            bot.answer_callback_query(call.id, "Хорошо")
            bot.send_message(call.message.chat.id, "Понял, передвигаю персонажа")
            action = InlineKeyboardMarkup(row_width=3)
            action.add(InlineKeyboardButton(1, callback_data="выбор2.1"),
                       InlineKeyboardButton(2, callback_data="выбор2.2"),
                       InlineKeyboardButton(3, callback_data="выбор2.3"))
            bot.send_message(call.message.chat.id, f"Вы пришли на выбранную локацию, ваши действия?\n"
                                                   f"1: {Info['stages'][2][1]['choice_1']}\n"
                                                   f"2: {Info['stages'][2][1]['choice_2']}\n"
                                                   f"3: {Info['stages'][2][1]['choice_3']}",
                             reply_markup=action)
        elif call.data == "loc2.2":
            bot.answer_callback_query(call.id, "Хорошо")
            bot.send_message(call.message.chat.id, "Понял, передвигаю персонажа")
            action = InlineKeyboardMarkup(row_width=3)
            action.add(InlineKeyboardButton(1, callback_data="выбор2.1"),
                       InlineKeyboardButton(2, callback_data="выбор2.2"),
                       InlineKeyboardButton(3, callback_data="выбор2.3"))
            bot.send_message(call.message.chat.id, f"Вы пришли на выбранную локацию, ваши действия?\n"
                                                   f"1: {Info['stages'][2][2]['choice_1']}\n"
                                                   f"2: {Info['stages'][2][2]['choice_2']}\n"
                                                   f"3: {Info['stages'][2][2]['choice_3']}",
                             reply_markup=action)
        elif call.data == "loc2.3":
            bot.answer_callback_query(call.id, "Хорошо")
            bot.send_message(call.message.chat.id, "Понял, передвигаю персонажа")
            action = InlineKeyboardMarkup(row_width=3)
            action.add(InlineKeyboardButton(1, callback_data="выбор2.1"),
                       InlineKeyboardButton(2, callback_data="выбор2.2"),
                       InlineKeyboardButton(3, callback_data="выбор2.3"))
            bot.send_message(call.message.chat.id, f"Вы пришли на выбранную локацию, ваши действия?\n"
                                                   f"1: {Info['stages'][2][3]['choice_1']}\n"
                                                   f"2: {Info['stages'][2][3]['choice_2']}\n"
                                                   f"3: {Info['stages'][2][3]['choice_3']}",
                             reply_markup=action)


@bot.callback_query_handler(
    func=lambda call: call.data == "выбор3.1" or call.data == "выбор3.2" or call.data == "выбор3.3")
def ending(call):  # последствия выбора действий на 3 локе и конец квеста(принудительный к сожалению)
    with open('data.json') as f:
        user_progress = json.load(f)
    if user_progress[str(call.message.chat.id)]['progres'] == 3:
        if call.data == "выбор3.1":
            bot.send_message(call.message.chat.id, "быстро проходя по локации вы полуили 20 ед урона")
            user_progress[str(call.message.chat.id)]['hp'] -= 20
            bot.send_message(call.message.chat.id,
                             f"ваше текущее здоровье равно: {user_progress[str(call.message.chat.id)]['hp']}")
            user_progress[str(call.message.chat.id)]['progres'] += 1
            save_data(user_progress, 'data.json')
        elif call.data == "выбор3.2":
            bot.send_message(call.message.chat.id, "вы просто прошли локацию не получая урона "
                                                   f"ваше текущее здоровье равно: {user_progress[str(call.message.chat.id)]['hp']}")
            user_progress[str(call.message.chat.id)]['progres'] += 1
            save_data(user_progress, 'data.json')
        elif call.data == "выбор3.3":
            bot.send_message(call.message.chat.id, "исследуя локацию вы получили 10 ед урона,"
                                                   " но нашли свиток повышающий здоровье на 10 так что вышли в 0"
                                                   f"ваше текущее здоровье равно: {user_progress[str(call.message.chat.id)]['hp']}")
            user_progress[str(call.message.chat.id)]['progres'] += 1
            save_data(user_progress, 'data.json')
    if user_progress[str(call.message.chat.id)]['progres'] == 4:
        bot.send_message(call.message.chat.id, f"Поздравляю вы дошли до финальной локации: {Info['stages'][4]['name']}"
                                               f"описание локации: {Info['stages'][4]['description']}")
        bot.send_message(call.message.chat.id,
                         "На финальной локациии вас ждет битва с боссом если у вас достаточно характеристик вы победите"
                         "так же у вас есть шанс умереть который не зависит от характеристик")
        if user_progress[str(call.message.chat.id)]['hp'] >= 60 and user_progress[str(call.message.chat.id)][
            'damage'] >= 10:
            death = random.randint(1, 100)
            if death <= user_progress[str(call.message.chat.id)]['dc']:
                bot.send_message(call.message.chat.id, "вы умерли от случайности так что вам не повезло")
                user_progress[str(call.message.chat.id)]['progres'] = 0
            else:
                bot.send_message(call.message.chat.id, "Поздравляю вас вы победили финального босса и прошли квест")
        elif user_progress[str(call.message.chat.id)]['hp'] < 60:
            bot.send_message(call.message.chat.id, "вы умерли из-за недостатка здоровья")
        elif user_progress[str(call.message.chat.id)]['damage'] < 10:
            bot.send_message(call.message.chat.id, "вы умерли из-за недостатка урона")


@bot.callback_query_handler(
    func=lambda call: call.data == "выбор2.1" or call.data == "выбор2.2" or call.data == "выбор2.3")
def loc3(call):  # последствия выбора действия на второй локации и выбор 3 локации
    with open('data.json') as f:
        user_progress = json.load(f)
    if user_progress[str(call.message.chat.id)]['progres'] == 2:
        if call.data == "выбор2.1":
            bot.send_message(call.message.chat.id,
                             'Пока вы искали секреты на вас напали монстры и вы получили 10 ед. урона'
                             'но вы нашли новое оружие: Кровавы меч ')
            user_progress[str(call.message.chat.id)]['weapon'] = "Кровавый меч"
            user_progress[str(call.message.chat.id)]['damage'] += 15
            user_progress[str(call.message.chat.id)]['hp'] -= 10
            user_progress[str(call.message.chat.id)]['progres'] += 1
            bot.send_message(call.message.chat.id,
                             f'Ваше текущее здоровье : {user_progress[str(call.message.chat.id)]["hp"]}')
            save_data(user_progress, 'data.json')
        elif call.data == "выбор2.2":
            bot.send_message(call.message.chat.id,
                             'Пока вы исследовали локацию на вас напали монстры и вы получили 5 ед. урона'
                             'но вы нашли новое кольцо: Кольцо с сапфиром ')
            user_progress[str(call.message.chat.id)]['jewelery'] = "Кольцо с сапфиром"
            user_progress[str(call.message.chat.id)]['hp'] -= 5
            user_progress[str(call.message.chat.id)]['dc'] -= 1
            user_progress[str(call.message.chat.id)]['progres'] += 1
            bot.send_message(call.message.chat.id,
                             f'Ваше текущее здоровье : {user_progress[str(call.message.chat.id)]["hp"]}')
            save_data(user_progress, 'data.json')
        elif call.data == "выбор2.3":
            bot.send_message(call.message.chat.id,
                             'Пока вы бились с монстрами  вы получили 10 ед. урона'
                             'но вы нашли свиток повышающий здоровье на 20 ')
            user_progress[str(call.message.chat.id)]['hp'] += 10
            user_progress[str(call.message.chat.id)]['progres'] += 1
            bot.send_message(call.message.chat.id,
                             f'Ваше текущее здоровье : {user_progress[str(call.message.chat.id)]["hp"]}')
            save_data(user_progress, 'data.json')
        if user_progress[str(call.message.chat.id)]['progres'] == 3:
            bot.send_message(call.message.chat.id,
                             "Вы выбрались из второй  локации и перед вами предстает выбор: куда идти?")
            bot.send_message(call.message.chat.id, f"1)Имя: {Info['stages'][3][1]['name']}\n"
                                                   f"Описание:{Info['stages'][3][1]['description']}")
            bot.send_message(call.message.chat.id, f"2)Имя: {Info['stages'][3][2]['name']}\n"
                                                   f"Описание:{Info['stages'][3][2]['description']}")
            loc = InlineKeyboardMarkup(row_width=1)
            loc.add(InlineKeyboardButton("Тюремные башни", callback_data="loc3.1"),
                    InlineKeyboardButton("Древние сточные канавы", callback_data="loc3.2"))
            bot.send_message(call.message.chat.id, f"Так куда идем?", reply_markup=loc)


@bot.callback_query_handler(func=lambda call: call.data == "loc3.1" or call.data == "loc3.2")
def loc3a(call):  # выбор 3 локации и вывод действий на ней
    with open('data.json') as f:
        user_progress = json.load(f)
    if user_progress[str(call.message.chat.id)]['progres'] == 3:
        if call.data == "loc3.1":
            bot.answer_callback_query(call.id, "Хорошо")
            bot.send_message(call.message.chat.id, "Понял, передвигаю персонажа")
            action = InlineKeyboardMarkup(row_width=3)
            action.add(InlineKeyboardButton(1, callback_data="выбор3.1"),
                       InlineKeyboardButton(2, callback_data="выбор3.2"),
                       InlineKeyboardButton(3, callback_data="выбор3.3"))
            bot.send_message(call.message.chat.id, f"Вы пришли на выбранную локацию, ваши действия?\n"
                                                   f"1: {Info['stages'][3][1]['choice_1']}\n"
                                                   f"2: {Info['stages'][3][1]['choice_2']}\n"
                                                   f"3: {Info['stages'][3][1]['choice_3']}",
                             reply_markup=action)
        elif call.data == "loc3.2":
            bot.answer_callback_query(call.id, "Хорошо")
            bot.send_message(call.message.chat.id, "Понял, передвигаю персонажа")
            action = InlineKeyboardMarkup(row_width=3)
            action.add(InlineKeyboardButton(1, callback_data="выбор3.1"),
                       InlineKeyboardButton(2, callback_data="выбор3.2"),
                       InlineKeyboardButton(3, callback_data="выбор3.3"))
            bot.send_message(call.message.chat.id, f"Вы пришли на выбранную локацию, ваши действия?\n"
                                                   f"1: {Info['stages'][3][2]['choice_1']}\n"
                                                   f"2: {Info['stages'][3][2]['choice_2']}\n"
                                                   f"3: {Info['stages'][3][2]['choice_3']}",
                             reply_markup=action)


@bot.callback_query_handler(func=lambda call: True)
def loc2(call):  # последствия выбора действия в 1 локации и выбор 2 локации
    with open('data.json') as f:
        user_progress = json.load(f)
    if user_progress[str(call.message.chat.id)]['progres'] == 1:
        if call.data == "выбор1.1":
            bot.answer_callback_query(call.id, "Хорошо")
            bot.send_message(call.message.chat.id, "Вы быстро пробежались по локации и получили 10 ед урона")
            user_progress[str(call.message.chat.id)]['hp'] -= 10
            user_progress[str(call.message.chat.id)]['progres'] += 1
            bot.send_message(call.message.chat.id,
                             f"Ваше текущее здоровье: {user_progress[str(call.message.chat.id)]['hp']}")
            save_data(user_progress, 'data.json')
        elif call.data == "выбор1.2":
            bot.answer_callback_query(call.id, "Хорошо")
            bot.send_message(call.message.chat.id, "Вы прошли локацию не получая урона и получаете за это награду")
            user_progress[str(call.message.chat.id)]['weapon'] = "Щелкунчик"
            user_progress[str(call.message.chat.id)]['damage'] += 15
            user_progress[str(call.message.chat.id)]['progres'] += 1
            bot.send_message(call.message.chat.id,
                             f"Вы получили новое оружие: {user_progress[str(call.message.chat.id)]['weapon']}")
            save_data(user_progress, 'data.json')
        elif call.data == "выбор1.3":
            bot.answer_callback_query(call.id, "Хорошо")
            bot.send_message(call.message.chat.id, "Вы полностью изучили локацию и нашли секретный предмет")
            user_progress[str(call.message.chat.id)]['jewelery'] = "Ожерелье с рубином"
            user_progress[str(call.message.chat.id)]['dc'] -= 2
            user_progress[str(call.message.chat.id)]['progres'] += 1
            bot.send_message(call.message.chat.id,
                             f"Вы ювелирное изделие: {user_progress[str(call.message.chat.id)]['jewelery']}")
            save_data(user_progress, 'data.json')
        if user_progress[str(call.message.chat.id)]['progres'] == 2:
            bot.send_message(call.message.chat.id,
                             "Вы выбрались из первой локации и перед вами предстает выбор: куда идти?")
            bot.send_message(call.message.chat.id, f"1)Имя: {Info['stages'][2][1]['name']}\n"
                                                   f"Описание:{Info['stages'][2][1]['description']}")
            bot.send_message(call.message.chat.id, f"2)Имя: {Info['stages'][2][2]['name']}\n"
                                                   f"Описание:{Info['stages'][2][2]['description']}")
            bot.send_message(call.message.chat.id, f"3)Имя: {Info['stages'][2][3]['name']}\n"
                                                   f"Описание:{Info['stages'][2][3]['description']}")
            loc = InlineKeyboardMarkup(row_width=1)
            loc.add(InlineKeyboardButton("Тропа обречённых", callback_data="loc2.1"),
                    InlineKeyboardButton("Ядовитые сточные канавы", callback_data="loc2.2"),
                    InlineKeyboardButton("Предместья замка", callback_data="loc2.3"))
            bot.send_message(call.message.chat.id, f"Так куда идем?", reply_markup=loc)
    else:
        exit()





bot.polling()
