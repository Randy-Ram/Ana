import requests
from modules.config import kommunicate_api_key, kommunicate_bot_id
from pprint import pprint
import json


headers = {"Api-Key": kommunicate_api_key}

send_message_url = "https://services.kommunicate.io/rest/ws/message/v2/send"


def send_text_message(group_id, message):
    try:
        data = {
            "groupId": group_id,
            "message": message,
            "fromUserName": kommunicate_bot_id,
        }
        resp = requests.post(send_message_url, json=data, headers=headers)
        pprint(resp.text)
    except Exception as e:
        pprint(e)


def send_generic_message(data):
    resp = requests.post(send_message_url, json=data, headers=headers)
    pprint(resp.text)


def send_template_message(group_id, message, template_id, payload):
    """

    :param group_id:
    :param message:
    :param template_id: The ID of the template being used, the payload must match the
                        template structure. See docs for more info
                        Buttons - 3
                        QuickReplies - 6
                        Images - 9
                        ListTemplate - 7
                        Card - 10
                        CardCarousel - ?
    :param payload: Payload specific to the template being used.
    :return:
    """
    data = {
        "message": message,
        "groupId": group_id,
        "fromUserName": kommunicate_bot_id,
        "platform": "kommunicate",
        "metadata": {
            "contentType": "300",
            "templateId": template_id,
            "payload": payload,
        },
    }
    resp = requests.post(send_message_url, json=data, headers=headers)
    pprint(resp.text)


def send_message_buttons(message, group_id, payload):
    """

    :param group_id:
    :param message:
    :param payload: A list of
    :return:
    """
    data = {
        "message": message,
        "groupId": group_id,
        "fromUserName": kommunicate_bot_id,
        "platform": "kommunicate",
        "metadata": {"contentType": "300", "templateId": "3", "payload": payload},
    }
    pprint(data)
    send_generic_message(data=data)
    # resp = requests.post(send_message_url, json=data, headers=headers)
    # pprint(resp.text)


def send_quick_reply(group_id, message, payload):
    """

    :param group_id:
    :param payload:
            '''[
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
                "title": "Make Booking \U0001F5A5",
                "message": "Make Booking"
            }
            ]'''
    :return:
    """
    data = {
        "groupId": group_id,
        "fromUserName": kommunicate_bot_id,
        "message": message,
        "platform": "kommunicate",
        "metadata": {"contentType": "300", "templateId": "6", "payload": str(payload)},
    }
    pprint(data)
    send_generic_message(data)


def send_card_message(group_id, message, payload):
    data = {
        "groupId": group_id,
        "fromUserName": kommunicate_bot_id,
        "message": message,
        "platform": "kommunicate",
        "metadata": {"contentType": "300", "templateId": "10", "payload": str(payload)},
    }
    pprint(data)
    send_generic_message(data)


def send_carousel_message(group_id, payload, message):
    data = {
        "message": message,
        "platform": "kommunicate",
        "groupId": group_id,
        "fromUserName": kommunicate_bot_id,
        "metadata": {"contentType": "300", "templateId": "10", "payload": payload},
    }
    pprint(data)
    send_generic_message(data)


def send_message_with_autosuggestion(group_id, payload):
    """
    :param group_id:
    :return:
    """
    data = {
        "groupId": group_id,
        "fromUserName": "ana",
        "platform": "kommunicate",
        "message": "Where are you travelling from?",
        "metadata": payload,
    }
    pprint(data)
    resp = requests.post(send_message_url, json=data, headers=headers)
    pprint(resp.text)


def transfer_to_agent(group_id, message):
    data = {
        "groupId": group_id,
        "message": message,
        "fromUserName": "ana",
        "platform": "kommunicate",
        "metadata": {"KM_ASSIGN_TO": ""},
    }
    pprint(data)
    send_generic_message(data)


if __name__ == "__main__":
    source = [
        {"searchKey": "POS, Port-of-Spain", "message": "POS"},
        {"searchKey": "MIA, Miami International Airport", "message": "MIA"},
        {"searchKey": "JFK, John F. Kennedy, NYC", "message": "JFK"},
        {"searchKey": "YYZ, Toronto", "message": "YYZ"},
        {"searchKey": "BGI, Bridgetown, Barbados", "message": "BGI"},
    ]
    # source = ["London", "Miami", "Port of Spain"]
    placeholder = "Enter City Name"
    payload = {
        "KM_AUTO_SUGGESTION": json.dumps(
            {"placeholder": "Enter City Name", "source": source}
        )
    }
    send_message_with_autosuggestion("16800298", payload)
