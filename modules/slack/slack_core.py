import requests
from modules.config import slack_token, slack_post_msg_url, slack_post_ephemeral_url
from pprint import pprint

def send_message(channel, message):
    """

    :param message: Message to be sent - text string
    :param channel: Channel to post message
    :return: None
    """
    header = {
        'Authorization': 'Bearer ' + slack_token
    }
    data = {
        "channel": channel,
        "text": message
    }
    resp = requests.post(slack_post_msg_url, headers=header, json=data)
    print(resp.text)


def send_ephemeral_msg(channel, user_id, message, payload=None):
    header = {
        'Authorization': 'Bearer ' + slack_token
    }
    if payload is None:
        data = {
            "channel": channel,
            "attachments": message,
            "user": user_id
        }
    else:
        data = payload
    resp = requests.post(slack_post_ephemeral_url, headers=header, json=data)
    print(resp.text)


def send_response_to_slash_command(response_url, text):
    """
    Method to respond to commands invoked in Slack via a slash "/flist"
    :param response_url: The URL to send the response too
    :param text: The text to send.
    :return:
    """
    text = {
        "text": text
    }
    resp = requests.post(response_url, json=text)
    print(resp.text)


def send_test_response(slack_request):
    payload = {
            "attachments": [
                {
                    "actions": [
                  {
                    "name": 'fload',
                    'text': 'Check flight load',
                    'type': 'button',
                    'value': '281218 526'
                  }],
             'attachment_type': 'default',
             'callback_id': 'fload',
             'fallback': 'Sorry, could not get the flight load. Try running /fload '
                         'manually'
                }],
             'text': '*POS -> JFK*\n'
                     '*BW526*\n'
                     'Dept Time: Fri 28 Dec, 2018 03:15PM\n'
                     'Arrv Time: Fri 28 Dec, 2018 10:25PM\n'
                     '****************************************\n'
                     '\n',
            'channel': 'CEVKRDUET',
            'user': 'UBJUR1S7L'
    }
    # channel = slack_request["channel_id"]
    # user_id = slack_request["user_id"]
    # payload["channel"] = channel
    # payload["user"] = user_id
    send_ephemeral_msg("CEVKRDUET", "UBJUR1S7L", None, payload=payload)


if __name__ == "__main__":
    send_test_response("Hello Randy")
