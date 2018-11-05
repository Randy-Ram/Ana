from pprint import pprint

intent_mapping = {
    'facebook_flight.status': '',
    'twitter_flight.status': ''
}


def handle_request(request):
    intent = None
    session = None
    # extract intent
    if 'queryResult' in request and 'intent' in request['queryResult']:
        intent = request['queryResult']['intent']['displayName']
    # extract session
    if 'session' in request:
        session = request['session']
    pprint(request.json)
