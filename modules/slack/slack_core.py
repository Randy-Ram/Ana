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
        "text": "Would you like to play a game?",
        # "response_type": "in_channel",
        "attachments": [
            {
                "text": "Choose a game to play",
                "fallback": "If you could read this message, you'd be choosing something fun to do right now.",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "callback_id": "game_selection",
                "actions": [
                    {
                        "name": "games_list",
                        "text": "Pick a game...",
                        "type": "select",
                        "options": [
                            {
                                "text": "Hearts",
                                "value": "hearts"
                            },
                            {
                                "text": "Bridge",
                                "value": "bridge"
                            },
                            {
                                "text": "Checkers",
                                "value": "checkers"
                            },
                            {
                                "text": "Chess",
                                "value": "chess"
                            },
                            {
                                "text": "Poker",
                                "value": "poker"
                            },
                            {
                                "text": "Falken's Maze",
                                "value": "maze"
                            },
                            {
                                "text": "Global Thermonuclear War",
                                "value": "war"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    channel = slack_request["channel_id"]
    user_id = slack_request["user_id"]
    payload["channel"] = channel
    payload["user"] = user_id
    send_ephemeral_msg(channel, user_id, None, payload=payload)


if __name__ == "__main__":
    send_message("Hello Randy", "CEU39H3H8")
