import os
from datetime import datetime

import telebot

from settings.message import get_message


# getting and checking variables
TOKEN = os.environ.get('TOKEN')
ADMIN_USER_ID = os.environ.get('ADMIN_USER_ID')
if not TOKEN or not ADMIN_USER_ID:
    raise LookupError(
        'Please define TOKEN and ADMIN_USER_ID as environ vars'
    )

if not ADMIN_USER_ID.strip().isdigit():
    raise TypeError(f'Incorrect ADMIN_USER_ID ({ADMIN_USER_ID})')
ADMIN_USER_ID = int(ADMIN_USER_ID.strip())

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Dictionary to store the messages
# TODO: move to database
messages = {}
# ID of the admin user
admins = [ADMIN_USER_ID]


def admin_filter(message):
    """
    Administrator filter
    """
    user_id = message.from_user.id
    return user_id in admins


@bot.message_handler(commands=['start'])
def send_welcome(message):
  """
  Answer to start message.
  """
  bot.reply_to(message, get_message('start'), parse_mode='HTML')


@bot.message_handler(commands=['help'])
def send_welcome(message):
  """
  Answer to help message.
  """
  bot.reply_to(message, get_message('help'), parse_mode='HTML')


@bot.message_handler(commands=['clear'])
def clear_history(message):
    """
    Clear all the answers in the table.
    """
    if not admin_filter(message):
        return
    messages.clear()
    bot.send_message(message.chat.id, 'Список ответов очищен.')


@bot.message_handler(commands=['answers'])
def send_answers(message):
    """
    Create table with answers and send it to the admin.
    """
    if not admin_filter(message):
        return
    # Generate a table with all the messages
    table = '№ - Пользователь - Ответ - Дата и время\n'
    for i, (user, answer, date) in enumerate(messages.values(), start=1):
        table += f'{i} - {user} - {answer} - {date}\n'
    bot.send_message(message.chat.id, table)


@bot.message_handler(func=lambda message: True)
def collect_messages(message):
    """
    Get messages from users and store their answers.
    """
    err_msg = get_message('incorrect')
    message_parts = message.text.split(' ', 1)
    if len(message_parts) == 2:
        number, text = message_parts
        number = number.strip()
        # TODO: why not to use the number and store it in messages?
        if number.isdigit() and number in ['1', '2', '3', '4']:
            messages[message.message_id] = (message.from_user.first_name, text, datetime.now())
            bot.send_message(message.chat.id, 'Сообщение сохранено.')
    else:
        bot.send_message(message.chat.id, err_msg, parse_mode='HTML')


if __name__ == '__main__':
    # Run the bot
    bot.polling()
