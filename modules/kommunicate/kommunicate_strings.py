## whatsapp_bot.py
# DF Request Strings
KOMM_DF_EXCEPTION = "Whatsapp DF handler needs a valid intent"
KOM_NO_FUNCTIONALITY = "I'm sorry. This functionality is not available."

# Whatsapp Handle Request
DF_SENDER_ID = 'kommunicate_'

# Whatsapp Bot
KOM_ERROR_MSG_BODY = "Sorry but it seems I'm having some issues at the moment."


KOM_WELCOME_GREETING = "\U0001F916 - Hi there, I'm Ana. I'm a robot and I'll try to answer any questions you may have. You can type 'menu' to access the below options anytime."
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
        "message": "Caribbean Miles\U0001F4B3"
    },
    {
        "title": "Speak to Agent \U0001F469",
        "message": "Transfer to Agent"
    },
    {
        "title": "Edit Reservation \U0001F3F7",
        "message": "Edit Reservation \U0001F3F7"
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


KOM_MANAGE_BOOKING = 'https://book.bw.amadeus.com/plnext/CaribbeanAirlines/Override.action?REC_LOC={booking_ref}&DIRECT_RETRIEVE_LASTNAME={last_name}&TRIP_FLOW=YES&EMBEDDED_TRANSACTION=RetrievePNR&DIRECT_RETRIEVE=TRUE&SO_SITE_ALLOW_DIRECT_RT=TRUE&SO_SITE_PNR_SERV_REQ_LOGIN=NO&SO_SITE_DISPL_SPECIAL_REQS=TRUE&SO_SITE_ALLOW_PNR_SERV=YES&SO_SITE_ALLOW_PNR_MODIF=Y&SO_SITE_ALLOW_TKT_PNR_MODIF=Y&SO_SITE_RT_SHOW_PRICES=TRUE&SO_SITE_ETKT_VIEW_ENABLED=TRUE&SO_SITE_RT_PRICE_FROM_TST=TRUE&SO_GL=&SO_SITE_OFFICE_ID=MIABW08IB&SO_SITE_QUEUE_OFFICE_ID=MIABW08IB&SO_SITE_QUEUE_CATEGORY=0C0&SO_SITE_POINT_OF_SALE=MIA&LANGUAGE=GB&SO_SITE_MODIFY_OUTSIDE_PNR=TRUE&SERVSTRD_CARRY_OVER=TRUE&SO_SITE_CHANGE_PAST_TRIP=Y&SO_SITE_CHARGEABLE_SEATMAP=TRUE&SO_SITE_MAXIMAL_TIME=D362&SITE=H001H001&EXTERNAL_ID=BOOKING&SO_SITE_CSSR_SVC_POLICY_VER=12.3&SO_SITE_SRV_POLICY_PURC=FALSE&SO_SITE_ENABLE_SRV_POLICY=&SO_SITE_SEATMAP_MODIF=TRUE&SO_SITE_CSSR_CHRG_SEAT_MODIF=TRUE&SO_SITE_NAVIGATION_ENABLED=TRUE&SO_SITE_MIN_AVAIL_DATE_SPAN=H3'