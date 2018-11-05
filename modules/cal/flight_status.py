import requests
import datetime
import traceback
import json
from config import flight_info_endpoint, cal_api_get_token, cal_api_check_token, app_id, app_key
from pprint import pprint

payload = {
    "appId": app_id,
    "appKey": app_key
}


def get_token():
    try:
        r = requests.post(cal_api_get_token, json=payload, verify=False)
        resp = r.json()
        if resp['status'] is True:
            return resp['token']
        else:
            return None
    except Exception as err:
        print(err)
        print(traceback.print_exc())


def create_header():
    token = get_token()
    return {
        'token': token
    }


def get_from_to_date(iso_time):
    new_datetime = datetime.datetime.strptime(iso_time, "%Y-%m-%dT%H:%M:%S%z")
    f_date = new_datetime.date().strftime("%Y-%m-%d") + "T00:00:00"
    t_date = new_datetime.date().strftime("%Y-%m-%d") + "T23:59:00"
    return f_date, t_date


def get_flight_info(flight_number, iso_date):
    from_date, to_date = get_from_to_date(iso_date)
    if "BW" in flight_number:
        flight_number = flight_number.replace("BW", "").strip()
    data = {
      "from_date": from_date,
      "to_date": to_date,
      "flight_number": flight_number
    }
    header = create_header()
    resp = requests.post(flight_info_endpoint, json=data, headers=header, verify=False)
    pprint(resp.json())
    return resp.json()


if __name__ == "__main__":
    from_date, to_date = get_from_to_date('2018-10-30T12:00:00-04:00')
    get_flight_info("BW600", from_date, to_date)
