## whatsapp_bot.py
# DF Request Strings
KOMM_DF_EXCEPTION = "Whatsapp DF handler needs a valid intent"
KOM_NO_FUNCTIONALITY = "I'm sorry. This functionality is not available."

# Whatsapp Handle Request
DF_SENDER_ID = 'kommunicate_'

# Whatsapp Bot
KOM_ERROR_MSG_BODY = "Sorry but it seems I'm having some issues at the moment."


KOM_WELCOME_GREETING = "Hey there, how can I help you? You can type 'menu' to access " \
                       "the below options anytime."
KOM_WELCOME_MESSAGES = [
    {
        "title": "Check In \U0001F3AB",
        "message": "Check In "
    },
    {
        "title": "Flight Status \U0001F55B",
        "message": "Flight Status"
    },
    {
        "title": "Baggage Info \U0001F6C4",
        "message": "Baggage Info"
    },
    {
        "title": "Caribbean Miles \U0001F4B3",
        "message": "Caribbean Miles"
    },
    {
        "title": "Speak to Agent \U0001F469",
        "message": "Transfer to Agent"
    }
]

KOM_TRANSFER_MESSAGE = "Transferring Chat. Our agents will get back to you shortly."

KOM_MILES_MENU = [
    {
        "title": "Miles Balance \U0001F4CA",
        "message": "Miles Balance"
    },
    {
        "title": "Miles FAQ \U00002753",
        "message": "What is Caribbean Miles?"
    }
]
