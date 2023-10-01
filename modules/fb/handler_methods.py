"""
The functions in this file are used to handle various aspects of the Facebook bot interactions

e.g. on_postback is a method that is run when a postback is sent from Facebook - when a user clicks a quick button etc.
e.g. on_message is a method that is run when a user sends a message to the bot.
"""

from modules.fb.fb_bot import fb_bot, facebook_handle_request
from modules.fb.helpers.attachment import FBAttachment
from pprint import pprint
from modules.fb.helpers import persistent_menu
from modules import config


token = config.facebook_access_token


def on_postback(sender, text, requestInfo):
    print("postback")
    print(text)
    # fb_bot.send_text_message(sender, 'Received postback "{0}"'.format(text))
    if text == "get_started":
        send_initial_options(sender)
    elif text == "transfer_request":
        handover_request(sender)
    else:
        # pprint(text)
        # send_text_to_google(text, sender)
        facebook_handle_request(sender, text)


def on_location(sender, location, requestInfo):
    print("location")
    pprint(location)


def create_welcome_message(sender):
    user_info = fb_bot.get_userinfo(sender)
    pprint(user_info)
    first_name = user_info["first_name"]
    return f"\U0001F916 - Hello {first_name}, I'm Ana. I'm a robot and I'll try to answer any questions you may have."


def send_initial_options(sender):
    fb_bot.send_text_message(
        sender,
        create_welcome_message(sender),
        [
            FBAttachment.quick_reply("Check In \U0001F3AB"),
            FBAttachment.quick_reply("Flight Status \U0001F55B"),
            FBAttachment.quick_reply("Baggage Info \U0001F6C4"),
            FBAttachment.quick_reply("Make Booking \U0001F5A5"),
        ],
    )


def display_sender_action(sender_action, recipient_id):
    """

    :param sender_action: Can be either "typing_on", "typing_off", "mark_seen"
    :param recipient_id: ID of recipient
    :return:
    """
    graph_endpoint = (
        "https://graph.facebook.com/v2.6/me/messages?access_token={0}".format(token)
    )
    payload = {"recipient": {"id": recipient_id}, "sender_action": sender_action}
    response = fb_bot._send_payload(payload, graph_endpoint)


def handle_action(action, df_response, user_session):
    pass


def handover_check(recipient_id, df_response=None, text=None):
    pass


def handover_request(recipient_id, silent=False):
    print("Handing over request to agent...")
    if not silent:
        fb_bot.send_text_message(
            recipient_id,
            "One sec, transferring you to an agent for assistance (Response times may vary).",
        )
    pass_thread_endpoint = "https://graph.facebook.com/v2.6/me/pass_thread_control?access_token={0}".format(
        token
    )
    payload = {
        "recipient": {"id": recipient_id},
        "target_app_id": 263902037430900,
    }
    response = fb_bot._send_payload(payload, pass_thread_endpoint)


def on_linked(sender, login, requestInfo):
    print("link")
    print(sender + " " + login)


def on_unlinked(sender, requestInfo):
    print("unlink")
    print(sender + " unlink")


def on_message(sender, text, requestInfo):
    print("ON MESSAGE")
    # process_message(sender, text)
    facebook_handle_request(sender, text)


def process_message(sender, text):
    fb_bot.send_text_message(
        sender,
        "Please share your location",
        [persistent_menu.FBAttachment.quick_reply_location()],
    )
