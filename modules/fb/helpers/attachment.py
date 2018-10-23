# -*- coding: utf-8 -*-
class FBAttachment:
    class File:
        image = 'image'
        audio = 'audio'
        video = 'video'
        file = 'file'

    @staticmethod
    def button_postback(title, postback):
        return {
            'type': 'postback',
            'title': title,
            'payload': postback
        }

    @staticmethod
    def button_web_url(title, url):
        return {
            'type': 'web_url',
            'title': title,
            'url': url
        }

    @staticmethod
    def button_call(title, phone_number):
        return {
            "type": "phone_number",
            "title": title,
            "payload": phone_number
        }

    @staticmethod
    def button_account_link(url):
        return {
            'type': 'account_link',
            'url': url
        }

    @staticmethod
    def button_account_unlink(self=""):
        return {
            'type': 'account_unlink'
        }

    @staticmethod
    def quick_reply(title):
        return {
            'content_type': 'text',
            'title': title,
            'payload': title
        }

    @staticmethod
    def quick_reply_location():
        return {
            'content_type': 'location'
        }