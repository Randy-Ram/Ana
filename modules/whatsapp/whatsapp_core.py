from twilio.rest import Client
from modules.config import whatsapp_account_sid, whatsapp_auth_token, whatspp_acc_num
from modules.whatsapp.whatsapp_strings import WHATSAPP_ERROR_MSG_BODY

client = Client(whatsapp_account_sid, whatsapp_auth_token)


def send_message(to_num, message):
    try:
        if not message:
            body = WHATSAPP_ERROR_MSG_BODY
        else:
            body = message
        msg = client.messages.create(body=body, from_=whatspp_acc_num, to=to_num)

    except Exception as err:
        print(err)
        print(message)
