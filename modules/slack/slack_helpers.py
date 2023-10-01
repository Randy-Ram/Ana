from datetime import datetime


def create_flight_load_attachment_json(resp_arr, attachment_arr, channel_id, user_id):
    output_arr = []
    for attach, text_val in zip(attachment_arr, resp_arr):
        attach[0] = datetime.strptime(attach[0], "%d%m%y").strftime(
            "%Y%m%d"
        )  # Format the datetime
        output_arr.append(
            {
                "text": text_val,
                "channel": channel_id,
                "user": user_id,
                "replace_original": False,
                "attachments": [
                    {
                        "fallback": "Sorry, could not get the flight load. Try running /fload manually",
                        "callback_id": "fload",
                        "attachment_type": "default",
                        "actions": [
                            {
                                "name": "fload",
                                "text": "Check flight load",
                                "type": "button",
                                "value": " ".join(
                                    attach
                                ),  # The value that is passed when the user clicks in the button
                            }
                        ],
                    }
                ],
            }
        )
    return output_arr


"""{
    "text": "Would you like to play a game?",
    "attachments": [
        {
            "text": "Choose a game to play",
            "fallback": "You are unable to choose a game",
            "callback_id": "wopr_game",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "game",
                    "text": "Chess",
                    "type": "button",
                    "value": "chess"
                },
                {
                    "name": "game",
                    "text": "Falken's Maze",
                    "type": "button",
                    "value": "maze"
                },
                {
                    "name": "game",
                    "text": "Thermonuclear War",
                    "style": "danger",
                    "type": "button",
                    "value": "war",
                    "confirm": {
                        "title": "Are you sure?",
                        "text": "Wouldn't you prefer a good game of chess?",
                        "ok_text": "Yes",
                        "dismiss_text": "No"
                    }
                }
            ]
        }
    ]
}
"""
