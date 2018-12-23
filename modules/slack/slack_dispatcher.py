"""
Dispatcher for slack slash commands
"""

from modules.slack.slack_core import send_response_to_slash_command, send_test_response
from modules.cal.flight_staff_listing import get_flight_staff_listing
from modules.cal.flight_loads import get_flight_loads_command
from modules.cal.flight_schedule import get_flight_schedule
from pprint import pprint

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


def handle_flight_schedule(response_url, text):
    try:
        date, dept_city, arrv_city, connections = text.strip().split()
        resp = get_flight_schedule(date, dept_city, arrv_city, connections)
        pprint(resp)
        send_response_to_slash_command(response_url, resp)
    except ValueError:
        send_response_to_slash_command(response_url, "Improper command usage. Please ensure you use the command like:"
                                                     "*/fsched 20181228 POS JFK 0*")


def dispatch_slack_action(slack_request):
    command = slack_request['command']
    response_url = slack_request['response_url']
    text = slack_request['text']
    if command == "/flist":
        handle_staff_flight_list(response_url, text)
    elif command == "/fload":
        handle_flight_load(response_url, text)
    elif command == "/fsched":
        handle_flight_schedule(response_url, text)
    elif command == "/fltest":
        send_test_response(slack_request)
