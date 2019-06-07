from ..helpers.attachment import FBAttachment


def get_persistent_menu_buttons():
    # return [
    #     FBAttachment.button_postback("Check Flight Status", "flight_status"),
    #     FBAttachment.button_postback("Check-In", "check-in"),
    #     FBAttachment.button_postback("Baggage Info", "baggage info"),
    #     FBAttachment.button_postback("Call Reservations", "book flight"),
    #     FBAttachment.button_postback("Transfer to Agent", "transfer_request"),
    #     # FBAttachment.button_postback("Itinerary", "itinerary"),
    # ]
    return [
        {
        "title": "Plan and Book \U00002708",
        "type": "nested",
        "call_to_actions": [
                FBAttachment.button_postback("Check Flight Status \U0001F55B", "flight_status"),
                FBAttachment.button_postback("Check-In \U0001F3AB", "check-in"),
                {
                    "title": "Caribbean Miles \U0001F4B3",
                    "type": "nested",
                    "call_to_actions": [
                        FBAttachment.button_postback("Miles Balance \U0001F4CA", "miles balance"),
                        FBAttachment.button_postback("Miles FAQ \U00002753", "what is caribbean miles")
                    ]
                },
                FBAttachment.button_postback("Rent A Car (Cartrawler) \U0001F697", "rent a car")
            ]
        },
        {
        "title": "Travel Info \U00002139",
        "type": "nested",
        "call_to_actions": [
            FBAttachment.button_postback("Flight Notifications \U000023F0", "Caribbean Notifications"),
            FBAttachment.button_postback("Baggage Info \U0001F6C4", "baggage info"),
            FBAttachment.button_postback("Special Services \U0000267F", "I want a wheelchair"),
            FBAttachment.button_postback("Duty Free \U0001F943", "duty free")
        ]},
        {
        "title": "Support \U0001F6CE",
        "type": "nested",
        "call_to_actions": [
            FBAttachment.button_postback("Speak to Agent \U0001F469", "transfer_request"),
            FBAttachment.button_postback("Contact Reservations Team \U0001F3AB", "book flight"),
            FBAttachment.button_postback("Contact Directory \U0000260E", "contact directory")
        ]}

    ]
