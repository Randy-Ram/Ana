import dialogflow_v2 as dialogflow
import os
from pprint import pprint

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.getcwd(), "Flights-2d3067c2af02.json")

# print(config.GOOGLE_APPLICATION_CREDENTIALS)

"""
{'originalDetectIntentRequest': {'payload': {}},
 'queryResult': {'action': 'flight.check',
                 'allRequiredParamsPresent': True,
                 'fulfillmentMessages': [{'text': {'text': ['']}}],
                 'intent': {'displayName': 'flight.status',
                            'name': 'projects/flights-e717c/agent/intents/1cac474e-e32f-465d-8712-594226e5baae'},
                 'intentDetectionConfidence': 0.88,
                 'languageCode': 'en',
                 'outputContexts': [{'lifespanCount': 3,
                                     'name': 'projects/flights-e717c/agent/sessions/75268246-869c-854a-0c4d-50bebfe86a05/contexts/check-flight',
                                     'parameters': {'airline': '',
                                                    'airline.original': '',
                                                    'airport': [],
                                                    'airport.original': '',
                                                    'airport_from': '',
                                                    'airport_from.original': '',
                                                    'airport_to': '',
                                                    'airport_to.original': '',
                                                    'date': '2018-10-30T12:00:00-04:00',
                                                    'date.original': 'tomorrow',
                                                    'flight-number': 'BW 525',
                                                    'flight-number.original': 'BW '
                                                                              '525',
                                                    'from': '',
                                                    'from.original': '',
                                                    'to': '',
                                                    'to.original': ''}}],
                 'parameters': {'airline': '',
                                'airport': [],
                                'airport_from': '',
                                'airport_to': '',
                                'date': '2018-10-30T12:00:00-04:00',
                                'flight-number': 'BW 525',
                                'from': '',
                                'to': ''},
                 'queryText': 'what is the flight status of BW 525 tomorrow'},
 'responseId': 'e87bd064-6864-4626-aa12-732c1b62df15',
"""


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        pprint(response.query_result)
        return response.query_result.fulfillment_text


if __name__ == "__main__":
    pprint(detect_intent_texts('flights-e717c', "twitter_e87bd064-6864-4626-aa12-732c1b62df15",
                               "What is the status of flight BW600 tomorrow?", "en"))
