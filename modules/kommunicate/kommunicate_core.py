import requests
from modules.config import kommunicate_api_key
from pprint import pprint


headers = {
    "Api-Key": kommunicate_api_key
}

send_message_url = 'https://services.kommunicate.io/rest/ws/message/v2/send'


def send_text_message(group_id, message):
    try:
        data = {
            "groupId": group_id,
            "message": message,
            "fromUserName": "ana"
        }
        resp = requests.post(send_message_url, json=data,  headers=headers)
        pprint(resp.text)
    except Exception as e:
        pprint(e)


def send_message_with_buttons(group_id, message):
    data = {
        "message": message,
        "group_id": group_id,
        "platform": "kommunicate",
        "metadata": {
            "contentType": "300",
            "templateId": "3",
            "payload": [{
                    "type": "link",
                    "url": "https://www.google.com",
                    "name": "Go To Google"
                },
                {
                    "type": "link",
                    "url": "https://www.facebook.com",
                    "name": "Go To Facebook",
                    "openLinkInNewTab": False
                }
            ]
        }
    }
    resp = requests.post(send_message_url, json=data, headers=headers)
    pprint(resp.text)


def send_message_with_autosuggestion(group_id):
    """
    :param group_id:
    :return:
    """
    data = {
        "groupId": "16650159",
        "fromUserName": "ana",
        "platform": "kommunicate",
        "metadata": {
            "KM_AUTO_SUGGESTION": {
                "placeholder": "enter city name",
                "source": ["POS", "JFK", "ANU"]
            }
       }
    }
    resp = requests.post(send_message_url, json=data, headers=headers)
    pprint(resp.text)


if __name__ == "__main__":
    # send_text_message('16650159', 'Greetings! How can I assist?')
    send_message_with_autosuggestion('16650159')
    # send_message_with_buttons('16650159', "Click below")
