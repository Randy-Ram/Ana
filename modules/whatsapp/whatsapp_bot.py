from modules.whatsapp import whatsapp_core
from modules.config import df_project_id
from modules.helpers.helpers import *
from modules.dialogflow import df
from pprint import pprint
from modules.cal import flight_status, default_responses, flight_loads
from time import sleep
from modules.logger import log_request, log_error
from threading import Thread
from modules.whatsapp.whatsapp_strings import *

"""
{'AccountSid': 'ACca18028c19aa159322f34a632f8e2082',
 'ApiVersion': '2010-04-01',
 'Body': 'Hello',
 'From': 'whatsapp:+18683907015',
 'MessageSid': 'SMc2adf0e56efaf380a1a632e032c79854',
 'NumMedia': '0',
 'NumSegments': '1',
 'SmsMessageSid': 'SMc2adf0e56efaf380a1a632e032c79854',
 'SmsSid': 'SMc2adf0e56efaf380a1a632e032c79854',
 'SmsStatus': 'received',
 'To': 'whatsapp:+14155238886'}
"""


def whatsapp_flight_status(request, session_id):
    api_resp = flight_status.fetch_flight_status(request)
    pprint(api_resp)
    if 'preamble' in api_resp.keys() and api_resp['preamble'] is not None:
        whatsapp_core.send_message(session_id, api_resp["preamble"])
        sleep(1)
    for each_flight in api_resp["response_list"]:
            whatsapp_core.send_message(session_id, each_flight['msg'])


def whatsapp_flight_loads(request, session_id):
    api_resp = flight_loads.get_flight_loads(request)
    for resp in api_resp:
        whatsapp_core.send_message(session_id, resp)


intent_mapping = {
    "flight.status": whatsapp_flight_status,
    "flight.loads": whatsapp_flight_loads
}


def whatsapp_handle_df_request(request, session_id):
    if 'queryResult' in request and 'intent' in request['queryResult']:
        intent = request['queryResult']['intent']['displayName']
    else:
        raise Exception(WHATSAPP_DF_EXCEPTION)
    # Use intent mapping dict to call function. All functions take the request and the session_id
    if intent in intent_mapping:
        intent_mapping[intent](request, session_id)
    elif intent in default_responses.responses:
        response = default_responses.responses[intent]
        whatsapp_core.send_message(session_id, response)
    else:
        whatsapp_core.send_message(session_id, WHATSAPP_NO_FUNCTIONALITY)
        log_error(f"{intent}: Intent not supported")
        raise Exception(intent + ": Intent not supported")


def whatsapp_handle_request(request):
    text = request['Body']
    sender_id = request['From']
    df_sender_id = DF_SENDER_ID + sender_id
    ai_json_response = df.detect_intent_texts(df_project_id, df_sender_id, text, "en")
    pprint(ai_json_response)
    # text_to_send = remove_escaped_characters(ai_json_response["result"]["fulfillment"]["speech"])
    if 'fulfillmentText' in ai_json_response:
        text_to_send = remove_escaped_characters(ai_json_response['fulfillmentText'])
        whatsapp_core.send_message(sender_id, text_to_send)
        # twitter_core.send_text_with_buttons(sender_id, text_to_send, btn_info)
    if 'action' in ai_json_response and ai_json_response['action'] == "input.unknown":
        # log_request(ai_json_response)
        thread = Thread(target=log_request, kwargs={'df_response': ai_json_response, 'err_type': 'unknown'})
        thread.start()
