from modules.fb.helpers.faq_helper import *
from modules.helpers.helpers import remove_escaped_characters
from modules.fb.fb_strings import *
from modules.kommunicate.kommunicate_actionable import *
from modules.kommunicate.kommunicate_core import send_text_message, send_carousel_message, send_message_buttons, send_card_message
import json
from pprint import pprint


def send_button_with_urls(button_dict, button_title, session_id):
    buttons = []
    for key, val in button_dict.items():
        buttons.append(KommActionableMessages.button_web_url(val, key))
    buttons = json.dumps(buttons)
    send_message_buttons(button_title, session_id, buttons)


def create_and_send_carousel(info_dict, session_id, message, url_title='More Info'):
    """

    :param info_dict: "Card Title": [anything, subtitle, img_src, buttons]
    :param session_id:
    :param url_title:
    :return:
    """
    element_list = []
    for title, value in info_dict.items():
        element_list.append(KommActionableMessages.carousel_payload(title, value[2], value[1], value[3]))
    # pprint(element_list)
    element_list = json.dumps(element_list)
    send_carousel_message(session_id, payload=element_list, message=message)


def faq_baggage(session_id):
    try:
        for key, val in baggage_dict.items():
            val.append([KommActionableMessages.card_link_button("More Info", val[0])])
        # send_text_message(session_id, FB_BAGGAGE_INFO)
        create_and_send_carousel(baggage_dict, session_id, message=FB_BAGGAGE_INFO)
    except Exception as e:
        print(e)
        send_text_message(session_id, FB_BAGGAGE_ERROR)


def faq_special_requests(session_id):
    try:
        for key, val in ssr_dict.items():
            val.append([KommActionableMessages.card_link_button("More Info", val[0])])
        create_and_send_carousel(ssr_dict, session_id, message=FB_SPECIAL_SERVICES_INFO)
    except Exception as e:
        print(e)
        send_text_message(session_id, FB_SPECIAL_SERVICES_ERROR)


def faq_dutyfree(session_id):
    try:
        buttons = [
            KommActionableMessages.card_link_button("Order Now", "https://caribbeanairlinesdutyfree.com/"),
            KommActionableMessages.card_link_button("More Info", "https://www.caribbean-airlines.com/#/caribbean-experience/duty-free")
        ]
        img = 'https://i.imgur.com/4PEsVdo.jpg'
        title = "CAL Duty Free"
        subtitle = "Browse. Order. Enjoy."
        kom_card_payload = json.dumps([KommActionableMessages.card_payload(title, subtitle, img, buttons)])
        send_card_message(session_id, "Here's our Duty Free offering", kom_card_payload)
    except Exception as e:
        print(e)
        send_text_message(session_id, FB_DUTY_FREE_ERROR)


def faq_miles(session_id):
    try:
        miles_title = FB_MILES_TITLE
        send_button_with_urls(miles_dict, miles_title, session_id)
    except Exception as e:
        print(e)
        send_text_message(session_id, FB_MILES_ERROR)


def faq_checkin_online(session_id):
    checkin_title = FB_CHECKIN_TITLE
    send_button_with_urls(checkin_dict, checkin_title, session_id)


def faq_rent_car(session_id):
    title = FB_CAR_RENTAL_TITLE
    send_button_with_urls(car_dict, title, session_id)


def faq_contacts(session_id):
    title = FB_CONTACTS_TITLE
    send_button_with_urls(contact_dict, title, session_id)


def faq_reservations(session_id):
    """
    TODO - NEED TO RESOLVE SINCE PHONE NUMBERS ARE NOT A WEB LINK
    :param session_id:
    :return:
    """
    try:
        for key, val in reservation_dict.items():
            val.append([KommActionableMessages.card_link_button("Call Representative", val[0])])
        create_and_send_carousel(reservation_dict, session_id, message="Here's our reservation info.")
        website_url = {
            "Book a Flight": "https://www.caribbean-airlines.com/"
        }
        title = FB_RESERVATIONS_TITLE
        send_button_with_urls(website_url, title, session_id)
    except Exception as e:
        print(e)
        send_text_message(session_id, FB_RESERVATIONS_ERROR)


if __name__ == "__main__":
    faq_baggage("16800298")
