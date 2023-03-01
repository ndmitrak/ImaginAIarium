import logging
import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# установка уровня логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# токен вашего бота
TOKEN = '5874216138:AAFxfGM4_Ooc3MnZ5fX3fDd-Vg5DA_fMYts'

# создание экземпляра Telegram-бота
bot = telegram.Bot(token=TOKEN)

# создание экземпляра обновления Telegram-бота
updater = Updater(token=TOKEN, use_context=True)

# обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Привет! Я бот-викторина. Я буду показывать картинки, а ты должен будешь оставить в комментарии свой ответ. Ты сможешь видеть комментарии других пользователей только после того, как отправишь свой ответ.")

# обработчик новых сообщений
def new_message(update, context):
    chat_id = update.effective_message.chat_id

    if update.effective_message:
        user_id = update.message.from_user.id
        message_id = update.message.message_id

        # получаем список сообщений в канале
        messages = bot.get_chat_history(chat_id, limit=1000)

        # проверяем, был ли написан пользователем хотя бы один комментарий
        has_comment = False
        for message in messages:
            if message.from_user.id == user_id and message.message_id != message_id and message.reply_to_message is not None:
                has_comment = True
                break

        # если пользователь еще не написал комментарий, скрываем все сообщения кроме его сообщения
        if not has_comment:
            for message in messages:
                if message.from_user.id != user_id:
                    context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)

# добавление обработчиков команд и сообщений
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.photo, new_message))

# запуск Telegram-бота
updater.start_polling()