from modules.twitter import twitter_core
from modules.dialogflow import df
from modules.helpers.helpers import *
from modules.cal import flight_status, default_responses
from pprint import pprint
from modules.config import df_project_id
from time import sleep
from modules.logger import log_request
from threading import Thread

"""
{'direct_message_events': [{'created_timestamp': '1540561880170',
                            'id': '1055819166702338053',
                            'message_create': {'message_data': {'entities': {'hashtags': [],
                                                                             'symbols': [],
                                                                             'urls': [],
                                                                             'user_mentions': []},
                                                                'text': 'Hi'},
                                               'sender_id': '1053316284375539712',
                                               'target': {'recipient_id': '46435366'}},
                            'type': 'message_create'}],
 'for_user_id': '46435366',
 'users': {'1053316284375539712': {'created_timestamp': '1539965146647',
                                   'followers_count': 1,
                                   'friends_count': 1,
                                   'id': '1053316284375539712',
                                   'name': 'Randy Ram',
                                   'profile_image_url': 'http://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png',
                                   'profile_image_url_https': 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png',
                                   'protected': False,
                                   'screen_name': 'HyperManTT',
                                   'statuses_count': 0,
                                   'verified': False},
           '46435366': {'created_timestamp': '1244740502000',
                        'description': '🇹🇹\xa0Electrical Engineer | Computer '
                                       'Scientist | Head of Software '
                                       'Engineering',
                        'followers_count': 192,
                        'friends_count': 167,
                        'id': '46435366',
                        'location': 'Trinidad and Tobago',
                        'name': 'Randy',
                        'profile_image_url': 'http://pbs.twimg.com/profile_images/1019669603520274433/-dLD2YMH_normal.jpg',
                        'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1019669603520274433/-dLD2YMH_normal.jpg',
                        'protected': False,
                        'screen_name': 'Randy_Ram',
                        'statuses_count': 6823,
                        'verified': False}}}

"""


btn_info = [
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
                    "label": "Speak to an agent",
                    "url": "https://twitter.com/messages/compose?recipient_id=243654400"
                }
            ]


def twitter_get_flight_status(request, session_id):
    """
    Function that gets the flight number and date, sends to CAL's API and returns response to user
    :param request: Request from DF
    :param session_id: User ID to respond too
    :return:
    """
    api_resp = flight_status.fetch_flight_status(request)
    if 'preamble' in api_resp.keys() and api_resp['preamble'] is not None:
        twitter_core.send_dm(session_id, api_resp["preamble"])
        sleep(1)
    for each_flight in api_resp["response_list"]:
            twitter_core.send_dm(session_id, each_flight['msg'])


def twitter_dutyfree(request, session_id):
    btn_info = [
                    {
                        "type": "web_url",
                        "label": "Order Items for Pickup",
                        "url": "https://caribbeanairlinesdutyfree.com/"
                    },
                    {
                        "type": "web_url",
                        "label": "More Info on CAL Duty Free",
                        "url": "https://www.caribbean-airlines.com/#/caribbean-experience/duty-free"
                    }
                ]
    twitter_core.send_text_with_buttons(session_id, "Here you go...", btn_info)


def twitter_miles(request, session_id):
    btn_info = [
        {
            "type": "web_url",
            "label": "Manage Miles Account",
            "url": "https://caribbeanairlines.frequentflyer.aero"
        },
        {
            "type": "web_url",
            "label": "More Info on Caribbean Miles",
            "url": "https://www.caribbean-airlines.com/#/loyalty-programmes/caribbean-miles"
        }
    ]
    twitter_core.send_text_with_buttons(session_id, "Here some useful links regarding Caribbean Miles", btn_info)


def twitter_checkin(request, session_id):
    btn_info = [
        {
            "type": "web_url",
            "label": "Online Check-In",
            "url": "https://checkin.si.amadeus.net/1ASIHSSCWEBBW/sscwbw/checkin"
        }
    ]
    twitter_core.send_text_with_buttons(session_id, "You can click below to checkin online", btn_info)


def twitter_cars(request, session_id):
    btn_info = [
        {
            "type": "web_url",
            "label": "Rent a Car",
            "url": "http://cars.cartrawler.com/caribbeanairlines"
        }
    ]
    twitter_core.send_text_with_buttons(session_id, "We offer car rentals!", btn_info)


def twitter_hotels(request, session_id):
    btn_info = [
        {
            "type": "web_url",
            "label": "Book a Hotel",
            "url": "http://hotels.caribbean-airlines.com"
        }
    ]
    twitter_core.send_text_with_buttons(session_id, "We offer hotel bookings", btn_info)


# The POSITION OF THIS dict MATTERS - BEFORE twitter_handle_df_request and AFTER other functions
intent_mapping = {
    'flight.status': twitter_get_flight_status,
    'faq.dutyfree': twitter_dutyfree,
    'faq.miles_info': twitter_miles,
    'faq.checkin.online': twitter_checkin,
    'faq.cars': twitter_cars,
    'faq.hotels': twitter_hotels,
    'flight.checkin': twitter_checkin
}


def twitter_handle_df_request(request, session_id):
    if 'queryResult' in request and 'intent' in request['queryResult']:
        intent = request['queryResult']['intent']['displayName']
    else:
        raise Exception("Twitter DF handler needs a valid intent")
    # Use intent mapping dict to call function. All functions take the request and the session_id
    if intent in intent_mapping:
        intent_mapping[intent](request, session_id)
    elif intent in default_responses.responses:
        response = default_responses.responses[intent]
        twitter_core.send_dm(session_id, response)
    else:
        twitter_core.send_dm(session_id, "I'm sorry. This functionality is not available.")
        raise Exception(intent + ": Intent not supported")


def twitter_handle_user_request(request):
    """
    :param request: Incoming request from Twitter in JSON format (shown above)
    :return:
    """

    text = request['direct_message_events'][0]['message_create']['message_data']['text']
    sender_id = request['direct_message_events'][0]['message_create']['sender_id']
    df_sender_id = 'twitter_' + sender_id
    ai_json_response = df.detect_intent_texts(df_project_id, df_sender_id, text, "en")
    pprint(ai_json_response)
    # text_to_send = remove_escaped_characters(ai_json_response["result"]["fulfillment"]["speech"])
    if 'fulfillmentText' in ai_json_response:
        text_to_send = remove_escaped_characters(ai_json_response['fulfillmentText'])
        twitter_core.send_dm(sender_id, text_to_send)
        # twitter_core.send_text_with_buttons(sender_id, text_to_send, btn_info)
    if 'action' in ai_json_response and ai_json_response['action'] == "input.unknown":
        thread = Thread(target=log_request, kwargs={'df_response': ai_json_response})
        thread.start()
        # log_request(ai_json_response)
