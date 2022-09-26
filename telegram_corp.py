import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot("5702386910:AAFqcAU0GhrG4jr9dc2_g_OvuYsRYqDnTBw")
admin_id = 968868460

@bot.message_handler(commands=['start'])
def start(message):
    print('Started')

    connect = sqlite3.connect('db.sqlite3')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS corp_chats(
        id INTEGER, phone CHAR, username CHAR, first_name CHAR, last_name CHAR 
    )""")
    connect.commit()

    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM corp_chats WHERE id = {people_id}")
    data = cursor.fetchone()

    if data is None:
        user_id = [message.chat.id]
        cursor.execute("INSERT INTO corp_chats (id) VALUES (?);", user_id)
        connect.commit()


    bot.send_message(message.chat.id, 'Привет, Путя =)')
    bot.send_message(message.chat.id, 'Давай сыграем в небольшую игру?')
    # отправляю в свой чат Логи
    bot.send_message(admin_id, 'Путя запустила бота')

    markup = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton("Начнём", callback_data='location_0')
    markup.add(item1)
    bot.send_message(message.chat.id, 'Когда будешь готова, нажми на кнопку внизу', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'location_0':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("Я нашла первый ключ!", callback_data='location_1')
                markup.add(item1)
                # отправляю в свой чат Логи
                bot.send_message(admin_id, 'Игра началась')

                bot.send_message(call.message.chat.id, 'Отправляю тебе точку на карте, доберись до нее. Там ты найдешь "ключ" и сможешь продолжить Путь')
                bot.send_message(call.message.chat.id, 'P.S.: Но не нажимай кнопки раньше времени, это будет считаться жульничеством и ты можешь лишишься одного ключа!')
                bot.send_message(call.message.chat.id, 'https://go.2gis.com/6xgzi')
                bot.send_message(call.message.chat.id, 'Когда найдешь первый ключ, нажми на кнопку внизу', reply_markup=markup)

            elif call.data == 'location_1':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("Второй ключ у меня! И долго мне их еще искать?", callback_data='location_2')
                markup.add(item1)
                # отправляю в свой чат Логи
                bot.send_message(admin_id, 'Локация 1 - Мраморный дворец - достигнута')

                bot.send_message(call.message.chat.id, 'Поздравляю! Ты нашла первый ключ, но это еще не все. Твой Путь только начинается!')
                bot.send_message(call.message.chat.id, 'А между поиском всех ключей прочитай вот что:')

                bot.send_message(call.message.chat.id, '-------------------------------')
                bot.send_message(call.message.chat.id, 'Любимая, я в тебя влюбляюсь вновь и вновь. Ты мой свет в окошке, моя мечта, мой ангел. Я благодарен судьбе, что она подарила мне тебя, моя милая, желанная, единственная. Я так люблю смотреть в твои красивые глаза, твою милую улыбку. Ты, как лучик солнечного света, согреваешь меня своим теплом. Ты всегда нужна мне, моя любовь. Только с тобой, я чувствую себя самым счастливым человеком. Ты подарила мне радость, ты дала мне надежду. Я люблю тебя, моё солнышко! ♥ ')
                bot.send_message(call.message.chat.id, '-------------------------------')

                bot.send_message(call.message.chat.id, 'А вот и следующая точка, где нужно искать второй ключ')
                bot.send_message(call.message.chat.id, 'https://go.2gis.com/mm167')
                bot.send_message(call.message.chat.id, 'Когда справишься, просто нажми на кнопку внизу',
                                 reply_markup=markup)

            elif call.data == 'location_2':
                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton("Нашла еще один! И что же с ними делать?", callback_data='location_3')
                markup.add(item1)
                # отправляю в свой чат Логи
                bot.send_message(admin_id, 'Локация 2 - Марсово поле - достигнута')

                bot.send_message(call.message.chat.id, 'Воу воу, полегче! Не задавай лишних вопросов, всему свое время!')

                bot.send_message(call.message.chat.id, '-------------------------------')
                bot.send_message(call.message.chat.id, 'Есть прекрасный эпиграф жизни – любовью дорожить умейте. Это совершенно верно, ведь только любовь делает нашу жизнь богаче, щедрей, светлей, только любовь дарит нам радость и надежду. Ведь любовь – это и есть сама жизнь ♥ ')
                bot.send_message(call.message.chat.id, '-------------------------------')

                bot.send_message(call.message.chat.id, 'Теперь отправляйся за поиском третьего ключа')
                bot.send_message(call.message.chat.id, 'https://go.2gis.com/8bnrw')
                bot.send_message(call.message.chat.id, 'Если нашла - жми на кнопку',
                                 reply_markup=markup)

            # elif call.data == 'location_3':
            #     markup = types.InlineKeyboardMarkup(row_width=1)
            #     item1 = types.InlineKeyboardButton("У меня уже четыре ключа, что с ними делать?", callback_data='location_4')
            #     markup.add(item1)
            #     # отправляю в свой чат Логи
            #     bot.send_message(admin_id, 'Локация 3 - Спас на крови - достигнута')
            #
            #     bot.send_message(call.message.chat.id, 'Воу воу, полегче! Ты что такая быстрая))) Не задавай лишних вопросов, всему свое время!')
            #
            #     bot.send_message(call.message.chat.id, '-------------------------------')
            #     bot.send_message(call.message.chat.id, '')
            #     bot.send_message(call.message.chat.id, '-------------------------------')
            #
            #     bot.send_message(call.message.chat.id, 'Ищем четвертый ключ')
            #     bot.send_message(call.message.chat.id, 'https://go.2gis.com/98zne')
            #     bot.send_message(call.message.chat.id, 'Когда будешь на месте, нажми на кнопку внизу',
            #                      reply_markup=markup)

            elif call.data == 'location_3':

                # отправляю в свой чат Логи
                bot.send_message(admin_id, 'Локация 3 - Спас на крови - достигнута')

                bot.send_message(call.message.chat.id, 'Итак, у тебя уже целых три ключа. Можно только гадать для чего они тебе понадобятся')
                bot.send_message(call.message.chat.id, 'На самом деле, не столь важны ключи, как сам Путь!')

                bot.send_message(call.message.chat.id, '-------------------------------')
                bot.send_message(call.message.chat.id, 'Солнышко мое! Ты самая прекрасная в этом мире, и я безумно счастлив, что ты у меня есть!  Я уверен, что ты прекрасно знаешь, что ты – моя родная пуська. Но я хочу, чтобы все об этом узнали. Я готов кричать об этом! Я и ни капли не сомневаюсь в своих чувствах, и я очень тобой дорожу! Ты настолько внезапно появилась в моей жизни, и вообще все так быстро произошло. То чувство, которое возникло, превратилось в безумную любовь к тебе! Я готов исполнить любой твой каприз, лишь бы всегда видеть твою милую улыбку.  Я реально понимаю, что без моей пуськи уже не смогу. Кроме тебя, поверь, мне никто не нужен, никто точно не сможет тебя заменить. Мое сердечко уже навсегда принадлежит тебе. Только с тобой я реально счастлив! ♥ ')
                bot.send_message(call.message.chat.id, '-------------------------------')

                bot.send_message(call.message.chat.id, 'Ты уже близка к цели, осталось совсем немного...')
                bot.send_message(call.message.chat.id, 'https://go.2gis.com/h2ehb')


    except Exception as e:
        print(repr(e))


if __name__ == '__main__':
    bot.infinity_polling()
