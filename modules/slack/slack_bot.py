from config import df_project_id
from modules.helpers.helpers import *
from modules.dialogflow import df
from pprint import pprint
from modules.cal import flight_status, default_responses, flight_loads
from modules.slack import slack_core
from time import sleep

'''
{'api_app_id': 'AEVF2N5EJ',
 'authed_users': ['UEU3DE71Q'],
 'event': {'channel': 'CEU39H3H8',
           'client_msg_id': 'e8c6aeca-f9c3-4f9b-b908-72416eeaa896',
           'event_ts': '1544796095.001600',
           'text': '<@UEU3DE71Q> hello',
           'ts': '1544796095.001600',
           'type': 'app_mention',
           'user': 'UBJUR1S7L'},
 'event_id': 'EvETUWT08L',
 'event_time': 1544796095,
 'team_id': 'TBJN6RCRJ',
 'token': 'wVvpIhSl9dAz89dMmevnPuAR',
 'type': 'event_callback'}
'''


def slack_flight_status(request, session_id):
    api_resp = flight_status.fetch_flight_status(request)
    pprint(api_resp)
    if 'preamble' in api_resp.keys() and api_resp['preamble'] is not None:
        slack_core.send_message(session_id, api_resp["preamble"])
        sleep(1)
    for each_flight in api_resp["response_list"]:
            slack_core.send_message(session_id, each_flight['msg'])


def slack_flight_loads(request, session_id):
    api_resp = flight_loads.get_flight_loads(request)
    pprint(api_resp)
    for resp in api_resp:
        slack_core.send_message(session_id, resp)


intent_mapping = {
    "flight.loads": slack_flight_loads,
    "flight.status": slack_flight_status
}


def slack_handle_df_request(request, session_id):
    if 'queryResult' in request and 'intentDetectionConfidence' in request['queryResult']:
        if request['queryResult']['intentDetectionConfidence'] < 0.75:
            slack_core.send_message(session_id, "I'm sorry, your request is vague. "
                                                "Can you please be more specific about what you want?")
            return
    if 'queryResult' in request and 'intent' in request['queryResult']:
        intent = request['queryResult']['intent']['displayName']
    else:
        raise Exception("Slack DF handler needs a valid intent")
    # Use intent mapping dict to call function. All functions take the request and the session_id
    if intent in intent_mapping:
        intent_mapping[intent](request, session_id)
    elif intent in default_responses.responses:
        response = default_responses.responses[intent]
        slack_core.send_message(session_id, response)
    else:
        raise Exception(intent + ": Intent not supported")


def slack_handle_request(request):
    pprint(request)
    text = request['event']['text']
    if '<@UEU3DE71Q>' in text:
        text = text.replace('<@UEU3DE71Q>', '')
    sender_id = request['event']['channel']
    df_sender_id = 'slack_' + sender_id
    ai_json_response = df.detect_intent_texts(df_project_id, df_sender_id, text, "en")
    pprint(ai_json_response)
    # text_to_send = remove_escaped_characters(ai_json_response["result"]["fulfillment"]["speech"])
    if 'fulfillmentText' in ai_json_response:
        text_to_send = remove_escaped_characters(ai_json_response['fulfillmentText'])
        slack_core.send_message(sender_id, text_to_send)
