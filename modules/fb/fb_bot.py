"""
If you're implementing a bot, this is the file that you would
configure the logic of your bot
"""

import config
from ..fb.fb_core import FBBot
from modules.fb.helpers import persistent_menu
from config import df_project_id
from modules.helpers.helpers import *
from modules.dialogflow import df
from pprint import pprint
from modules.cal import flight_status, default_responses, flight_loads
from time import sleep


token = config.facebook_access_token
verify_token = config.verify_token
# app.secret_key = config.secret_key
fb_bot = FBBot(token, verify_token)


def display_sender_action(sender_action, recipient_id):
    """

    :param sender_action: Can be either "typing_on", "typing_off", "mark_seen"
    :param recipient_id: ID of recipient
    :return:
    """
    graph_endpoint = 'https://graph.facebook.com/v2.6/me/messages?access_token={0}'.format(token)
    payload = {
        "recipient": {"id": recipient_id},
        "sender_action": sender_action
    }
    response = fb_bot._send_payload(payload, graph_endpoint)


def configure_bot():
    # Set up the Persistent Menu and the Getting Started Button
    fb_bot.set_persistent_menu(persistent_menu.get_persistent_menu_buttons())
    fb_bot.set_get_started_button("get_started")
    return fb_bot


def handover_request(recipient_id, silent=False):
    print("Handing over request to agent...")
    if not silent:
        FBBot.send_text_message(recipient_id, "One sec, transferring you to an agent for assistance (Response times may vary).")
    pass_thread_endpoint = 'https://graph.facebook.com/v2.6/me/pass_thread_control?access_token={0}'.format(token)
    payload = {
        "recipient": {"id": recipient_id},
        "target_app_id": 263902037430900,
    }
    response = fb_bot._send_payload(payload, pass_thread_endpoint)


def facebook_flight_status(request, session_id):
    api_resp = flight_status.fetch_flight_status(request)
    pprint(api_resp)
    if 'preamble' in api_resp.keys() and api_resp['preamble'] is not None:
        fb_bot.send_text_message(session_id, api_resp["preamble"])
        sleep(1)
    for each_flight in api_resp["response_list"]:
            fb_bot.send_text_message(session_id, each_flight['msg'])


intent_mapping = {
    "flight.status": facebook_flight_status
}


def facebook_handle_df_request(request, session_id):
    if 'queryResult' in request and 'intent' in request['queryResult']:
        intent = request['queryResult']['intent']['displayName']
    else:
        raise Exception("Facebook DF handler needs a valid intent")
    # Use intent mapping dict to call function. All functions take the request and the session_id
    if intent in intent_mapping:
        intent_mapping[intent](request, session_id)
    elif intent in default_responses.responses:
        response = default_responses.responses[intent]
        fb_bot.send_text_message(recipient_id=session_id, text=response)
    else:
        raise Exception(intent + ": Intent not supported")


def facebook_handle_request(sender, text):
    try:
        display_sender_action("typing_on", sender)
        df_sender_id = "facebook_" + sender
        ai_json_response = df.detect_intent_texts(df_project_id, df_sender_id, text, "en")
        pprint(ai_json_response)
        if 'fulfillmentText' in ai_json_response:
            text_to_send = remove_escaped_characters(ai_json_response['fulfillmentText'])
            display_sender_action("typing_off", sender)
            fb_bot.send_text_message(recipient_id=sender, text=text_to_send)
    except Exception:
        # handover_request(sender)
        print("Error")
    finally:
        display_sender_action("typing_off", sender)
