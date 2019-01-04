import requests
import datetime
from pprint import pprint
from modules.config import flight_staff_listing_endpoint, cert_path


"""
{
  "flight_number": "434",
  "board_point": "POS",
  "off_point": "SLU",
  "dept_date": "20181217",
  "access_code": "monday"
}
"""


def make_flight_listing_req(dept_date, flight_number, access_code, board_point, off_point):
    if "BW" in flight_number:
        flight_number = flight_number.replace("BW", "").strip()

    data = {
        "flight_number": flight_number,
        "board_point": board_point,
        "off_point": off_point,
        "dept_date": dept_date,
        "access_code": access_code
    }
    pprint(data)
    resp = requests.post(flight_staff_listing_endpoint, json=data, verify=cert_path)
    pprint(resp.json())
    return resp.json()


def get_pax_status(status):
    if status == "cst":
        return "Standby"
    elif status == "cna":
        return "Not Accepted"
    elif status == "cac":
        return "Accepted"
    return status


def get_flight_staff_listing(date, board_point, off_point, flight_num):
    try:
        # date_formatted = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z").date().strftime("%Y%m%d")
        access_code = datetime.datetime.now().strftime("%A").lower()
        flight_listing = make_flight_listing_req(date, flight_num, access_code, board_point, off_point)
        if 'status' in flight_listing and flight_listing['status'] is True:
            if len(flight_listing['pax']) == 0:
                return "It seems there isn't any staff members on this flight."
            pax_list = flight_listing['pax']
            response_str = "*Staff Listing (by priority)*\n"
            for index, pax in enumerate(pax_list):
                response_str += f"{index + 1}. {pax['fname']} {pax['lname']}. Priority: {pax['priority']} " \
                                f"- Status: *{get_pax_status(pax['status'])}*"
                if 'seat' in pax and pax['seat'] != '':
                    response_str += f"{', Seat: ' + pax['seat']}"
                response_str += "\n"
            print(response_str)
            return response_str
        else:
            if 'message' in flight_listing:
                return 'Sorry. I got this error: ' + flight_listing['message']
            return "Error handling request."
    except Exception as err:
        import traceback
        print(traceback.print_exc())
        print(err)


if __name__ == "__main__":
    pass
