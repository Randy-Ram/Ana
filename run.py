from flask import Flask, request, jsonify, Response
from threading import Thread
# from tasks import make_celery
from modules import config
from functools import wraps
from modules.fb.handler_methods import *
from modules.twitter.twitter_core import *
from modules.twitter.twitter_bot import *
from modules.whatsapp.whatsapp_bot import *
from modules.slack.slack_bot import *
from modules.slack.slack_dispatcher import dispatch_slack_action
import requests
import random
import dispatcher


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
    """
    Decorating function to check for auth.
    :param f:
    :return:
    """
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
    return fb_bot.webhook(request, on_message, on_postback, on_linked, on_unlinked, on_location)


@app.route('/test', methods=["GET"])
def test_route():
    return jsonify({"value": "Hello World"})


@app.route('/dialogFlowEndpoint', methods=['POST'])
@requires_auth
def df_endpoint():
    """
    Webhook that DialogFlow contacts
    :return:
    """
    dispatcher.handle_request(request)
    return jsonify({"status": "success"})


@app.route('/twitter', methods=['GET', 'POST'])
def twitter_handler():
    if 'crc_token' in request.args:
        print("CRC Check")
        return webhook_challenge(request)
    else:
        # pprint(request.get_json())
        req = request.get_json()
        if "apps" not in req and "direct_message_events" in req:
            # send_options()
            twitter_handle_user_request(req)
        print("*" * 100)
    return jsonify({'status': 'success'})


@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp_handler():
    whatsapp_handle_request(request.form)
    return "Success"


@app.route('/register_twitter_endpoint', methods=["GET"])
def reg_twt_endpoint():
    resp = requests.post('https://www.twitter.com/all/development/webhooks.json?url=')
    print(resp.text)


@app.route('/slack_slash_commands', methods=['POST'])
def slack_slash_handler():
    responses = ["Getting that for you", "One sec...", "Fetching response...", "Acquiring data..."]
    pprint(request.form)
    thread = Thread(target=dispatch_slack_action, kwargs={'slack_request': request.form})
    thread.start()
    return random.choice(responses), 200


@app.route('/slack', methods=['POST'])
def slack_handler():
    req = request.get_json()
    if 'challenge' in req:
        return req['challenge']
    else:
        thread = Thread(target=slack_handle_request, kwargs={'request': request.get_json()})
        thread.start()
    return jsonify({"ok": True}), 200


@app.route('/slack_button_endpoint', methods=["POST"])
def slack_button_endpoint():
    print("Dropdown pressed")
    pprint(request.form)
    # thread = Thread(target=dispatch_slack_action, kwargs={'slack_request': request.form})
    # thread.start()
    return "Good", 200


if config.access_type == "test" and __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)
