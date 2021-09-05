from telegram import *
from telegram.ext import *

import constants as keys
import responses as R
import transaction as T

print("Bot enchufado...")

def start_command(update, context):
    update.message.reply_text('Hola '+ update.message.from_user['username'] +', \n¡Bienvenid@ al faucet-bot de EscuelaCryptoES! 😎😁\n\nSi quieres recibir 1 ETH en la red de Rinkeby y empezar a tope a programar, escribe /address y tu dirección de Ethereum a continuación.\nEj: /address 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 (Cambia esta dirección, si no estarás enviando 1 ETH al mismisimo Vitalik Buterin 🤪🤫) \n\n ¡Mucha suerte en tu proyecto!👨‍💻👩‍💻')

def help_command(update,context):
    update.message.reply_text("USO:\n\n/address [ETHEREUM_ADDRESS]")

def handle_message(update, context):
    print(update)
    #########if update.message.chat['title'] == 'Jefazos EscuelaCryptoES':
    text = str(update.message.text).lower()
    response = R.sample_responses(text)

    if len(response) == keys.AVERAGE_ETHEREUM_ADDRESS_LENGTH:
        user = update.message.from_user['username']
        user_address = response
        
        ####update.message.reply_text("Enviando 1 ETH de Rinkeby al jefazo " + user)
        update.message.reply_text("Enviando 1 ETH de Rinkeby a " + user)
        transaction_response = T.transaction(user, user_address)
        if transaction_response:
            update.message.reply_text("Transacción finalizada, disfruta de tu ETH :)")
        else:
            update.message.reply_text("Transacción fallida, ¿estás seguro que no tienes tu ETH diario ya?")
    elif response.__contains__("0x"):
        update.message.reply_text("¿Me estás vacilando? Escribe tu dirección completa si no te meto en la lista negra")
    else:
        update.message.reply_text(response)
    #####else:
        #####keyboard = [[InlineKeyboardButton(text='Unete al grupo', url='https://t.me/joinchat/Wr0jQzAWqaw4Yjc8')]]
        #####reply_markup = InlineKeyboardMarkup(keyboard)
        #####update.message.reply_text("Para usar este bot debes estar en el grupo de @EscuelaCryptoES", reply_markup = reply_markup)

def error(update,context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(keys.API_KEY, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

main()