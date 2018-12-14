from twilio.rest import Client
import twilio

account_sid = 'ACca18028c19aa159322f34a632f8e2082'
auth_token = 'fa9f053a869cba6cba2d96cda10d79d9'
whatspp_acc_num = 'whatsapp:+14155238886'

client = Client(account_sid, auth_token)


def send_message(to_num, message):
    try:
        if not message:
            body = "Sorry but it seems I'm having some issues at the moment."
        msg = client.messages.create(
                                      body=message,
                                      from_=whatspp_acc_num,
                                      to=to_num
                                  )

    except Exception as err:
        print(err)
        print(message)
