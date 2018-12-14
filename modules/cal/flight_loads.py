import requests
import datetime
import traceback
import json
from pprint import pprint


flight_loads_endpoint = 'https://api.caribbean-airlines.com/amadeus/flight_loads/'


def make_flight_loads_req(dept_date, flight_number, access_code, airline_code):
    if "BW" in flight_number:
        flight_number = flight_number.replace("BW", "").strip()

    data = {
        "flight_number": flight_number,
        "dept_date": dept_date,
        "access_code": access_code,
        "airline_code": airline_code
    }
    resp = requests.post(flight_loads_endpoint, json=data, verify=False)
    pprint(resp.json())
    return resp.json()


def get_flight_loads(df_request):
    try:
        response_list = []
        date = df_request['queryResult']['parameters']['date']
        date_formatted = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z").date().strftime("%d%m%y")
        access_code = datetime.datetime.now().strftime("%A").lower()
        flight_num = df_request['queryResult']['parameters']['flight-number']
        flight_loads = make_flight_loads_req(date_formatted, flight_num, access_code, "BW")
        if 'status' in flight_loads and flight_loads['status'] is True:
            load_list = flight_loads['loads']
            for each_flight in load_list:
                response_str = f"*{each_flight['origin']} -> {each_flight['destination']}*\n"
                for cabins, values in each_flight['cabins'].items():
                    # print(cabins, values)
                    if 'J' in cabins:
                        response_str += '*Business Class*\n'
                        response_str += f"Available: {values['available']}\n"
                        response_str += f"Booked: {values['booked']}\n"
                        response_str += f"Booked Staff: {values['booked_staff']}\n"
                        response_str += f"Capacity: {values['capacity']}\n\n"
                    if 'Y' in cabins:
                        response_str += '*Economy Class*\n'
                        response_str += f"Available: {values['available']}\n"
                        response_str += f"Booked: {values['booked']}\n"
                        response_str += f"Booked Staff: {values['booked_staff']}\n"
                        response_str += f"Capacity: {values['capacity']}\n"
                response_list.append(response_str)
            return response_list
        else:
            if 'message' in flight_loads:
                return ['Sorry. I got this error: ' + flight_loads['message']]
            return ["Error handling request."]
    except Exception as err:
        import traceback
        print(traceback.print_exc())
        print(err)


if __name__ == "__main__":
    test_req = {
        'queryResult': {
            'parameters': {
                'date': '2018-12-31T12:00:00-05:00',
                'flight-number': 'BW600'
            }
        }
    }

    pprint(get_flight_loads(df_request=test_req))
