from datetime import date, datetime
from re import split

import constants as keys

def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message.__contains__("/address"):
        address = split("/address ", user_message)[1]
        return address
        
    if user_message in ("gracias","Gracias","GRACIAS","thx","Thx","Thanks","Grazie"):
      return "A ti crack"
    
    return "Escribe tu dirección de Ethereum para recibir " + keys.REWARD + " ETH en Rinkeby"