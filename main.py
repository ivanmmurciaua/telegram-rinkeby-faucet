#  Telegram imports
from telegram import *
from telegram.ext import *

#  File imports and other libs
import constants as keys
import responses as R
import transaction as T

import requests
import json

print("Bot enchufado...")

def keyboardCreate(update):
    """==== Returns keyboard to join EscuelaCryptoES ====

    Args:
        update (Any): message info state
    """
    keyboard = [[InlineKeyboardButton(text='Únete al grupo', url='https://t.me/joinchat/KXjmNhHOxvk1NmE0')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Para usar este bot debes estar en el subgrupo de desarrolladores de @EscuelaCryptoES", reply_markup = reply_markup)

def goToMD(update):
    """==== If the bot is called from another place that is not MD, returns this message ====

    Args:
        update (Any): message info state
    """
    update.message.reply_text("Hablame por privado! @escryptoes_bot")

def checkUser(user):
    """==== Check if the user that calls the bot is member of EscuelaCryptoES group ====

    Args:
        user (int): user_id to check

    Returns:
        bool: if user is inside the group
    """
    params = { "chat_id" : keys.GROUP_ID, "user_id" : user, "format" : json }
    response = requests.get("https://api.telegram.org/bot" + keys.API_KEY + "/getChatMember", params=params) #  Get call with params to check it

    return (response.json()["ok"] & (response.json()["result"]["status"] == 'member'))

def start_command(update, context):
    """==== User greeting ====

    Args:
        update (Any): message info state
        context (Any): bot message context
    """
    if(checkUser(update.message.from_user['id'])):
        if update.message.chat['title'] != 'Rinkeby ETH Delivery Group': #  If call is not from MD -> ***
            update.message.reply_text("Hola @"+ update.message.from_user['username'] +", \n¡Bienvenid@ al faucet-bot de EscuelaCryptoES! 😎😁\n\nSi quieres recibir " +  str(keys.REWARD) +" ETH en la red de Rinkeby y empezar a tope a programar, escribe /address y tu dirección de Ethereum a continuación.\nEj: /address 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 (Cambia esta dirección, si no estarás enviando " +  str(keys.REWARD) + " ETH al mismisimo Vitalik Buterin 🤪🤫) \n\n ¡Mucha suerte en tu proyecto!👨‍💻👩‍💻")
        else:
            goToMD(update)
    else:
        keyboardCreate(update)

def help_command(update,context):
    """==== User help to use bot ====

    Args:
        update (Any): message info state
        context (Any): bot message context
    """
    if(checkUser(update.message.from_user['id'])):
        if update.message.chat['title'] != 'Rinkeby ETH Delivery Group': #   ***
            update.message.reply_text("USO:\n\n/address [ETHEREUM_ADDRESS]")
        else:
            goToMD(update)
    else:
        keyboardCreate(update)

def myTurn_command(update,context):
    """==== User turn to request more ETH ====

    Args:
        update (Any): message info state
        context (Any): bot message context
    """
    if(checkUser(update.message.from_user['id'])):
        if update.message.chat['title'] != 'Rinkeby ETH Delivery Group': #   ***
            user = update.message.from_user['username']
            newTime = T.howMuchIsLeft(user)
            update.message.reply_text("Hola @" + user + "\n\n" + newTime)
        else:
            goToMD(update)
    else:
        keyboardCreate(update)

def balance_command(update,context):
    """==== Returns the Smart Contract balance in ETH 2 dec. rounded ====

    Args:
        update (Any): message info state
        context (Any): bot message context
    """
    if(checkUser(update.message.from_user['id'])):
        if update.message.chat['title'] != 'Rinkeby ETH Delivery Group': #   ***
            update.message.reply_text("Balance actual:\n\n" + str(round(T.balance(), 2)) + " ETH")
        else:
            goToMD(update)
    else:
        keyboardCreate(update)

def handle_message(update, context):
    """==== Process user address or message ====

    Args:
        update (Any): message info state
        context (Any): bot message context
    """
    print(update)

    if(checkUser(update.message.from_user['id'])):
        if update.message.chat['title'] != 'Rinkeby ETH Delivery Group': #   ***
            text = str(update.message.text).lower()
            response = R.sample_responses(text) #  Return the processed string

            if len(response) == keys.AVERAGE_ETHEREUM_ADDRESS_LENGTH: #  If input message is an Ethereum address
                user = update.message.from_user['username']
                user_address = response

                update.message.reply_text("Enviando " + str(keys.REWARD) +" ETH de Rinkeby a @" + user)
                transaction_response = T.transaction(user, user_address)

                if transaction_response: #  Transaction state
                    update.message.reply_text("Transacción finalizada, disfruta de tu ETH :)")
                else:
                    newTime = T.howMuchIsLeft(user)
                    update.message.reply_text("Transacción fallida\n\n" + newTime)

            elif response.__contains__("0x"): #  The user try to troll
                update.message.reply_text("¿Me estás vacilando? Escribe tu dirección completa si no te meto en la lista negra")
            else:
                update.message.reply_text(response)
        else:
            goToMD(update)
    else:
        keyboardCreate(update)

def error(update,context):
    """==== Error function ====

    Args:
        update (Any): message info state
        context (Any): bot message context
    """
    print(f"Update {update} caused error {context.error}")

def main():
    """==== Main function ===="""
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    #  Command handler
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("myturn", myTurn_command))
    dp.add_handler(CommandHandler("balance", balance_command))

    #  Message handler
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    
    #  Error handler
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

#  Main function call
if __name__ == "__main__":
    main()