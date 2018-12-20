"""
'action': 'input.unknown',
 'allRequiredParamsPresent': True,
 'diagnosticInfo': {'webhook_latency_ms': 199.0},
 'fulfillmentMessages': [{'text': {'text': ["I didn't quite get that. Can you "
                                            'say it again, differently?']}}],
 'fulfillmentText': "I don't quite understand. Can you possibly phrase your "
                    'question differently?',
 'intent': {'displayName': 'Default Fallback Intent',
            'isFallback': True,
            'name': 'projects/flights-e717c/agent/intents/65f3db74-38f2-4fb6-9f73-a6ff7e219d15'},
 'intentDetectionConfidence': 1.0,
 'languageCode': 'en',
 'parameters': {},
 'queryText': ' Ltoatoaga'
"""

from modules import models
import traceback


def log_request(df_response):
    user_question = ''
    bot_response = ''
    bot_intent = ''
    bot_action = ''
    detection_confidence = ''
    try:
        session = models.get_pg_session()
        if df_response.get('queryText'):
            user_question = df_response.get('queryText')
        if df_response.get('fulfillmentText'):
            bot_response = df_response.get('fulfillmentText')
        if df_response.get('intent') and df_response['intent'].get('displayName'):
            bot_intent = df_response['intent']['displayName']
        if df_response.get('action'):
            bot_action = df_response['action']
        if df_response.get('intentDetectionConfidence'):
            detection_confidence = df_response['intentDetectionConfidence']
        user_query = models.AnaUserQueries(user_question=user_question,
                                           bot_response=bot_response,
                                           bot_intent=bot_intent,
                                           bot_action=bot_action,
                                           detection_confidence=detection_confidence)
        session.add(user_query)
        session.commit()
        session.close()
    except Exception as e:
        print(traceback.print_exc())
        print("Error logging user question")
