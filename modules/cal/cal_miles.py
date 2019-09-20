import zeep
import traceback
from zeep.transports import Transport
from requests import Session


session = Session()
session.verify = False
# wsdl = 'https://wsbwauat.frequentflyer.aero/lms-ws/lmsWs?wsdl'
wsdl = 'https://wsbwa.frequentflyer.aero/lms-ws/lmsWs?wsdl'
transport = Transport(session=session)
try:
    client = zeep.Client(wsdl=wsdl, transport=transport)
except Exception as e:
    raise ConnectionError("Cannot connect to ALMS")
username = 'wstest'
password ='WS-test01'


def query_miles_from_alms(member_id):
    member_type = client.get_type('ns0:memberReq')
    member = member_type(memberId=member_id, retrieveMemberProfiles={'retrieveMemberProfileType': 'ALL'})
    header_type = client.get_element('ns0:header')
    header = header_type(userName=username, passWord=password)
    response = client.service.retrieveProfile(retrieveProfileRequest=member, _soapheaders=[header])
    if response['processStatus'] == 'NOK':
        return None
    else:
        return response['memberCard']['awardMiles']


def get_miles(df_response):
    try:
        member_id = str(int(df_response['queryResult']['parameters']['memberId']))
        return query_miles_from_alms(member_id)
    except KeyError:
        print(traceback.print_exc())
        return None


if __name__ == "__main__":
    print(query_miles_from_alms("1120207513"))

# 23756, 9336, 22615