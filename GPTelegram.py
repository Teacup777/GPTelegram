from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

#ChatGPT Telegram bot by Teacup

# -*- coding: utf-8 -*-
openai.api_key = 'your openai key'
TOKEN: Final = 'token of your bot'
BOT_USERNAME: Final = '@ of your bot'


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('The first message you want bot to send')


def get_content(in_prompt):
    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=in_prompt,
                                        temperature=0.6,
                                        max_tokens=3900)
    return response


def handle_response(text):
    processed = text.lower()

    models = openai.Model.list()

    print(models.data[0].id)

    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                   messages=[{"role": "user", "content": processed}])

    odpowiedz = chat_completion.choices[0].message.content

    return odpowiedz


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            response: str = handle_response(text)
            return response
        else:
            return 0
    else:
        response: str = handle_response(text)

        print('Bot:', response)
        await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print('Polling')
    app.run_polling(poll_interval=3)