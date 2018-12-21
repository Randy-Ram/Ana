"""
Define all the Facebook Methods that would return special responses
"""
from modules.fb.helpers.attachment import FBAttachment
from modules.fb.helpers.faq_helper import *
from modules.helpers.helpers import remove_escaped_characters
from modules.fb.fb_strings import *


def faq_airport_map(fb_bot, df_response, user_session):
    try:
        airport_code = df_response['result']['parameters']['airport']['IATA']
        formatted_airport_code = airport_code.lower()
        if formatted_airport_code not in available_terminal_maps:
            fb_bot.send_text_message(user_session, FB_NO_TERMINAL_MAP)
        else:
            fb_bot.send_text_message(user_session, FB_TERMINAL_MAP_AVAIL)
            fb_bot.send_message_file_attachment(user_session, FBAttachment.File.image,
                                                "https://i.imgur.com/oKOajZr.jpg")
    except KeyError:
        fb_bot.send_text_message(user_session, FB_NO_TERMINAL_MAP)


def faq_promo_response(fb_bot, promo_name, user_session, df_response):
    speech = ""
    try:
        if "fulfillment" in df_response["result"].keys() and "speech" in df_response["result"]["fulfillment"].keys():
            speech = df_response["result"]["fulfillment"]["speech"]
        if promo_name not in promos.keys():
            fb_bot.send_text_message(user_session, FB_NO_PROMOTION_ERROR)
        else:
            fb_bot.send_text_message(user_session, remove_escaped_characters(speech))
            fb_bot.send_message_file_attachment(user_session, FBAttachment.File.image, promos[promo_name])
    except Exception as e:
        fb_bot.send_text_message(user_session, FB_NO_PROMOTION_ERROR)


def send_button_with_urls(button_dict, button_title, fb_bot, user_session):
    buttons = []
    for key, val in button_dict.items():
        buttons.append(FBAttachment.button_web_url(key, val))
    fb_bot.send_message_buttons(user_session, button_title, buttons)


def create_generic_element(title, image_url, subtitle, button_arr):
    # buttons = []
    # for key, val in button_dict.items():
    #     buttons.append(FBAttachment.button_web_url(key, val))
    return {
        "title": title,
        "image_url": image_url,
        "subtitle": subtitle,
        "buttons": button_arr
    }


def create_and_send_carousel(info_dict, fb_bot, user_session, url_title="More Info"):
    """

    :param info_dict: Must contain key, val in the form "Card Title": ["Any Value", "Image URL", subtitles, button(FB.Attachment)]
    :param fb_bot:
    :param user_session:
    :return:
    """
    element_list = []
    for title, value in info_dict.items():
        element_list.append(
            create_generic_element(title, value[1], value[2], value[3])
        )
    fb_bot.send_message_generic_carousel(user_session, element_list)


def faq_baggage(fb_bot, user_session):
    try:
        for key, val in baggage_dict.items():
            val.append([FBAttachment.button_web_url("More Info", val[0])])
        # pprint(baggage_dict)
        fb_bot.send_text_message(user_session, FB_BAGGAGE_INFO)
        create_and_send_carousel(baggage_dict, fb_bot, user_session)
    except:
        fb_bot.send_text_message(user_session, FB_BAGGAGE_ERROR)


def faq_special_requests(fb_bot, user_session):
    try:
        for key, val in ssr_dict.items():
            val.append([FBAttachment.button_web_url("More Info", val[0])])
        fb_bot.send_text_message(user_session, FB_SPECIAL_SERVICES_INFO)
        create_and_send_carousel(ssr_dict, fb_bot, user_session)
    except:
        fb_bot.send_text_message(user_session,FB_SPECIAL_SERVICES_ERROR)


def faq_dutyfree(fb_bot, user_session):
    try:
        buttons = [
            FBAttachment.button_web_url("Order Now", 'https://caribbeanairlinesdutyfree.com/'),
            FBAttachment.button_web_url("More Info", 'https://www.caribbean-airlines.com/#/caribbean-experience/duty-free')
        ]
        img = 'https://i.imgur.com/4PEsVdo.jpg'
        title = "CAL Duty Free"
        subtitle = "Browse. Order. Enjoy."
        fb_bot.send_message_generic(user_session, title, subtitle, img, buttons=buttons)
    except:
        fb_bot.send_text_message(user_session, FB_DUTY_FREE_ERROR)


def faq_miles(fb_bot, user_session):
    try:
        miles_title = FB_MILES_TITLE
        send_button_with_urls(miles_dict, miles_title, fb_bot, user_session)
    except:
        fb_bot.send_text_message(user_session, FB_MILES_ERROR)


def faq_checkin_online(fb_bot, user_session):
    checkin_title = FB_CHECKIN_TITLE
    send_button_with_urls(checkin_dict, checkin_title, fb_bot, user_session)


def faq_rent_car(fb_bot, user_session):
    title = FB_CAR_RENTAL_TITLE
    send_button_with_urls(car_dict, title, fb_bot, user_session)


def faq_contacts(fb_bot, user_session):
    title = FB_CONTACTS_TITLE
    send_button_with_urls(contact_dict, title, fb_bot, user_session)


def faq_reservations(fb_bot, user_session):
    try:
        for key, val in reservation_dict.items():
            val.append([FBAttachment.button_call("Call Representative", val[0])])
        create_and_send_carousel(reservation_dict, fb_bot, user_session)
        website_url = {
            "Book a Flight": "https://www.caribbean-airlines.com/"
        }
        title = FB_RESERVATIONS_TITLE
        send_button_with_urls(website_url, title, fb_bot, user_session)
    except:
        fb_bot.send_text_message(user_session, FB_RESERVATIONS_ERROR)

