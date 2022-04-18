
def text_response(text: str) -> dict:
        return {
        'fulfillment_response': {
            'messages': [
                {
                    'text': {
                        'text': [
                            text
                        ]
                    }
                }
            ]
        }
    }

def validate_ssml(ssml: str) -> str:
    if not ssml.startswith('<speak>'):
        ssml = '<speak>' + ssml
    if not ssml.endswith('</speak>'):
        ssml += '</speak>'
    return ssml

def output_audio_text_response(ssml: str) -> dict:
    ssml = validate_ssml(ssml)
    return {
    'fulfillment_response': {
        'messages': [
            {
                'output_audio_text': {
                    'ssml': [
                        ssml
                    ]
                }
            }
        ]
    }
}

def text_and_ssml_response(text, ssml) -> dict:
    ssml = validate_ssml(ssml)
    return {
    'fulfillment_response': {
        'messages': [
            {
                'output_audio_text': {
                    'ssml': ssml
                },
            },{
                'text': {
                    'text': [
                        text
                    ]
                }
            }
        ]
    }
} 

def nearest_location_template(zip_code, address) -> str:
    # Page - Provide Vaccine Location
    # text = f"The nearest medical center to {zip_code} is {address}. Would you like me to text you the address?"
    text = f"Please give me a moment while I locate the nearest VA medical center.\nThe nearest medical center to {' '.join(str(zip_code))} is {address}. Would you like me to send this information to you via text message?"
    ssml = f'Please give me a moment while I locate the nearest VA medical center.  The nearest medical center to <say-as interpret-as="verbatim">{" ".join(str(zip_code))}</say-as> is {address}. Would you like me to send this information to you via text message?'    
    # resp: dict = text_response(text)
    resp: dict = text_and_ssml_response(text, ssml)
    print(resp)
    return resp

def text_nearest_template(phone_number) -> str:
    phone_number = f'({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}'
    text = f"No problem, we've sent a text message to {phone_number}"
    ssml = f"No problem, we've sent a text message to {phone_number}"
    resp = text_and_ssml_response(text, ssml)
    print(resp)
    return resp

def resp_next_nearest_template(next_nearest, zip_code) -> str:
    # Page - Provide Alternate Location
    # text = f"The next nearest medical center to you is {next_nearest}. Would you like me to text you the address?"
    text = f"Sure. The next nearest medical center to {' '.join(str(zip_code))} is {next_nearest}. Would you like me to send this information to you via text message?"
    ssml = f"Sure. The next nearest medical center to {' '.join(str(zip_code))} is {next_nearest}. Would you like me to send this information to you via text message?"
    resp = text_and_ssml_response(text, ssml)
    print(resp)
    return resp

def text_next_nearest_template(phone_number) -> str: 
    # Page - Confirm sms and schedule appointment
    phone_number = f'({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}'
    # text = f"No problem, we've sent you the next nearest address to {phone_number}"
    text = f"Thank you, the facility address has been sent to {phone_number}.\nWould you like to schedule an appointment?"
    resp = text_response(text)
    return resp

def user_authenticated_template(user: dict) -> str:
    name = user['First Name'] + ' ' + user['Last Name']
    status = user['Claim Status']
    # text = f'The user is: {name}.  The status is {status}.'
    text = f"Thank you {user['First Name']}. You are now authenticated and I am currently accessing the Central Scheduling System.  I see that you have received the first dose."
    resp: dict = text_response(text)
    return resp

def resp_set_appt_template(current_address, date, time):
    text = f"Thank you. I now have your second covid vaccination scheduled for {date} {time} at the {current_address} location. Would you like to receive a confirmation of the appointment via text message?"
    ssml = f'Thank you. I now have your second covid vaccination scheduled for <say-as interpret-as="date" format="yyyymmdd" detail="1">{date}</say-as> <say-as interpret-as="time" format="hms12">{time}</say-as> at the {current_address} location. Would you like to receive a confirmation of the appointment via text message?'
    resp: dict = text_and_ssml_response(text, ssml)
    return resp

def resp_text_appt_template(phone_number, current_address, date, time):
    phone_number = f'({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}'
    text = f'Your appointment is confirmed for {date} {time} at the {current_address} location.'
    ssml = f'Your appointment is confirmed for <say-as interpret-as="date" format="yyyymmdd" detail="1">{date}</say-as> <say-as interpret-as="time" format="hms12">{time}</say-as> at the {current_address} location.'
    resp = text_and_ssml_response(text, ssml)
    return resp

def resp_get_ticket_template(user: dict) -> str:
    text = f"Thank you, {user['First Name']}. The VA received your {user['Claim Type']} claim  on {user['Claim Filed Date']}. The status of your claim is {user['Claim Status']}. What else can I help you with?"
    ssml = text
    resp = text_and_ssml_response(text, ssml)
    return resp
