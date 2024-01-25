# Библиотеки
import telebot
from telebot import types
import os
import datetime
import sqlite3

# Инициализация бота
token = 'TOKEN_TG_BOT'
bot = telebot.TeleBot(token)

# /start
@bot.message_handler(commands=['start'])
def start(message):
    # Передача привета
    bot.send_message(message.chat.id, "Дарова, это наверное мой первый лично написанный проект на python, для отображения расписания. Для обновления используется web-скрапинг, поэтому обновление может занять некоторое время. Также вы пожете стать последователем моего творчества для использования в своей группе, написав в dm @requiemzxc_komaru")
    bot.send_message(message.chat.id, "Я не стал добавлять отдельную кнопку для пожертвований, но если вам интересна такая деятельность, нажмите на /donate")
    # Кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Обновить")
    item2 = types.KeyboardButton("Посмотреть")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

# /donate
@bot.message_handler(commands=['donate'])
def donate(message):
    # Донатка
    bot.send_message(message.chat.id, "[На эти деньги я могу и поесть, и хост продлить)](https://pay.cloudtips.ru/p/04e90a41)", parse_mode='Markdown', disable_web_page_preview=True)
    
# Таймер
last_update_time = None



# Дальше могли быть комменты, но там и так все понятно, камон



@bot.message_handler(content_types=['text'])
def handle_text(message):
    global last_update_time
    if message.text == "Обновить":
        if last_update_time is None or (datetime.datetime.now() - last_update_time).total_seconds() > 6*60*60:
            bot.send_message(message.chat.id, "Идет обновление базы данных. Покури сходи.")
            os.system("python main.py")
            bot.send_message(message.chat.id, "Обновились)")
            last_update_time = datetime.datetime.now()
        else:
            bot.send_message(message.chat.id, "Какой-то пользователь уже обновил базу, каждое обновление можно провести раз в 6 часов, и обычно если есть изменения расписания, то ваши кураторы сообщают вам в группе.")
    elif message.text == "Посмотреть":
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text="П-210", callback_data="button1")
        button2 = types.InlineKeyboardButton(text="ПД-218", callback_data="button2")
        keyboard.add(button1)
        keyboard.add(button2)
        bot.send_message(message.chat.id, "Выбери группу:", reply_markup=keyboard)
        bot.send_message(message.chat.id, "[Присоеденяйся к группе, знай о обновлениях!](https://t.me/t1brime)", parse_mode='MarkdownV2', disable_web_page_preview=True)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "button1":
            bot.send_message(call.message.chat.id, "Вы выбрали 'П-210'")
            conn = sqlite3.connect('mydatabase.db')
            c = conn.cursor()
            c.execute('SELECT DISTINCT date FROM schedule_210')
            dates = c.fetchall()
            keyboard = types.InlineKeyboardMarkup()
            for date in dates:
                button = types.InlineKeyboardButton(text=date[0], callback_data=f"group_210_{date[0]}")
                keyboard.add(button)
            bot.send_message(call.message.chat.id, "Выберите дату:", reply_markup=keyboard)
            conn.close()
        if call.data == "button2":
            bot.send_message(call.message.chat.id, "Вы выбрали 'ПД-218'")
            conn = sqlite3.connect('mydatabase.db')
            c = conn.cursor()
            c.execute('SELECT DISTINCT date FROM schedule_218')
            dates = c.fetchall()
            keyboard = types.InlineKeyboardMarkup()
            for date in dates:
                button = types.InlineKeyboardButton(text=date[0], callback_data=f"group_218_{date[0]}")
                keyboard.add(button)
            bot.send_message(call.message.chat.id, "Выберите дату:", reply_markup=keyboard)
            conn.close()
        elif call.data.startswith("group_210_"):
            group = "210"
            date = call.data.split("_")[2]
            conn = sqlite3.connect('mydatabase.db')
            c = conn.cursor()
            c.execute(f'SELECT * FROM schedule_{group} WHERE date="{date}"')
            schedule = c.fetchall()
            for day in schedule:
                # разбиваем day на строки и удаляем первую строку (дату)
                schedule_without_date = '\n'.join(day[1].split('\n')[1:])
                bot.send_message(call.message.chat.id, day[0] + '\n' + schedule_without_date)
            conn.close()
            bot.send_message(call.message.chat.id, "[Поддержи мой проект](https://pay.cloudtips.ru/p/04e90a41)", parse_mode='MarkdownV2', disable_web_page_preview=True)
        elif call.data.startswith("group_218_"):
            group = "218"
            date = call.data.split("_")[2]
            conn = sqlite3.connect('mydatabase.db')
            c = conn.cursor()
            c.execute(f'SELECT * FROM schedule_{group} WHERE date="{date}"')
            schedule = c.fetchall()
            for day in schedule:
                # разбиваем day на строки и удаляем первую строку (дату)
                schedule_without_date = '\n'.join(day[1].split('\n')[1:])
                bot.send_message(call.message.chat.id, day[0] + '\n' + schedule_without_date)
            conn.close()
            bot.send_message(call.message.chat.id, "[Поддержи мой проект](https://pay.cloudtips.ru/p/04e90a41)", parse_mode='MarkdownV2', disable_web_page_preview=True)
bot.infinity_polling()
# Шляпа какая-то, но работает, и это главное