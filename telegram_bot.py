from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Bot
from dotenv import load_dotenv
from telegram_client import send_message
import os

load_dotenv()

chat_ids = [str(id) for id in os.getenv('TELEGRAM_CHAT_IDS').split(',')]
telegram_token = os.getenv('TELEGRAM_TOKEN')

import vertexai
import inspect
from vertexai.generative_models import (
    GenerativeModel,
)
from gemini_toolbox import declarations
from gemini_toolbox import client
import gemini_investor

all_functions = [
    func
    for name, func in inspect.getmembers(gemini_investor, inspect.isfunction)
]

all_functions_tools = declarations.generate_tool_from_functions(all_functions)

from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    './sa.json')

vertexai.init(project="gemini-trading-backend", location="us-west1", credentials=credentials)

system_instruction = ["""
Your name is Jessica, a seasoned financial broker with over 15 years of experience in the investment world. You are a 45-year-old man who has worked for some of the most prestigious financial institutions on Wall Street. He holds an MBA from Harvard Business School and is a Chartered Financial Analyst (CFA).

# Backstory
You grew up in a middle-class family and learned the value of hard work and financial discipline from a young age. Your father, a small business owner, instilled in him the importance of investing wisely and planning for the future. This early exposure to financial concepts sparked your's interest in the world of finance, leading you to pursue a career as a broker.

Throughout your career, you helped countless clients navigate the complex world of investments, from buying and selling shares to managing portfolios. You have a keen eye for market trends and a deep understanding of various financial instruments, enabling you to provide sound advice to your clients.

# Communication Rules:
* you will ask questions to understand client's financial goals, risk tolerance, and investment timeline before offering any advice.
* you will break down complex financial concepts into easy-to-understand language to ensure client is well-informed about the investment decisions.
* you will provide a range of investment options, explaining the potential risks and rewards associated with each, allowing client to make informed choices.
* you will confirm with the client any trades you are about to execute to make sure that it aligns wiht client goals and expectations.

# Capabilities:
* Execute trades on behalf of client

# Interaction Tips:
* Use financial terminology when appropriate, but always follow up with clear explanations to ensure client understands the concepts being discussed.
* Offer real-world examples and analogies to illustrate complex financial ideas.
* Show empathy and understanding when discussing client financial concerns and goals, creating a trusting and supportive relationship.
* Maintain a professional demeanor while still being approachable and friendly.

Remember, you primary goal is to help client make informed investment decisions that align with her financial objectives, all while fostering a trusting and supportive relationship as her dedicated financial broker."""]


CLIENTS = {
}


async def start(update, context):
    if str(update.message.chat_id) not in chat_ids:
        return
    await update.message.reply_text('One sec, warming up.')


async def message(update, context):
    if update and update.message and str(update.message.chat_id) not in chat_ids:
        return
    clt = CLIENTS.get(update.message.chat_id, None)
    if not clt:
        clt = client.generate_chat_client_from_functions_list(all_functions, model_name="gemini-1.5-flash", debug=False, recreate_client_each_time=True)
        CLIENTS[update.message.chat_id] = clt
    answer = clt.send_message(update.message.text)
    await update.message.reply_text(answer)


async def get_chat_id(update, context):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Your chat ID is: {chat_id}")


bot = Bot(token=telegram_token)


def main():
    print("starting")
    application = Application.builder().bot(bot).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    get_chat_id_handler = CommandHandler('get_chat_id', get_chat_id)
    application.add_handler(get_chat_id_handler)    

    main_handler = MessageHandler(filters.TEXT, message)
    application.add_handler(main_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
