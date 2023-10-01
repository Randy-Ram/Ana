class KommActionableMessages:
    @staticmethod
    def button_web_url(url, name, open_link_in_new_tab="false"):
        return {
            "type": "link",
            "url": url,
            "name": name,
            "openLinkInNewTab": open_link_in_new_tab,
        }

    @staticmethod
    def button_submit(name, reply_text=""):
        return {"name": name, "replyText": reply_text}

    @staticmethod
    def quick_reply(title, message, reply_metadata=None):
        return (
            {"title": title, "message": message}
            if reply_metadata is None
            else {"title": title, "message": message, "replyMetadata": reply_metadata}
        )

    @staticmethod
    def image_reply(caption, image_url):
        return {"caption": caption, "url": image_url}

    @staticmethod
    def list_element(img_src, title, description, action):
        return {
            "imgSrc": img_src,
            "title": title,
            "description": description,
            "action": action,
        }

    @staticmethod
    def list_button(action_type, name, link_or_text):
        return (
            {"name": name, "action": {"type": "quick_reply", "text": link_or_text}}
            if action_type == "quick_reply"
            else {"name": name, "action": {"type": "link", "url": link_or_text}}
        )

    @staticmethod
    def list_payload(header_img_src, header_text, elements, buttons):
        """
        Returns the payload for a list template

        :param header_img_src: URL for header image
        :param header_text: Text for Header
        :param elements: List of elements - gotten from list_element method
        :param buttons: list of buttons received from list_button method
        :return:
        """
        return {
            "headerImgSrc": header_img_src,
            "headerText": header_text,
            "elements": elements,
            "buttons": buttons,
        }

    @staticmethod
    def card_quick_reply_button(title, message):
        return {
            "action": {
                "type": "quickReply",
                "payload": {"title": title, "message": message},
            }
        }

    @staticmethod
    def card_link_button(name, url):
        return {"name": name, "action": {"type": "link", "payload": {"url": url}}}

    @staticmethod
    def card_submit_button(button_text, form_data):
        return {
            "action": {
                "type": "submit",
                "payload": {"text": button_text, "formData": form_data},
            }
        }

    @staticmethod
    def card_payload(
        title, subtitle, img, buttons, overlay_text="", description="", title_ext=""
    ):
        return {
            "title": title,
            "subtitle": subtitle,
            "header": {"overlayText": overlay_text, "imgSrc": img},
            "description": description,
            "titleExt": title_ext,
            "buttons": buttons,
        }

    @staticmethod
    def carousel_payload(
        title, subtitle, img_src, buttons, description="", overlay_text="", title_ext=""
    ):
        return {
            "title": title,
            "subtitle": subtitle,
            "header": {"overlayText": overlay_text, "imgSrc": img_src},
            "description": description,
            "titleExt": title_ext,
            "buttons": buttons,
        }
