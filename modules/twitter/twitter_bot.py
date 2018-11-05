from modules.twitter import twitter_core
from modules.dialogflow import nlp
from modules.helpers.helpers import *

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


def twt_get_flight_status(request):
    pass


def twt_handle_request(request):
    """
    :param request: Incoming request from Twitter in JSON format (shown above)
    :return:
    """

    text = request['direct_message_events'][0]['message_create']['message_data']['text']
    sender_id = request['direct_message_events'][0]['message_create']['sender_id']
    ai_json_response = nlp.ai_instantiate_and_get_response(text, sender_id)
    # pprint(ai_json_response)
    text_to_send = remove_escaped_characters(ai_json_response["result"]["fulfillment"]["speech"])
    # twitter_core.send_dm(sender_id, text_to_send)
    twitter_core.send_text_with_buttons(sender_id, text_to_send, btn_info)