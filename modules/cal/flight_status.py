import requests
import datetime
import traceback
from modules.config import flight_info_endpoint, cal_api_get_token, app_id, app_key, cert_path
from pprint import pprint
from modules.fb.helpers.status_cards import gen_fb_status_card

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


def format_datetime(iso_time):
    new_datetime = datetime.datetime.strptime(iso_time, "%Y-%m-%dT%H:%M:%S")
    return new_datetime.strftime("%a %d %b, %Y") + " " + new_datetime.strftime("%I:%M%p")


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
    resp = requests.post(flight_info_endpoint, json=data, headers=header, verify=True)
    pprint(resp.json())
    return resp.json()


def fetch_flight_status(df_request):
    print("Getting flight status")
    response_dict = {
        'preamble': None,
        'response_list': []
    }
    try:
        date = df_request['queryResult']['parameters']['date']
        flight_num = df_request['queryResult']['parameters']['flight-number']
        # flight_resp = response_generator(date, flight_num)
        if ":" == date[-3:-2]:
            date = date[:-3] + date[-2:]
        day_of_date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z").date()
        flight_info = get_flight_info(flight_num, date)  # GET FLIGHT INFO FROM API
        # if len(flight_info.keys()) > 1:
        #     response_dict['preamble'] = "It seems there were more than one flight {flight_num} on {dept_date}. " \
        #                                 "This is usually because of overnight flights".format(
        #         flight_num=flight_num,
        #         dept_date=day_of_date
        #     )
        if len(flight_info) == 0:
            response_dict['preamble'] = "I'm not seeing any flights for {flight_num} scheduled for {dept_date}".format(
                flight_num=flight_num,
                dept_date=day_of_date
            )
        else:
            for key, flight_resp in flight_info.items():
                flight_status = flight_resp["flight_status"]
                formatted_arr_date = format_datetime(flight_resp['arr_time_local'])
                formatted_dept_date = format_datetime(flight_resp['dept_time_local'])
                formatted_std = format_datetime(flight_resp['std_local'])
                formatted_sta = format_datetime(flight_resp['sta_local'])
                # Get the date only from the Flight Status endpoint response to compare
                arr_date_only = datetime.datetime.strptime(flight_resp['arr_time_local'], "%Y-%m-%dT%H:%M:%S").date()
                dept_date_only = datetime.datetime.strptime(flight_resp['dept_time_local'], "%Y-%m-%dT%H:%M:%S").date()
                # Commenting the below bc I'm not sure why it was added in the first place
                # if arr_date_only != day_of_date and dept_date_only != day_of_date:
                #     continue
                if flight_status in ("Cancelled", "Delayed"):
                    flight_status = "cancellation" if flight_status == "Cancelled" else "delay"
                    msg = f'Unfortunately {flight_num} has suffered a {flight_status}. The estimated departure time ' \
                          f'is {formatted_dept_date} ({flight_resp["dept_code"]} time) and the new estimated arrival' \
                          f' time is {formatted_arr_date} ({flight_resp["arr_code"]} time).'
                    # response_dict['response_list'].append({'flight_status': flight_status, "msg": msg, 'api_response': flight_resp})
                    fb_card = gen_fb_status_card(flight_resp, flight_status)
                    response_dict['response_list'].append({'flight_status': flight_status, 'msg': msg,
                                                           'fb_card': fb_card})
                elif flight_status == "Scheduled":
                    msg = "{flight_num} is scheduled to depart {dept_city} on {dept_time} ({dept_code} time) and arrive" \
                          " in {arr_city} at {arr_time} ({arr_code} time).".format(
                        flight_num=flight_num,
                        arr_city=flight_resp["arr_city"],
                        arr_time=formatted_arr_date,
                        dept_city=flight_resp["dept_city"],
                        dept_time=formatted_dept_date,
                        dept_code=flight_resp["dept_code"],
                        arr_code=flight_resp["arr_code"]
                    )
                    response_dict['response_list'].append({'flight_status': flight_status, 'msg': msg})
                    # fb_bot.send_text_message(user_session, msg)
                elif flight_status == "Completed":
                    msg = "{flight_num} has already reached {arr_city} from {dept_city}. It arrived on {arr_time} " \
                          "({arr_code} time).".format(
                        flight_num=flight_num,
                        arr_city=flight_resp["arr_city"],
                        arr_time=formatted_arr_date,
                        arr_code=flight_resp['arr_code'],
                        dept_city=flight_resp['dept_city']
                    )
                    print("COMPLETED FLIGHT")
                    response_dict['response_list'].append({'flight_status': flight_status, 'msg': msg})
                    # fb_bot.send_text_message(user_session, msg)
                elif flight_status == "Airborne":
                    msg = "{flight_num} departed {dept_city} at {dept_time} ({dept_code} time). It is currently" \
                        " airborne and scheduled to arrive at {arr_city} at {arr_time} ({arr_code} time)".format(
                            flight_num=flight_num,
                            arr_city=flight_resp["arr_city"],
                            arr_time=formatted_arr_date,
                            dept_city=flight_resp["dept_city"],
                            dept_time=formatted_dept_date,
                            dept_code=flight_resp["dept_code"],
                            arr_code=flight_resp["arr_code"]
                    )
                    response_dict['response_list'].append({'flight_status': flight_status, 'msg': msg})
                    # fb_bot.send_text_message(user_session, msg)
                elif flight_status == "Landed":
                    msg = f"{flight_num} has just landed in {flight_resp['arr_city']}. It arrived at " \
                          f"{formatted_arr_date} ({flight_resp['arr_code']} time.)"
                    response_dict['response_list'].append({'flight_status': flight_status, 'msg': msg})
                else:
                    response_dict['response_list'].append({'flight_status': "error", "msg": "Sorry, I can't seem to "
                                                                                            "find any information for "
                                                                                            "that flight."})
        if len(response_dict['response_list']) > 1:
            response_dict['preamble'] = "It seems there were more than one flight {flight_num} on {dept_date}. " \
                                        "This is usually because of overnight flights".format(
                flight_num=flight_num,
                dept_date=day_of_date
            )
    except KeyError:
        print(traceback.print_exc())
        response_dict['response_list'].append(
            {'flight_status': "error", "msg": "Sorry, I can't seem to find any information for that flight."})
        # fb_bot.send_text_message(user_session, "Sorry, I can't seem to find any information for that flight.")
    except Exception as e:
        print(traceback.print_exc())
        response_dict['response_list'].append(
            {'flight_status': "error", "msg": "Sorry, I can't seem to find any information for that flight."})
    finally:
        return response_dict


if __name__ == "__main__":
    # from_date, to_date = get_from_to_date('2018-11-12T12:00:00-05:00')
    get_flight_info("BW600", '2018-11-12T12:00:00-05:00')
