from modules.kommunicate import kommunicate_core
from modules.config import df_project_id
from modules.helpers.helpers import *
from modules.dialogflow import df
from pprint import pprint
from modules.cal import flight_status, default_responses, flight_loads, cal_miles
from time import sleep
from modules.logger import log_request
from modules.kommunicate.kommunicate_strings import *
from threading import Thread
import traceback
from modules.kommunicate.kommunicate_actionable import KommActionableMessages
import json
from modules.kommunicate.kommunicate_faq import *

"""
{
'applicationId': '1bfe0fad3344291b54fd439d73c54542b',
 'botId': 'ana',
 'contentType': 0,
 'createdAt': 1550757013912,
 'from': '9MjplAPFQDVDljsaOMjQZ3Cd6PyvfHqk',
 'groupId': 16650159,
 'key': '5-16650159-1550757013897',
 'message': 'Randy!',
 'metadata': {'KM_CHAT_CONTEXT': '{}'},
 'source': 1
 }
"""


def komm_send_welcome_msg(request, greeting=KOM_WELCOME_GREETING):
    sender_id = request["groupId"]
    payload = []
    for items in KOM_WELCOME_MESSAGES:
        payload.append(KommActionableMessages.quick_reply(items["title"], items["message"]))
    payload = json.dumps(payload)
    pprint(payload)
    kommunicate_core.send_quick_reply(sender_id, greeting, payload)


def komm_transfer_to_agent(request):
    sender_id = request["groupId"]
    kommunicate_core.transfer_to_agent(sender_id, message=KOM_TRANSFER_MESSAGE)


def kom_send_miles_menu(request):
    miles_msg = "What would you like to know about Caribbean Miles?"
    sender_id = request['groupId']
    payload = []
    for items in KOM_MILES_MENU:
        payload.append(KommActionableMessages.quick_reply(items["title"], items["message"]))
    payload = json.dumps(payload)
    pprint(payload)
    kommunicate_core.send_quick_reply(sender_id, miles_msg, payload)


def komm_flight_status(request, session_id):
    api_resp = flight_status.fetch_flight_status(request)
    pprint(api_resp)
    if 'preamble' in api_resp.keys() and api_resp['preamble'] is not None:
        kommunicate_core.send_text_message(session_id, api_resp["preamble"])
        sleep(1)
    for each_flight in api_resp["response_list"]:
            kommunicate_core.send_text_message(session_id, each_flight['msg'])


def komm_flight_loads(request, session_id):
    api_resp = flight_loads.get_flight_loads(request)
    for resp in api_resp:
        kommunicate_core.send_text_message(session_id, resp)


def komm_miles_check(request, session_id):
    api_resp = cal_miles.get_miles(request)
    if api_resp is None:
        kommunicate_core.send_text_message(session_id, "Sorry, I can't seem to get any information for that account.")
    else:
        miles = "{:,}".format(api_resp)
        kommunicate_core.send_text_message(session_id, "Your account currently has {0} miles.".format(str(miles)))


intent_mapping = {
    "flight.status": komm_flight_status,
    "flight.loads": komm_flight_loads,
    "faq.miles_check": komm_miles_check
}

faq_mapping = {
    "faq.baggage": faq_baggage,
    "faq.dutyfree": faq_dutyfree,
    "faq.special_requests": faq_special_requests,
    "faq.miles_info": faq_miles,
    "faq.checkin.online": faq_checkin_online,
    "flight.checkin": faq_checkin_online,
    "faq.cars": faq_rent_car,
    "faq.reservations": faq_reservations,
    "faq.contacts": faq_contacts
}


def komm_handle_df_request(request, session_id):
    # pprint(request)
    if 'queryResult' in request and 'intent' in request['queryResult']:
        intent = request['queryResult']['intent']['displayName']
    else:
        raise Exception(KOMM_DF_EXCEPTION)
    # Use intent mapping dict to call function. All functions take the request and the session_id
    if intent in intent_mapping:
        intent_mapping[intent](request, session_id)
    elif intent in faq_mapping:
        faq_mapping[intent](session_id)
    elif intent in default_responses.responses:
        response = default_responses.responses[intent]
        kommunicate_core.send_text_message(session_id, response)
    else:
        kommunicate_core.send_text_message(session_id, KOM_NO_FUNCTIONALITY)
        raise Exception(intent + ": Intent not supported")


def komm_handle_request(request):
    print(type(request))
    pprint(request)
    try:
        text = request["message"]
        sender_id = request["groupId"]
        pprint(sender_id)
        df_sender_id = DF_SENDER_ID + str(sender_id)
        ai_json_response = df.detect_intent_texts(df_project_id, df_sender_id, text, "en")
        pprint(ai_json_response)
        if 'fulfillmentText' in ai_json_response:
            if 'action' in ai_json_response and ai_json_response['action'] == "input.welcome":
                komm_send_welcome_msg(request)
            else:
                text_to_send = remove_escaped_characters(ai_json_response['fulfillmentText'])
                kommunicate_core.send_text_message(sender_id, text_to_send)
            # twitter_core.send_text_with_buttons(sender_id, text_to_send, btn_info)
        if 'action' in ai_json_response and ai_json_response['action'] == "input.unknown":
            # log_request(ai_json_response)
            thread = Thread(target=log_request, kwargs={'df_response': ai_json_response})
            thread.start()
    except Exception as e:
        traceback.print_exc()


if __name__ == "__main__":
    req = {
        "groupId": '16795351'
    }
    komm_send_welcome_msg(req)
