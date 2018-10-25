import os
import sys
import config
from pprint import pprint
import json
import config

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = config.dialogflow_access_token


def get_ai_handle():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'en'  # optional, default value equal 'en'
    request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
    return request


def send_text_query(request, text):
    request.query = text
    response = request.getresponse()
    return json.loads(response.read().decode("utf-8"))


def ai_instantiate_and_get_response(text, sender_id):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'en'  # optional, default value equal 'en'
    request.session_id = sender_id
    request.query = text
    response = request.getresponse()
    # pprint(json.loads(response.read().decode("utf-8")))
    return json.loads(response.read().decode("utf-8"))


if __name__ == '__main__':
    print(ai_instantiate_and_get_response("Hi"))
