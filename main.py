from telegram import *
from telegram.ext import *

import constants as keys
import responses as R
import transaction as T

print("Bot enchufado...")

def start_command(update, context):
    update.message.reply_text('Hola!\nBienvenido al bot de EscuelaCryptoES\nSi quieres recibir 1 ETH de Rinkeby para empezar a tope a programar, escribe /address y tu dirección de Ethereum')

def handle_message(update, context):
    print(update)
    if update.message.chat['title'] == 'Jefazos EscuelaCryptoES':
        text = str(update.message.text).lower()
        response = R.sample_responses(text)

        if len(response) == keys.AVERAGE_ETHEREUM_ADDRESS_LENGTH:
            user = update.message.from_user['username']
            user_address = response
            
            update.message.reply_text("Enviando 1 ETH de Rinkeby al jefazo " + user)
            transaction_response = T.transaction(user, user_address)
            if transaction_response:
                update.message.reply_text("Transacción finalizada, disfruta de tu Ether :)")
            else:
                update.message.reply_text("Transacción fallida, ¿estás seguro que no tienes tu Ether diario ya?")
        else:
            update.message.reply_text(response)
    else:
        keyboard = [[InlineKeyboardButton(text='Unete al grupo', url='https://t.me/joinchat/Wr0jQzAWqaw4Yjc8')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Para usar este bot debes estar en el grupo de @EscuelaCryptoES", reply_markup = reply_markup)

def error(update,context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(keys.API_KEY, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", start_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

main()