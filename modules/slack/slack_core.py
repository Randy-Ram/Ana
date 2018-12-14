import requests
slack_msg_url = 'https://slack.com/api/chat.postMessage'
slack_token = "xoxb-392754862868-504115483058-FNqBktO5XNQrjVTsb4kdfYbt"


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


if __name__ == "__main__":
    send_slack_message("Hello Randy", "CEU39H3H8")
