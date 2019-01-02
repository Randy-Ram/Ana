"""
Dispatcher for slack slash commands
"""

from modules.slack.slack_core import send_response_to_slash_command, send_ephemeral_msg
from modules.slack.slack_helpers import create_flight_load_attachment_json
from modules.cal.flight_staff_listing import get_flight_staff_listing
from modules.cal.flight_loads import get_flight_loads_command
from modules.cal.flight_schedule import get_flight_schedule
from pprint import pprint
import json

"""
{'channel_id': 'CEVKRDUET',
 'channel_name': 'ana_testing',
 'command': '/flist',
 'response_url': 'https://hooks.slack.com/commands/TBJN6RCRJ/506262782357/GITrjzhl7MX5GiWzwtV2L9xU',
 'team_domain': 'bitsplease-tt',
 'team_id': 'TBJN6RCRJ',
 'text': '20181218 POS SLU 434',
 'token': 'wVvpIhSl9dAz89dMmevnPuAR',
 'trigger_id': '505325974464.392754862868.44ba072ecd8fdb3177adf0d2d168a6f0',
 'user_id': 'UBJUR1S7L',
 'user_name': 'randyram9'}
"""


def handle_staff_flight_list(response_url, text):
    try:
        date, board_point, off_point, flight_num = text.strip().split()
        resp = get_flight_staff_listing(date, board_point, off_point, flight_num)
        pprint(resp)
        send_response_to_slash_command(response_url, resp)
    except ValueError:
        send_response_to_slash_command(response_url, "Improper command usage. Please ensure you use the command like: "
                                                     "*/flist 20181217 POS SLU 434*")


def handle_flight_load(response_url, text):
    try:
        date, flight_number = text.strip().split()
        resp = get_flight_loads_command(date, flight_number)
        pprint(resp)
        send_response_to_slash_command(response_url, resp)
    except ValueError:
        send_response_to_slash_command(response_url, "Improper command usage. Please ensure you use the command like:"
                                                     "*/fload 20181228 525*")


def handle_flight_schedule(response_url, text, channel_id, user_id):
    try:
        date, dept_city, arrv_city, connections = text.strip().split()
        resp_arr, attachment_arr, resp_msg = get_flight_schedule(date, dept_city, arrv_city, connections)
        if resp_arr is None and resp_msg is not None:
            send_ephemeral_msg(channel_id, user_id, resp_msg)
            return
        output_arr = create_flight_load_attachment_json(resp_arr, attachment_arr, channel_id, user_id)
        for responses in output_arr:
            # send_response_to_slash_command(response_url, responses)
            # pprint(responses)
            send_ephemeral_msg(channel_id, user_id, None, payload=responses)
    except ValueError:
        send_response_to_slash_command(response_url, "Improper command usage. Please ensure you use the command like:"
                                                     "*/fsched 20181228 POS JFK 0*")


def dispatch_slack_action(slack_request):
    command = slack_request['command']
    response_url = slack_request['response_url']
    text = slack_request['text']
    channel_id = slack_request["channel_id"]
    user_id = slack_request["user_id"]
    if command == "/flist":
        handle_staff_flight_list(response_url, text)
    elif command == "/fload":
        handle_flight_load(response_url, text)
    elif command == "/fsched":
        handle_flight_schedule(response_url, text, channel_id, user_id)
    elif command == "/fltest":
        # send_test_response(slack_request)
        handle_flight_schedule(response_url, text, channel_id, user_id)


def dispatch_slack_button_req(slack_btn_resp):
    slack_payload = json.loads(slack_btn_resp['payload'])
    # pprint(slack_payload)
    req = slack_payload['callback_id']
    text = slack_payload['actions'][0]['value']
    response_url = slack_payload['response_url']
    if req == 'fload':
        handle_flight_load(response_url, text)


"""
{'payload': '{
        "type":"interactive_message",
        "actions":[
            {"name":"fload","type":"button","value":"281218 524"}
            ],
        "callback_id":"fload",
        "team":{"id":"TBJN6RCRJ","domain":"bitsplease-tt"},
        "channel":{"id":"CEVKRDUET","name":"ana_testing"},"user":{"id":"UBJUR1S7L","name":"randyram9"},
        "action_ts":"1545581109.192653","message_ts":"1545581098.004300","attachment_id":"1",
        "token":"wVvpIhSl9dAz89dMmevnPuAR","is_app_unfurl":false,
        "response_url":"https:\\/\\/hooks.slack.com\\/actions\\/TBJN6RCRJ\\/510674468884\\/J7c2R5RfdnjjLaErLKajjlRJ",
        "trigger_id":"510737732499.392754862868.cfaf707a5ca951ca45409a3f9c57ec92"}'}

"""

