"""
The below contains the default responses for Ana. If the intent does not match in the specific handler, it checks
the default responses to see if the intent is specified there.
"""

responses = {
    "faq.baggage": 'You can find info on our baggage policy here: https://www.caribbean-airlines.com/#/baggage',
    'faq.dutyfree': 'You can find info on your duty-free here: https://www.caribbean-airlines.com/#/caribbean-experience/duty-free',
    'faq.special_requests': 'You can find info on all special requests here: https://www.caribbean-airlines.com/#/requests-and-special-assistance/seat-asignments',
    'faq.miles_info': 'You can find info on Caribbean Miles here: https://www.caribbean-airlines.com/#/loyalty-programmes/caribbean-miles',
    'faq.checkin.online': 'You can check-in online at: https://checkin.si.amadeus.net/1ASIHSSCWEBBW/sscwbw/checkin',
    'flight.checkin': 'You can check-in online at: https://checkin.si.amadeus.net/1ASIHSSCWEBBW/sscwbw/checkin',
    'faq.cars': 'You can rent cars here: http://cars.cartrawler.com/caribbeanairlines',
    'faq.hotels': 'You can book hotels here: http://hotels.caribbean-airlines.com',
    'faq.reservations': 'You can get all reservation related information here: https://www.caribbean-airlines.com/#/reservations',
    'faq.contacts': 'You can find our contact info here: https://www.caribbean-airlines.com/#/phone-contact-directory',
    'input.unknown': "I'm sorry, I don't quite understand your request.",
    'flight.book': "Sorry, currently I can't perform flight bookings ☹.️"
                   "You can check out our website to book flights: https://www.caribbean-airlines.com"
}