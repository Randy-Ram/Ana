from flask import Flask, request, jsonify, Response
# from tasks import make_celery
import config
import codecs
from functools import wraps
from modules.fb.fb_bot import configure_bot
from modules.fb.handler_methods import *
from modules.twitter.twitter_core import *
from modules.twitter.twitter_bot import *
import requests
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
        pprint(request.get_json())
        req = request.get_json()
        if "apps" not in req and "direct_message_events" in req:
            # send_options()
            twt_handle_request(req)
        print("*" * 100)
    return jsonify({'status': 'success'})


@app.route('/register_twitter_endpoint', methods=["GET"])
def reg_twt_endpoint():
    resp = requests.post('https://www.twitter.com/all/development/webhooks.json?url=')
    print(resp.text)


if config.access_type == "test":
    app.run(host='0.0.0.0', port='5000', debug=True)
