from pprint import pprint
from modules.twitter.twitter_bot import twitter_handle_df_request
from modules.whatsapp.whatsapp_bot import whatsapp_handle_df_request
from modules.fb.fb_bot import facebook_handle_df_request
from modules.slack.slack_bot import slack_handle_df_request
from modules.kommunicate.kommunicate_bot import  komm_handle_df_request

# intent_mapping = {
#     'facebook_flight.status': '',
#     'twitter_flight.status': twitter_get_flight_status
# }

service_handlers = {
    'facebook': facebook_handle_df_request,
    'twitter': twitter_handle_df_request,
    'whatsapp': whatsapp_handle_df_request,
    'slack': slack_handle_df_request,
    'kommunicate': komm_handle_df_request
}


def get_platform_and_session_id(session):
    if "/" not in session:
        raise Exception("Session must contain '/' and '_'")
    session_split = session.split("/")
    data = session_split[len(session_split) - 1]
    data_split = data.split("_")
    print(data_split)
    return data_split[0].lower(), data_split[1]


def handle_request(request):
    request = request.json
    session = None
    platform = None
    if 'session' in request:
        session = request['session']
        platform, session_id = get_platform_and_session_id(session)
    if session is None or platform is None:
        print(session)
        print(platform)
        raise Exception("Invalid session or platform")
    service_handlers[platform](request, session_id)
