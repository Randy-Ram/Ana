from flask import Flask, request, jsonify, Response
# from tasks import make_celery
import config
from pprint import pprint
import codecs
import requests
from functools import wraps
from modules.fb.fb_bot_logic import configure_bot
from modules.fb.helpers.attachment import FBAttachment
from modules.fb.fb_bot_logic import process_message


app = Flask(__name__)

bot = configure_bot()


def check_auth(username, password):
    """This function is called to check if a username /
        password combination is valid.
        """
    return username == config.http_user and password == config.http_pw


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route("/", methods=["GET", "POST"])
def index():
    pprint(request)
    return jsonify({"status": "Success"})


@app.route('/facebook', methods=['GET', 'POST'])
def webhook():
    pprint(request)
    return bot.webhook(request, on_message, on_postback, on_linked, on_unlinked, on_location)


def on_linked(sender, login, requestInfo):
    print("link")
    print(sender+" " + login)


def on_unlinked(sender, requestInfo):
    print("unlink")
    print(sender+" unlink")


@app.route('/test', methods=["GET"])
def test_route():
    return jsonify({"value": "Hello World"})


def on_postback(sender, text, requestInfo):
    print("postback")
    print(text)
    bot.send_text_message(sender, 'Received postback "{0}"'.format(text))
    if text == 'get_started':
        send_initial_options(sender)
    elif text == "transfer_request":
        handover_request(sender)
    else:
        pprint(text)
        # send_text_to_google(text, sender)


def on_location(sender, location, requestInfo):
    print("location")
    pprint(location)


def remove_escaped_characters(text):
    return codecs.unicode_escape_decode(text)[0]


def create_welcome_message(sender):
    user_info = bot.get_userinfo(sender)
    first_name = user_info['first_name']
    return '''
            \U0001F916 - Hello {0}! I'm Disastron, your friendly bot that would like to be of assistance to you \
            during disasters. You can choose from the buttons below to get started'''.format(first_name)


def send_initial_options(sender):
    bot.send_text_message(sender, create_welcome_message(sender), [
        FBAttachment.quick_reply("Report Flooding \U0001F3AB"),
        FBAttachment.quick_reply("Request Assistance \U0001F55B"),
        FBAttachment.quick_reply("Get Help \U0001F6C4")
        # FBAttachment.quick_reply("Make Booking \U0001F5A5")
    ])


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
    response = bot._send_payload(payload, graph_endpoint)


@app.route('/dialogFlowEndpoint', methods=['POST'])
@requires_auth
def df_endpoint():
    """
    Webhook that DialogFlow contacts
    :return:
    """
    pass


def handle_action(action, df_response, user_session):
    pass


def handover_check(recipient_id, df_response=None, text=None):
    pass


def handover_request(recipient_id, silent=False):
    pass



@app.route('/send_flight_status_update', methods=['POST'])
def flight_status():
    pass


def send_text_to_google(text, sender):
    pass


def on_message(sender, text, requestInfo):
    print("ON MESSAGE")
    process_message(sender, text)


@app.route('/twitter', methods=['GET', 'POST'])
def twitter_handler():
    pass


if config.access_type == "test":
    app.run(host='0.0.0.0', port='5000', debug=True)
