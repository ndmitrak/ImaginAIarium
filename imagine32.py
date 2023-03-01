import telebot

bot = telebot.TeleBot('5874216138:AAFxfGM4_Ooc3MnZ5fX3fDd-Vg5DA_fMYts')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот для сбора сообщений в формате 'Цифра текст'. Пожалуйста, используйте этот формат при отправке сообщений.")

@bot.message_handler(func=lambda message: True)
def collect_messages(message):
    message_parts = message.text.split(' ', 1)
    if len(message_parts) == 2:
        number, text = message_parts
        number = number.strip()
        if number.isdigit():
            # здесь нужно добавить код для сбора сообщений и сохранения их в базе данных или файле
            bot.send_message(message.chat.id, "Сообщение сохранено.")
        else:
            bot.send_message(message.chat.id, "Некорректный формат сообщения. Пожалуйста, используйте формат 'Цифра текст'.")
    else:
        bot.send_message(message.chat.id, "Некорректный формат сообщения. Пожалуйста, используйте формат 'Цифра текст'.")

bot.polling()



