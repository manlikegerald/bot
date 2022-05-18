import Constants as keys
from telegram.ext import *
import Responses as R
import Model as M

print("Bot Started...")
def start_command(update, context):
    update.message.reply_text("Hello buddy!!!")
    update.message.reply_text("What's up?")

def help_command(update, context):
    update.message.reply_text("This bot is at its testing phase so if you need any help, please go on google!")

def handle_message(update, context):
    text = str(update.message.text).lower()
    print("The query: " + text)
    #response = R.sample_responses(text)
    response = M.model_input(text)
    update.message.reply_text(response)

def error(update, context):
    print(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("start", help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()



main()


