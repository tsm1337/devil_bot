from email import message
from email.headerregistry import MessageIDHeader
from glob import glob
import logging
from random import choice, randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(filename="bot.log", level=logging.INFO)
logger = logging.getLogger(__name__)



def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text("Здравствуй, пользователь!")
    
def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)

def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Ваше число {user_number}, моё {bot_number}, вы выиграли"
    elif user_number == bot_number:
        message = f"Ваше число {user_number}, моё {bot_number}, ничья"
    else:
        message = f"Ваше число {user_number}, моё {bot_number}, вы проиграли"
    return message

def guess_number(update, context):
    print(context.args)
    if context.args:
         try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
         except (TypeError, ValueError):
            message = "Введите целое число"    
    else:
        message = "Введите число"
    update.message.reply_text(message)

def send_cat_picture(update, context):
    cat_photo_list = glob('images/cat*.jp*g')
    cat_photo_filename = choice(cat_photo_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_photo_filename, 'rb'))


def main():
    mybot = Updater(settings.API_KEY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logger.info("Bot start")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()

