"""
If you're implementing a bot, this is the file that you would
configure the logic of your bot
"""

import config
from ..fb.fb_core import FBBot
from modules.fb.helpers import persistent_menu

token = config.facebook_access_token
verify_token = config.verify_token
# app.secret_key = config.secret_key
bot = FBBot(token, verify_token)


def configure_bot():
    # Set up the Persistent Menu and the Getting Started Button
    bot.set_persistent_menu(persistent_menu.get_persistent_menu_buttons())
    bot.set_get_started_button("get_started")
    return bot


def process_message(sender, text):
    bot.send_text_message(sender, "Please share your location", [
        persistent_menu.FBAttachment.quick_reply_location()
    ])