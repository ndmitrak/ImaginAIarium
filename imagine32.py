import telebot
from datetime import datetime

# Initialize the bot
bot = telebot.TeleBot('5874216138:AAFxfGM4_Ooc3MnZ5fX3fDd-Vg5DA_fMYts')

# Dictionary to store the messages
messages = {}

# ID of the admin user
admin_user_id = 193521537


# Define the administrator filter
def admin_filter(message):
    if message.new_chat_member:
        user_id = message.new_chat_member.id
    else:
        user_id = message.from_user.id
    return user_id == admin_user_id


# Define the message handler
@bot.message_handler(func=lambda message: True)
def collect_messages(message):
    if admin_filter(message):
        if message.text == '/clear':
            messages.clear()
            bot.send_message(message.chat.id, "Список ответов очищен.")
            return

        if message.text == '/answers':
            # Generate a table with all the messages
            table = '№ - Пользователь - Ответ - Дата и время\n'
            for i, (user, answer, date) in enumerate(messages.values(), start=1):
                table += f'{i} - {user} - {answer} - {date}\n'
            bot.send_message(message.chat.id, table)
            return

    message_parts = message.text.split(' ', 1)
    if len(message_parts) == 2:
        number, text = message_parts
        number = number.strip()
        if number.isdigit() and number in ['1', '2', '3', '4']:
            messages[message.message_id] = (message.from_user.first_name, text, datetime.now())
            bot.send_message(message.chat.id, "Сообщение сохранено.")
        else:
            bot.send_message(message.chat.id, "Некорректный формат сообщения. Пожалуйста, используйте формат 'Цифра текст'.")
    else:
        bot.send_message(message.chat.id, "Некорректный формат сообщения. Пожалуйста, используйте формат 'Цифра текст'.")


# Run the bot
bot.polling()