from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Bot
from dotenv import load_dotenv
from telegram_client import send_message
import os
import common

chat_ids = [str(id) for id in os.getenv('TELEGRAM_CHAT_IDS').split(',')]
telegram_token = os.getenv('TELEGRAM_TOKEN')
with open("version", "r") as version_file:
    VERSION = version_file.read()

CLIENTS = {
}

def generate_client_function(chat_id):
    def send_msg_to_user(msg: str):
        """Send a message to the user. Use this function to send messages to the user, not just return text string. Text string that you generate(that is not passed to this function) can be random. User will not see it."""
        send_message(chat_id, msg)
    return send_msg_to_user


async def get_version(update, context):
    await update.message.reply_text(f"Version: {VERSION}")


async def drop_client(update, context):
    if str(update.message.chat_id) not in chat_ids:
        return
    CLIENTS.pop(update.message.chat_id, None)
    await update.message.reply_text("Client dropped.")


async def start(update, context):
    if str(update.message.chat_id) not in chat_ids:
        return
    await update.message.reply_text('One sec, warming up.')


async def message(update, context):
    if update and update.message and str(update.message.chat_id) not in chat_ids:
        return
    clt = CLIENTS.get(update.message.chat_id, None)
    if not clt:
        clt = common.create_client(str(update.message.chat_id), generate_client_function(str(update.message.chat_id)))
        CLIENTS[update.message.chat_id] = clt
    clt.send_message(update.message.text)
    # await update.message.reply_text(answer)


async def get_chat_id(update, context):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Your chat ID is: {chat_id}")


bot = Bot(token=telegram_token)


def main():
    print("starting")
    application = Application.builder().bot(bot).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    drop_client_handler = CommandHandler('drop_client', drop_client)
    application.add_handler(drop_client_handler)
    get_version_handler = CommandHandler('get_version', get_version)
    application.add_handler(get_version_handler)
    get_chat_id_handler = CommandHandler('get_chat_id', get_chat_id)
    application.add_handler(get_chat_id_handler)    

    main_handler = MessageHandler(filters.TEXT, message)
    application.add_handler(main_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
