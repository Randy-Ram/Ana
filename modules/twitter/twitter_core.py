import base64
import hashlib
import hmac
from modules.config import (
    twitter_consumer_key,
    twitter_consumer_secret,
    twitter_access_token,
    twitter_access_token_secret,
)
from TwitterAPI import TwitterAPI
import json
from pprint import pprint

# python3 -m modules.twitter.twitter_core

twt_bot = TwitterAPI(
    twitter_consumer_key,
    twitter_consumer_secret,
    twitter_access_token,
    twitter_access_token_secret,
)

ENV_NAME = "development"


def webhook_challenge(request):
    # creates HMAC SHA-256 hash from incoming token and your consumer secret
    # encoded_secret = twitter_consumer_secret.encode("utf-8")
    sha256_hash_digest = hmac.new(
        twitter_consumer_secret.encode("utf-8"),
        msg=request.args.get("crc_token").encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    # construct response data with base64 encoded hash
    response = {
        "response_token": "sha256="
        + base64.b64encode(sha256_hash_digest).decode("ascii")
    }

    # returns properly formatted json response
    print(response)
    return json.dumps(response)


def configure_bot():
    return


def send_dm(user_id, message_text):
    print("SENDING DM: " + message_text)
    print(user_id)
    event = {
        "event": {
            "type": "message_create",
            "message_create": {
                "target": {"recipient_id": user_id},
                "message_data": {"text": message_text},
            },
        }
    }

    r = twt_bot.request("direct_messages/events/new", json.dumps(event))
    pprint(r.json())
    return "SUCCESS" if r.status_code == 200 else "PROBLEM: " + r.text


def create_welcome_message():
    """
    To fix, not currently working
    :return:
    """
    user_id = "1053316284375539712"
    wm_params = {
        "welcome_message": {
            "message_data": {
                "text": "Hi! What can I do for you today?",
                "quick_reply": {
                    "type": "options",
                    "options": [
                        {
                            "label": "Flight Status",
                            "description": "Check the status of a flight",
                            "metadata": "external_id_1",
                        },
                        {
                            "label": "Check In",
                            "description": "Check in for flight.",
                            "metadata": "external_id_2",
                        },
                        {
                            "label": "Baggage Info",
                            "description": "Info about baggage policies",
                            "metadata": "external_id_3",
                        },
                        {
                            "label": "Talk to a Human",
                            "description": "Talk with a customer service agent.",
                            "metadata": "external_id_4",
                        },
                    ],
                },
            }
        }
    }
    resp = twt_bot.request(
        "direct_messages/welcome_messages/new", json.dumps(wm_params)
    )
    pprint(resp.json())
    print("SUCCESS" if resp.status_code == 200 else "PROBLEM: " + resp.text)


def tweet(message_text):
    r = twt_bot.request("statuses/update", {"status": message_text})
    print("SUCCESS" if r.status_code == 200 else "PROBLEM: " + r.text)


def get_user_id_from_screen_name(screen_name):
    r = twt_bot.request("users/lookup", {"screen_name": screen_name})
    pprint(r.json())
    print(r.json()[0]["id"] if r.status_code == 200 else "PROBLEM: " + r.text)


def create_webhook(endpoint):
    query_param = {"url": endpoint}
    r = twt_bot.request(
        "account_activity/all/:%s/webhooks" % ENV_NAME, params=query_param
    )
    print(r.json())


def get_webhooks():
    r = twt_bot.request("account_activity/all/webhooks")
    # pprint(r.json())
    return r.json()


def add_subscription():
    r = twt_bot.request(
        "account_activity/all/:%s/subscriptions" % ENV_NAME, method_override="POST"
    )
    print("Subscription Addition Response: ")
    pprint(r.response.status_code)


def get_all_subscriptions():
    twt_bot2 = TwitterAPI(
        twitter_consumer_key,
        twitter_consumer_secret,
        twitter_access_token,
        twitter_access_token_secret,
        auth_type="oAuth2",
    )
    r = twt_bot2.request("account_activity/all/:%s/subscriptions/list" % ENV_NAME)
    # r = twt_bot.request('account_activity/all/:%s/subscriptions/list' % ENV_NAME,  method_override='GET')
    print(r.json())


def trigger_crc(webhook_id):
    r = twt_bot.request(
        "account_activity/all/:%s/webhooks/:%s" % (ENV_NAME, webhook_id),
        method_override="PUT",
    )
    pprint(r.response.status_code)


def get_welcome_messages():
    r = twt_bot.request("direct_messages/welcome_messages/list")
    pprint(r.json())


def get_welcome_message_by_id(id):
    r = twt_bot.request(
        "direct_messages/welcome_messages/rules/show", params={"id": id}
    )
    print(r.json())


def get_welcome_message_rules():
    r = twt_bot.request("direct_messages/welcome_messages/rules/list")
    pprint(r.json())


def set_welcome_message_rules(id):
    event = {"welcome_message_rule": {"welcome_message_id": id}}
    r = twt_bot.request("direct_messages/welcome_messages/rules/new", json.dumps(event))
    pprint(r.json())


def delete_welcome_message(id):
    payload = {"id": id}
    r = twt_bot.request("direct_messages/welcome_messages/destroy", params=payload)
    pprint(r.status_code)


def send_options(sender_id, options):
    """
    :param options: Should be a list with dicts inside:
     "options": [
                            {
                                "label": "Order Status",
                                "description": "Check the status of an order recently placed.",
                                "metadata": "external_id_1"
                            },
                            {
                                "label": "Return",
                                "description": "Return a product you received less than 30 days ago.",
                                "metadata": "external_id_2"
                            }

    :return:
    """
    id = "1053316284375539712"
    event = {
        "event": {
            "type": "message_create",
            "message_create": {
                "target": {"recipient_id": sender_id},
                "message_data": {
                    "text": "Hi, how can I help you?",
                    "quick_reply": {"type": "options", "options": options},
                },
            },
        }
    }
    r = twt_bot.request("direct_messages/events/new", json.dumps(event))
    print("SUCCESS" if r.status_code == 200 else "PROBLEM: " + r.text)


def change_endpoints(new_endpoint, delete=False):
    twt_bot2 = TwitterAPI(
        twitter_consumer_key,
        twitter_consumer_secret,
        twitter_access_token,
        twitter_access_token_secret,
        auth_type="oAuth2",
    )
    current_webhooks = get_webhooks()
    if "environments" in current_webhooks:
        curr_id = current_webhooks["environments"][0]["webhooks"][0]["id"]
        r = twt_bot2.request(
            "account_activity/all/:%s/webhooks/:%s" % (ENV_NAME, curr_id)
        )
        print(f"Status {r.status_code}")
        if delete:
            return
        create_webhook(new_endpoint)
        add_subscription()


def send_text_with_buttons(sender_id, text, btn_info):
    """

    :param text: Message to be sent
    :param btn_info: Must be in the form
                 [
                    {
                        "type": "web_url",
                        "label": "See flight details",
                        "url": "https://www.google.com"
                    },
                    {
                        "type": "web_url",
                        "label": "Map it",
                        "url": "https://www.google.com"
                    },
                    {
                        "type": "web_url",
                        "label": "Visit MyAirline.domain",
                        "url": "https://www.google.com"
                    }
                ]
    :return:
    """
    event = {
        "event": {
            "type": "message_create",
            "message_create": {
                "target": {"recipient_id": sender_id},
                "message_data": {"text": text, "ctas": btn_info},
            },
        }
    }
    r = twt_bot.request("direct_messages/events/new", json.dumps(event))
    print("SUCCESS" if r.status_code == 200 else "PROBLEM: " + r.text)


if __name__ == "__main__":
    # tweet()
    # send_dm('1053316284375539712', "Hello")
    # get_user_id()
    # send_options()
    # create_welcome_message()
    # create_webhook("https://rram.ngrok.io/twitter")
    # delete_welcome_message("1055843962479620100")  #1055843962479620100
    # get_welcome_messages()
    # get_welcome_message_by_id("1055844711917862917")
    # set_welcome_message_rules('1055844711917862917')
    # get_welcome_message_rules()
    # pprint(get_webhooks())

    # change_endpoints("https://test.test.com/twitter", delete=True)
    # change_endpoints("https://bot.caribbean-airlines.com/twitter")
    pprint(get_webhooks())
    add_subscription()
    get_all_subscriptions()
    # trigger_crc("1073660905299329032")
    # get_user_id_from_screen_name("HyperManTT")  # 243654400
    """
    Changing webhooks involves the following:
    - Run change_endpoint function
    - Run get_webhooks to see new webhook id
    - trigger CRC with new webhook id
    - Add subscription
    - View added subscription   
    """
