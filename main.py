import os
from fastapi import FastAPI
from modules.databases import sessions
from modules.models import WebhookRequest
from modules.functions import (
    get_session_id, 
    text_address,
    find_nearest_facilities, 
    update_session_doc, 
    get_next_nearest, 
    text_next_nearest,
    get_user_by_branch,
    get_current_address,
    format_datetime,
    text_appt_confirmation
)
from modules.responses import (
    resp_next_nearest_template, 
    nearest_location_template, 
    text_nearest_template,
    text_next_nearest_template,
    user_authenticated_template,
    resp_set_appt_template,
    resp_text_appt_template,
    resp_get_ticket_template
)

app = FastAPI()

@app.post('/find_nearest')
async def find_nearest_location(webhook: WebhookRequest):
    session_id = get_session_id(webhook)
    parameters = webhook.sessionInfo.dict()['parameters']
    zip_code = parameters.get('zip-code')
    if zip_code:
        locations = find_nearest_facilities(zip_code)
        data = {
            'locations': locations,
            'location_index': 0
        }
        update_session_doc(session_id, data)
        return nearest_location_template(zip_code, locations[0]['address'])
    else:
        ...
    
@app.post('/text_nearest_address')
async def send_text_address(webhook: WebhookRequest):
    session_id = get_session_id(webhook)
    parameters = webhook.sessionInfo.dict()['parameters']
    phone_number = parameters['phone-number']
    text_address(session_id, phone_number)
    return text_nearest_template(phone_number)

@app.post('/find_next_nearest')
async def find_next_location(webhook: WebhookRequest):
    session_id = get_session_id(webhook)
    parameters = webhook.sessionInfo.dict()['parameters']
    zip_code = parameters.get('zip-code')
    next_nearest = get_next_nearest(session_id)
    return resp_next_nearest_template(next_nearest, zip_code)

@app.post('/text_next_nearest')
async def text_next_address(webhook: WebhookRequest):
    session_id = get_session_id(webhook)
    parameters = webhook.sessionInfo.dict()['parameters']
    phone_number = parameters['phone-number']
    text_address(session_id, phone_number)
    return text_next_nearest_template(phone_number)

@app.post('/authenticate_user')
async def authenticate_user(webhook: WebhookRequest):
    session_id = get_session_id(webhook)
    parameters = webhook.sessionInfo.dict()['parameters']
    # Cannot test without payload.  
    branch = parameters.get('service-branch')
    user = get_user_by_branch(branch)
    return user_authenticated_template(user)
    
@app.post('/set_appointment')
async def schedule_appointment(webhook: WebhookRequest):
    session_id = get_session_id(webhook)
    parameters = webhook.sessionInfo.dict()['parameters']
    preferred_time = parameters.get('preferred-time')
    date, time = format_datetime(preferred_time)
    current_address = get_current_address(session_id)['address']
    # Review API method
    return resp_set_appt_template(current_address, date, time)

@app.post('/text_appointment')
async def text_appointment(webhook: WebhookRequest):
    session_id = get_session_id(webhook)
    current_address = get_current_address(session_id)['address']
    parameters = webhook.sessionInfo.dict()['parameters']
    phone_number = parameters['phone-number']
    preferred_time = parameters.get('preferred-time')
    date, time = format_datetime(preferred_time)
    text_appt_confirmation(session_id, phone_number, date, time)
    return resp_text_appt_template(phone_number, current_address, date, time)

@app.post('/get_ticket')
async def get_ticket_status(webhook: WebhookRequest):
    session_id = get_session_id(webhook)
    parameters = webhook.sessionInfo.dict()['parameters']
    # Cannot test without payload.  
    branch = parameters.get('service-branch')
    user = get_user_by_branch(branch)
    return resp_get_ticket_template(user)
