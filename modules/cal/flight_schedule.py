import requests
import datetime
from pprint import pprint
from modules.config import flight_schedule_endpoint
from datetime import datetime

"""
[[{'arrival_city': 'YYZ',
   'arrival_datetime': '171218T0640',
   'departure_city': 'POS',
   'departure_datetime': '171218T0135',
   'flight_number': '602'}],
 [{'arrival_city': 'YYZ',
   'arrival_datetime': '171218T1815',
   'departure_city': 'POS',
   'departure_datetime': '171218T1310',
   'flight_number': '600'}]]
"""


def make_flight_schedule_req(dept_date, dept_city, arrv_city, access_code):
    data = {
      "dept_date": dept_date,  # ddmmyy
      "dept_city": dept_city,
      "arrv_city": arrv_city,
      "access_code": access_code
    }
    pprint(data)
    resp = requests.post(flight_schedule_endpoint, json=data, verify=False)
    pprint(resp.json())
    return resp.json()


def format_datetime(datetime_str):
    return datetime.strptime(datetime_str, "%d%m%yT%H%M").strftime("%a %d %b, %Y %I:%M%p")


def get_flight_schedule(date, dept_city, arrv_city, max_connections):
    msg_to_send = ''
    resp_arr = []
    attachment_arr = []
    access_code = datetime.now().strftime("%A").lower()
    date = datetime.strptime(date, "%Y%m%d").strftime("%d%m%y")
    schedule = make_flight_schedule_req(date, dept_city, arrv_city, access_code)
    if 'status' in schedule and schedule['status'] is True:
        for flights in schedule['flights']:
            if len(flights) > int(max_connections) + 1:
                continue
            for index, each_flight in enumerate(flights):  # Comment
                if len(flights) == 1:  # Direct flight
                    resp_arr.append(f"*{each_flight['departure_city']} -> {each_flight['arrival_city']}*\n" \
                                    f"*BW{each_flight['flight_number']}*\n" \
                                    f"Dept Time: {format_datetime(each_flight['departure_datetime'])}\n" \
                                    f"Arrv Time: {format_datetime(each_flight['arrival_datetime'])}\n{'*' * 40}\n\n"
                                    )
                    attachment_arr.append([date, each_flight['flight_number']])
                else:
                    flight_string = ''
                    local_msg = ''
                    for index2, each_leg in enumerate(flights):
                        # print(flights)
                        if index2 == 0:
                            flight_string += f"*{each_leg['departure_city']}->"
                        elif index2 == len(flights) - 1 and len(flights) == 2:
                            flight_string += f"{each_leg['departure_city']}->{each_leg['arrival_city']}*\n"
                        elif index2 == len(flights) - 1:
                            flight_string += f"->{each_leg['arrival_city']}*\n"
                        else:
                            flight_string += f"{each_leg['departure_city']}->{each_leg['arrival_city']}"
                        local_msg += f"*{each_leg['departure_city']} -> {each_leg['arrival_city']}*\n" \
                                     f"*BW{each_leg['flight_number']}*\n" \
                                     f"Dept Time: {format_datetime(each_leg['departure_datetime'])}\n" \
                                     f"Arrv Time: {format_datetime(each_leg['arrival_datetime'])}\n\n"
                        resp_arr.append(f"{flight_string}\n{local_msg}\n{'*' * 40}\n\n")
                        attachment_arr.append([date, each_leg['flight_number']])
        return resp_arr, attachment_arr


if __name__ == "__main__":
    get_flight_schedule("20190112", "POS", "JFK")

