from datetime import datetime
import googlemaps
import json
from urllib.parse import urlunparse, urlencode
from .databases import sessions
from .models import WebhookRequest
from .data import DESTINATIONS, USERS
from google.cloud import firestore
from twilio.rest import Client


def find_nearest_facilities(address: str) -> list:
    API_KEY = 'AIzaSyA3XwIfGzcj1V868dJfsXhXkB5AHx0Bke0'
    gmaps = googlemaps.Client(key=API_KEY)
    distance_matrix = gmaps.distance_matrix(origins=address, destinations=DESTINATIONS, mode='driving')
    sorted_matrix = [(
            distance_matrix['destination_addresses'][idx], 
            distance_matrix['rows'][0]['elements'][idx]['distance']['value'],
            distance_matrix['rows'][0]['elements'][idx]['duration']['value']
        ) for idx in range(len(DESTINATIONS))]
    sorted_matrix.sort(key=lambda r: r[2])
    return [
        {
            'address': sm[0], 
            'distance': sm[1], 
            'duration': sm[2]
        } for sm in sorted_matrix 
    ]

def get_session_id(webhook: WebhookRequest) -> str:
    session = webhook.sessionInfo.dict().get('session')
    return session.split('/')[-1]

def update_session_doc(session_id: str, data: dict):
    document = sessions.document(session_id)
    document.set(data)

def get_session_doc(session_id: str):
    document = sessions.document(session_id).get()
    return document.to_dict()

def get_current_address(session_id: str) -> str:
    document = get_session_doc(session_id)
    location_index = document.get('location_index')
    if not location_index:
        raise KeyError('Uh oh, something went wrong!')
    return document.get('locations')[location_index]

# def format_datetime(pt: dict):
#     date = '{year}-{month}-{day}'.format(
#         year=str(int(pt['year'])),
#         month=str(int(pt['month'])),
#         day=str(int(pt['day']))
#     )
#     time = '{hours}:{minutes}'.format(
#         hours=str(int(pt['hours'])),
#         minutes=str(int(pt['minutes']))
#     )
#     return date, time

def format_datetime(pt: dict):
    year = int(pt['year'])
    month = int(pt['month'])
    day = int(pt['day'])
    hour = int(pt['hours'])
    minute = int(pt['minutes'])
    dt_object = datetime(
        year, month, day,
        hour=hour, minute=minute
    )
    date = dt_object.strftime("%Y-%m-%d")
    time = dt_object.strftime('%I:%M %p')
    return date, time

def validate_phone_number(phone_number: str):
    print(phone_number)
    phone_number = phone_number.replace('-', '')
    if not phone_number.startswith('+1'):
        phone_number = '+1' + phone_number
    print(phone_number)
    return phone_number

def make_maps_url(address) -> str:
    # https://www.google.com/maps/dir/?api=1&parameters
    parameters = {
        'api': 1,
        'destination': address,
        'travelmode': 'driving'
    }
    scheme = 'https'
    netloc = 'www.google.com'
    path = '/maps/dir/'
    query = urlencode(parameters)
    return urlunparse((scheme, netloc, path, None, query, None))


def text_address(session_id: str, phone_number: str):
    ACCOUNT_SID = 'AC99b6074fd1d43e6918348ccf18cb47e3'
    AUTH_TOKEN = 'a5aaa6b4721f53a445ac8f23228cefcb'
    messaging = Client(ACCOUNT_SID, AUTH_TOKEN)

    phone_number = validate_phone_number(phone_number)
    session_doc = get_session_doc(session_id)
    location_index = session_doc['location_index']
    nearest = session_doc['locations'][location_index]['address']

    dir_url = make_maps_url(nearest)
    # body = f'The nearest VA location is {nearest}.'
    body = f"Your preferred VA Medical Center is {nearest}"
    body_dir = f"Here's a link with directions: {dir_url}"
    messaging.messages.create(
        body=body, 
        from_='+18448805679', 
        to=phone_number
    )
    messaging.messages.create(
        body=body_dir, 
        from_='+18448805679', 
        to=phone_number
    )

def text_appt_confirmation(session_id: str, phone_number: str, date, time):
    ACCOUNT_SID = 'AC99b6074fd1d43e6918348ccf18cb47e3'
    AUTH_TOKEN = 'a5aaa6b4721f53a445ac8f23228cefcb'
    messaging = Client(ACCOUNT_SID, AUTH_TOKEN)

    phone_number = validate_phone_number(phone_number)
    session_doc = get_session_doc(session_id)
    location_index = session_doc['location_index']
    nearest = session_doc['locations'][location_index]['address']

    dir_url = make_maps_url(nearest)

    body = f'Your appointment at {nearest} is set for {date} {time}'
    body_dir = f"Here's a link with directions: {dir_url}"
    messaging.messages.create(
        body=body, 
        from_='+18448805679', 
        to=phone_number
    )
    messaging.messages.create(
        body=body_dir, 
        from_='+18448805679', 
        to=phone_number
    )

def get_next_nearest(session_id: str) -> str:
    session_doc = get_session_doc(session_id)
    # Usage of modulus operator to 'wrap-around'
    # Upon hitting index 4 ... 4 % 4 = 0, 5 % 4 = 1...
    location_index = (session_doc['location_index'] + 1) % len(session_doc['locations'])
    next_nearest = session_doc['locations'][location_index]['address']
    session_doc.update({'location_index': location_index})
    update_session_doc(session_id, session_doc)
    return next_nearest

def text_next_nearest(session_id: str, phone_number: str):
    ACCOUNT_SID = 'AC99b6074fd1d43e6918348ccf18cb47e3'
    AUTH_TOKEN = 'a5aaa6b4721f53a445ac8f23228cefcb'
    messaging = Client(ACCOUNT_SID, AUTH_TOKEN)

    phone_number = validate_phone_number(phone_number)
    session_doc = get_session_doc(session_id)
    location_index = session_doc['location_index']
    nearest = session_doc['locations'][location_index]['address']

    # body = f'The next nearest VA location is {nearest}.'
    body = f"Your preferred VA Medical Center is {nearest}"
    message = messaging.messages.create(
        body=body, 
        from_='+18448805679', 
        to=phone_number
    )

def validate_branch(branch):
    airforce = ['air force', 'airforce']
    natlguard = ['national guard', 'nationalguard']
    validated = None
    if branch.lower().strip() == 'army':
        validated = 'Army'
    elif branch.lower().strip() == 'navy':
        validated = 'Navy'
    elif branch.lower().strip() in airforce:
        validated = 'Airforce'
    elif branch.lower().strip() in natlguard:
        validated = 'National Guard'
    else:
        print('Branch of service validation error')
        validated = None
    return validated

def get_user_by_branch(branch):
    validated = validate_branch(branch)
    return USERS.get(validated)