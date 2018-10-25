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
fb_bot = FBBot(token, verify_token)


def configure_bot():
    # Set up the Persistent Menu and the Getting Started Button
    fb_bot.set_persistent_menu(persistent_menu.get_persistent_menu_buttons())
    fb_bot.set_get_started_button("get_started")
    return fb_bot