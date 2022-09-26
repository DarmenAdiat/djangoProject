import bot_config
import telebot
from telebot import types
import sqlite3
import random


bot = telebot.TeleBot(bot_config.token)


@bot.message_handler(commands=['start'])
def start(message):
    print('Started')

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

    markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item0 = types.KeyboardButton("Главное меню")
    markup_menu.add(item0)
    bot.send_message(message.chat.id, 'Добро пожаловать, ' + message.from_user.first_name + '!',
                     reply_markup=markup_menu)

    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Получить одноразовый пароль", callback_data='code')
    item2 = types.InlineKeyboardButton("Изменить номер телефона", callback_data='phone')
    markup.add(item1)
    markup.add(item2)

    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)


@bot.message_handler(func=lambda m: m.text in ['/main', 'Главное меню'])
def main(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Получить одноразовый пароль", callback_data='code')
    item2 = types.InlineKeyboardButton("Изменить номер телефона", callback_data='phone')
    markup.add(item1)
    markup.add(item2)

    markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item0 = types.KeyboardButton("Главное меню")
    markup_menu.add(item0)

    bot.send_message(message.chat.id, '*Главное меню*', reply_markup=markup_menu, parse_mode="Markdown")
    bot.send_message(message.chat.id, '*Выберите действие:*', reply_markup=markup, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'code':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                send_contact = types.KeyboardButton(text="Отправить контакт", request_contact=True)
                menu = types.KeyboardButton("Главное меню")
                markup.add(send_contact, menu)
                bot.send_message(call.message.chat.id, text='Отправьте свой контакт', reply_markup=markup)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Получить одноразовый пароль', reply_markup=None)
                bot.register_next_step_handler(call.message, check_phone)

            elif call.data == 'phone':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                send_contact = types.KeyboardButton(text="Отправить контакт", request_contact=True)
                menu = types.KeyboardButton("Главное меню")
                markup.add(send_contact, menu)
                bot.send_message(call.message.chat.id, text='Отправьте свой контакт', reply_markup=markup)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Изменить номер телефона', reply_markup=None)
                bot.register_next_step_handler(call.message, check_phoneChange)

    except Exception as e:
        print(repr(e))


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

        markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item0 = types.KeyboardButton("Главное меню")
        markup_menu.add(item0)

        bot.send_message(message.chat.id, "Отлично, теперь введите Ваш ИИН", reply_markup=markup_menu)
        bot.register_next_step_handler(message, check_iin, telegram_phone)

    else:
        markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item0 = types.KeyboardButton("Главное меню")
        markup_menu.add(item0)
        bot.send_message(message.chat.id, "Некорректный контакт, вернитесь в Главное меню и попробуйте еще раз", reply_markup=markup_menu)


def check_iin(message, telegram_phone):
    if message.text.isdigit():  # если ИИН имеет числовое значение, ИНТЕДЖЕР, то:
        id_num = str(message.text)

        connect = sqlite3.connect('db.sqlite3')
        cursor = connect.cursor()

        cursor.execute(f"SELECT id_num, is_active FROM users_customuser WHERE id_num = \"{id_num}\"")

        data = cursor.fetchone()

        if data:  # если нашли ИИН в базе
            if data[1] == 1:  # если нашли ИИН в базе и он уже активированный, пишем ошибку
                bot.send_message(message.chat.id, "Опаньки... Ваш аккаунт уже был активирован ранее!")
            else:  # если нашли ИИН в базе и он НЕ активированный, выполняем код:
                if telegram_phone:  # если телефон был прислан, то выполняем код далее:
                    # здесь сверяем телефон из чата с тем что есть в базе
                    cursor.execute(f"SELECT id_num, phone FROM users_customuser WHERE id_num = \"{id_num}\"")
                    data2 = cursor.fetchone()
                    if data2:  # смотрим нашли ли мы этого пользователя, если нашли, то:
                        users_phone = data2[1]

                        if str(users_phone) == str(telegram_phone):

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


def check_phoneChange(message):
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

        markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item0 = types.KeyboardButton("Главное меню")
        markup_menu.add(item0)

        bot.send_message(message.chat.id, "Отлично, теперь введите Ваш ИИН", reply_markup=markup_menu)
        bot.register_next_step_handler(message, check_iinChange, telegram_phone)

    else:
        markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item0 = types.KeyboardButton("Главное меню")
        markup_menu.add(item0)
        bot.send_message(message.chat.id, "Некорректный контакт, вернитесь в Главное меню и попробуйте еще раз",
                         reply_markup=markup_menu)


def check_iinChange(message, telegram_phone):
    if message.text.isdigit():  # если ИИН имеет числовое значение, ИНТЕДЖЕР, то:

        id_num = message.text

        connect = sqlite3.connect('db.sqlite3')
        cursor = connect.cursor()

        cursor.execute(f"SELECT id_num, is_active, id FROM users_customuser WHERE id_num = \"{id_num}\"")
        data = cursor.fetchone()

        if data:  # если нашли ИИН в базе
            if data[1] == 0:  # если нашли ИИН в базе и он еще не активированный, пишем ошибку
                bot.send_message(message.chat.id, "Опаньки... Ваш аккаунт еще не активирован!")
            else:  # если нашли ИИН в базе и он НЕ активированный, выполняем код:
                if telegram_phone:  # если телефон был прислан, то выполняем код далее:
                    # здесь сверяем телефон из чата с тем что есть в базе
                    cursor.execute(f"SELECT phone, v_code FROM users_editphone WHERE id_num = \"{id_num}\"")
                    data2 = cursor.fetchone()
                    if data2:  # смотрим нашли ли мы этого пользователя, если нашли, то:
                        users_phone = data2[0]

                        if str(users_phone) == str(telegram_phone):
                            oneoff = data2[1]
                            bot.send_message(message.chat.id, 'Ваш код подтверждения:')
                            bot.send_message(message.chat.id, oneoff)  # отдаем пароль в чат
                        else:
                            bot.send_message(message.chat.id,
                                             "Опаньки... Ваш телефон на сайте и ваш контакт отличаются, "
                                             "попробуйте заполнить форму регистрации на сайте еще раз")  # отдаем пароль в чат
                            return
                    else:  # если НЕ НАШЛИ, то:
                        bot.send_message(message.chat.id, 'Чтобы изменить номер телефона, Вам необходимо выбрать данную функцию в Личном кабинете на веб-портале intra.isker.kz')
                        return
        else:  # если не нашли ИИН в базе то пишем ошибку
            bot.send_message(message.chat.id, 'Опаньки... Ваш ИИН не зарегистрирован в базе пользователей')

    else:  # если есть символы или пробелы в строке то пишем ошибку
        bot.send_message(message.chat.id, "Опаньки... Вы неправильно ввели ИИН, выполните запрос еще раз")


if __name__ == '__main__':
    bot.infinity_polling()
