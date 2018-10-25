from config import twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret
from TwitterAPI import TwitterAPI
import json
from pprint import pprint

#User ID: 46435366
#Fake ID: 1053316284375539712

# auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
# auth.set_access_token(twitter_access_token, twitter_access_token_secret)
#
# api = tweepy.API(auth)

twt_bot = TwitterAPI(twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret)


def configure_bot():
    return


def send_dm():
    user_id = '1053316284375539712'
    message_text = 'Sorry, was testing something!'

    event = {
        "event": {
            "type": "message_create",
            "message_create": {
                "target": {
                "recipient_id": user_id
                },
                "message_data": {
                    "text": message_text
                }
            }
        }
    }

    r = twt_bot.request('direct_messages/events/new', json.dumps(event))
    print('SUCCESS' if r.status_code == 200 else 'PROBLEM: ' + r.text)


def send_welcome_message():
    user_id = '1053316284375539712'
    wm_params = {
        "send_welcome_message": {
            "message_data": {
                "text": "Hi! What can I do for you today?",
                "quick_reply": {
                    "type": "options",
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
                        },
                        {
                            "label": "Change Order",
                            "description": "Update or cancel an order recently placed.",
                            "metadata": "external_id_3"
                        },
                        {
                            "label": "Talk to a Human",
                            "description": "Talk with a customer service agent.",
                            "metadata": "external_id_4"
                        }
                    ]
                }
            }
        }
    }
    resp = twt_bot.request('direct_messages/welcome_messages/new', json.dumps(wm_params))
    pprint(resp.json())
    print('SUCCESS' if resp.status_code == 200 else 'PROBLEM: ' + resp.text)


def tweet():
    TWEET_TEXT = 'Testing from Python API'
    r = twt_bot.request('statuses/update', {'status': TWEET_TEXT})
    print('SUCCESS' if r.status_code == 200 else 'PROBLEM: ' + r.text)


def get_user_id():
    SCREEN_NAME = 'HyperManTT'
    r = twt_bot.request('users/lookup', {'screen_name': SCREEN_NAME})
    print(r.json()[0]['id'] if r.status_code == 200 else 'PROBLEM: ' + r.text)


def create_webhook():
    query_param = {
        "url": "https://10ae46de.ngrok.io/twitter"
    }
    r = twt_bot.request('account_activity/all/:%s/webhooks' % ("development"), params=query_param)
    print(r.json())


def get_webhooks():
    r = twt_bot.request('account_activity/all/webhooks')
    pprint(r.json())


def add_subscription():
    r = twt_bot.request('account_activity/all/:%s/subscriptions' % ("development"), method_override="POST")
    pprint(r.response.status_code)


def get_subscriptions():
    r = twt_bot.request('account_activity/all/:%s/subscriptions/all/list' % ("development"))
    print(r.json())


def trigger_crc():
    r = twt_bot.request("account_activity/all/:%s/webhooks/:%s" % ("development", "1055127917909475329"), method_override="PUT")
    pprint(r.response.status_code)


def get_welcome_messages():
    r = twt_bot.request('direct_messages/welcome_messages/list')
    pprint(r.json())


def delete_welcome_message(id):
    payload = {
        'id': id
    }
    r = twt_bot.request('direct_messages/welcome_messages/destroy', params=payload)
    pprint(r.status_code)


def send_options():
    id = '1053316284375539712'
    event = {
        "event": {
            "type": "message_create",
            "message_create": {
                "target": {
                    "recipient_id": id
                },
                "message_data": {
                    "text": "Hi, how can I help you?",
                    "quick_reply": {
                        "type": "options",
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
                            },
                            {
                                "label": "Change Order",
                                "description": "Update or cancel an order recently placed.",
                                "metadata": "external_id_3"
                            },
                            {
                                "label": "Talk to a Human",
                                "description": "Talk with a customer service agent.",
                                "metadata": "external_id_4"
                            }
                        ]
                    }
                }
            }
        }
    }
    r = twt_bot.request('direct_messages/events/new', json.dumps(event))
    print('SUCCESS' if r.status_code == 200 else 'PROBLEM: ' + r.text)


if __name__ == "__main__":
    # tweet()
    # send_dm()
    # get_user_id()
    # send_options()
    # send_welcome_message()
    # create_webhook()
    # delete_welcome_message("1055188637325946884")
    get_welcome_messages()
    # get_webhooks()
    # add_subscription()
    # get_subscriptions()
    # trigger_crc()
