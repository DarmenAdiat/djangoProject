import telebot
import sqlite3
import random
from telebot import types

bot = telebot.TeleBot("5084541117:AAE-ALCPh_H1r8Fs8PdMCcfS5sPtSbGL-Ds")


@bot.message_handler(commands=['start'])
def start(message):
    print(message.chat)

    connect = sqlite3.connect('db.sqlite3')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS telegram_chats(
        id INTEGER, phone CHAR, username CHAR, first_name CHAR, last_name CHAR 
    )""")

    connect.commit()

    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM telegram_chats WHERE id = {people_id}")
    data = cursor.fetchone()

    if data is None:
        user_id = [message.chat.id]
        cursor.execute("INSERT INTO telegram_chats (id) VALUES (?);", user_id)
        connect.commit()
    # else:
    #     bot.send_message(message.chat.id, 'Ваш id уже есть!')

    bot.send_message(message.chat.id, 'Добро пожаловать, ' + message.from_user.first_name + '!')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Получить одноразовый пароль")
    markup.add(item1)

    # item2 = types.KeyboardButton(text="Отправить свой контакт", request_contact=True)
    # markup.add(item2)

    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)


# @bot.message_handler(content_types='text')
# def message_reply(message):
#     if message.text == "Получить одноразовый пароль":
#         bot.send_message(message.chat.id, "Введите ваш ИИН")
#         bot.register_next_step_handler(message, check_iin)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Получить одноразовый пароль":
        key_contact = types.ReplyKeyboardMarkup(resize_keyboard=True)
        send_contact = types.KeyboardButton(text="Отправить контакт", request_contact=True)
        key_contact.add(send_contact)
        bot.send_message(message.chat.id, text='Отправьте свой контакт', reply_markup=key_contact)


def check_iin(message, telegram_phone):
    if message.text.isdigit():  # если ИИН имеет числовое значение, ИНТЕДЖЕР, то:
        # bot.send_message(message.chat.id, message.text) вставить сюда
        id_num = message.text

        connect = sqlite3.connect('db.sqlite3')
        cursor = connect.cursor()

        cursor.execute(f"SELECT id_num, is_active FROM users_customuser WHERE id_num = {id_num}")
        data = cursor.fetchone()
        # print(data[1])
        if data:  # если нашли ИИН в базе
            if data[1] == 1:  # если нашли ИИН в базе и он уже активированный, пишем ошибку
                bot.send_message(message.chat.id, "Опаньки... Ваш аккаунт уже был активирован ранее!")
            else:  # если нашли ИИН в базе и он НЕ активированный, выполняем код:
                if telegram_phone:  # если телефон был прислан, то выполняем код далее:
                    # здесь сверяем телефон из чата с тем что есть в базе
                    cursor.execute(f"SELECT id_num, phone FROM users_customuser WHERE id_num = {id_num}")
                    data2 = cursor.fetchone()
                    if data2:  # смотрим нашли ли мы этого пользователя, если нашли, то:
                        users_phone = data2[1]
                        # users_phone = users_phone.replace('+', '')
                        # telegram_phone = telegram_phone.replace('+', '')
                        print(users_phone)
                        print(telegram_phone)
                        if str(users_phone) == str(telegram_phone):
                            bot.send_message(message.chat.id,
                                             "Телефоны совпали, работаем дальше")  # отдаем пароль в чат
                            oneoff = ''
                            for x in range(10):  # генерим одноразовый пароль и пишем его в базу
                                oneoff = oneoff + random.choice(
                                    list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))

                            cursor.execute("UPDATE users_customuser SET one_off = (?), phone = (?) WHERE id_num = (?)",
                                           (oneoff, telegram_phone, id_num))
                            connect.commit()
                            bot.send_message(message.chat.id, 'Ваш одноразовый пароль:')
                            bot.send_message(message.chat.id, oneoff)  # отдаем пароль в чат
                        else:
                            bot.send_message(message.chat.id,
                                             "Опаньки... Введенный вами телефон на сайте и ваш контакт отличаются, "
                                             "попробуйте заполнить форму регистрации на сайте еще раз")  # отдаем пароль в чат
                            return
                    else:  # если НЕ НАШЛИ, то:
                        return
        else:  # если не нашли ИИН в базе то пишем ошибку
            bot.send_message(message.chat.id, 'Опаньки... Ваш ИИН не зарегистрирован в базе пользователей')

    else:  # если есть символы или пробелы в строке то пишем ошибку
        bot.send_message(message.chat.id, "Опаньки... Вы неправильно ввели ИИН, запросите пароль еще раз")


@bot.message_handler(content_types=["contact"])
def check_phone(message):
    if message.contact is not None:
        telegram_phone = message.contact.phone_number  # присланный телефон
        telegram_phone = telegram_phone.replace('+', '')
        telegram_phone = '+'+telegram_phone

        username = message.chat.username  # имя пользователя из чата
        first_name = message.chat.first_name  # Имя из чата
        last_name = message.chat.last_name  # Фамилия из чата
        user_id = message.chat.id  # Идентификатор пользователя из чата
        connect = sqlite3.connect('db.sqlite3')
        cursor = connect.cursor()
        cursor.execute(
            "UPDATE telegram_chats SET phone = (?), username = (?), first_name = (?), last_name = (?) WHERE id = (?)",
            (telegram_phone, username, first_name, last_name, user_id))
        connect.commit()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Получить одноразовый пароль")
        markup.add(item1)
        bot.send_message(message.chat.id, "Отлично, теперь введите Ваш ИИН", reply_markup=markup)
        bot.register_next_step_handler(message, check_iin, telegram_phone)


# bot.polling(none_stop=True, interval=0)
bot.infinity_polling()