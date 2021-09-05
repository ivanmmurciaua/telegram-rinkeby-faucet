#from web3.middleware import geth_poa_middleware
from web3 import Web3
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

    tx = contract_instance.functions.refundUser(
        telegram_user,
        web3.toChecksumAddress(address_to)
        ).buildTransaction({
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
    print(txn_receipt)

    #response
    if txn_receipt.status:
        print("\n\n\n\nTransacción completada")
        return True
    else:
        print("\n\n\n\nTransacción fallida")
        return False