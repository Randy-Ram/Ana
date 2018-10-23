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
        "title": "Flood \U000026C8",
        "type": "nested",
        "call_to_actions": [
                FBAttachment.button_postback("Check Flight Status \U0001F55B", "flight_status"),
                FBAttachment.button_postback("Check-In \U0001F3AB", "check-in"),
                FBAttachment.button_postback("Rent A Car (Cartrawler) \U0001F697", "rent a car"),
                {
                    "title": "Caribbean Miles \U0001F4B3",
                    "type": "nested",
                    "call_to_actions": [
                        FBAttachment.button_postback("Miles Balance \U0001F4CA", "miles balance"),
                        FBAttachment.button_postback("Miles FAQ \U00002753", "what is caribbean miles")
                    ]
                }
            ]
        },
        {
        "title": "Earthquake \U0001F3DA",
        "type": "nested",
        "call_to_actions": [
            FBAttachment.button_postback("Baggage Info \U0001F6C4", "baggage info"),
            FBAttachment.button_postback("Special Services \U0000267F", "I want a wheelchair"),
            FBAttachment.button_postback("Travel Documents \U0001F4C4", "travel documents"),
            FBAttachment.button_postback("Duty Free \U0001F943", "duty free")
        ]},
        {
        "title": "Contact \U0001F4F1",
        "type": "nested",
        "call_to_actions": [
            FBAttachment.button_postback("Speak to Agent \U0001F469", "transfer_request"),
            FBAttachment.button_postback("Contact Reservations Team \U0001F3AB", "book flight"),
            FBAttachment.button_postback("Contact Directory \U0000260E", "contact directory")
        ]}

    ]