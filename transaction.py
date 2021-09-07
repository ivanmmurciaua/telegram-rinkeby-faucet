#from web3.middleware import geth_poa_middleware
from web3 import Web3
from re import split
from datetime import datetime, timedelta

import constants as keys

def transaction(telegram_user, address_to):

    web3 = Web3(Web3.HTTPProvider(keys.RINKEBY_URL))
    #web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    #from
    account_1 = keys.PUBLIC_ADDRESS
    private_key1 = keys.PRIVATE_KEY

    #contract conf
    contract_address = keys.CONTRACT_ADDRESS
    abi = keys.ABI
    contract_instance = web3.eth.contract(address=contract_address, abi=abi)

    #get the nonce.  Prevents one from sending the transaction twice
    nonce = web3.eth.getTransactionCount(account_1)

    tx = contract_instance.functions.payUser(
        telegram_user,
        web3.toChecksumAddress(address_to)
        ).buildTransaction({
        'from' : account_1,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei')
    })

    #sign the transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_key1)

    #send transaction
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

    #get transaction hash
    print(web3.toHex(tx_hash))

    #waiting for transaction
    txn_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    #response
    if txn_receipt.status:
        print("\n\n\n\nTransacción completada")
        return True
    else:
        print("\n\n\n\nTransacción fallida")
        return False

def howMuchIsLeft(telegram_user):

    web3 = Web3(Web3.HTTPProvider(keys.RINKEBY_URL))

    #contract conf
    contract_address = keys.CONTRACT_ADDRESS
    abi = keys.ABI
    contract_instance = web3.eth.contract(address=contract_address, abi=abi)

    tx = contract_instance.functions.seeMyInfo(telegram_user).call()

    if tx[3] == 0:
        return ('No estás registrado aún. Consigue tu ETH ya!')

    else:
        fecha1 = datetime.utcnow()
        fecha2 = datetime.utcfromtimestamp(tx[3])
        diferencia = fecha2 - fecha1

        dias = diferencia.days
        horas = int(split(":", str(timedelta(seconds = diferencia.seconds)))[0])
        minutos = int(split(":", str(timedelta(seconds = diferencia.seconds)))[1])
        segundos = int(split(":", str(timedelta(seconds = diferencia.seconds)))[2])

        if ( dias < 0 ):
            return("El tiempo de espera acabó. Pide tu ETH diario ya! 😎")
        else:
            if(dias != 1):
                return ("Podrás volver a pedir " + keys.REWARD + " ETH en " + str(dias) + " días, " + str(horas) + " horas, " + str(minutos) + " minutos y " + str(segundos) + " segundos.")
            else:
                return ("Podrás volver a pedir " + keys.REWARD +" ETH en " + str(dias) + " día, " + str(horas) + " horas, " + str(minutos) + " minutos y " + str(segundos) + " segundos.")

def balance():
    web3 = Web3(Web3.HTTPProvider(keys.RINKEBY_URL))
    return web3.fromWei(web3.eth.get_balance(keys.CONTRACT_ADDRESS), 'ether')