from .AirlineFlightUpdate import AirlineFlightUpdate


def gen_fb_status_card(flight_resp, flight_status):
    # pprint(flight_resp)
    # print(flight_status)
    formatted_status = "cancelled" if flight_status == "cancellation" else "delayed"
    message = AirlineFlightUpdate(
        "BW {flight_num} has unfortunately been {flight_status}".format(flight_num=flight_resp['flight_number'],
                                                                        flight_status=formatted_status),
        flight_status,
        "en_US",
        "-",
        AirlineFlightUpdate.make_update_flight_info(
            flight_resp['flight_number'],
            AirlineFlightUpdate.make_airport(flight_resp['dept_code'], flight_resp['dept_city']),
            AirlineFlightUpdate.make_airport(flight_resp['arr_code'], flight_resp['arr_city']),
            AirlineFlightUpdate.make_flight_schedule(flight_resp['dept_time_local'], flight_resp['arr_time_local'])
            # AirlineFlightUpdate.make_flight_schedule("2016-01-05T15:05", "2016-01-07T15:05")
        ),
        theme_color="#84329B"
    )
    return message
