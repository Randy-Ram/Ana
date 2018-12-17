import requests
from config import slack_token, slack_msg_url


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
    resp = requests.post(slack_msg_url, headers=header, json=data)
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


if __name__ == "__main__":
    send_message("Hello Randy", "CEU39H3H8")
