from twilio.rest import Client

ACCOUNT_SID = 'AC99b6074fd1d43e6918348ccf18cb47e3'
AUTH_TOKEN = 'a5aaa6b4721f53a445ac8f23228cefcb'

messaging = Client(ACCOUNT_SID, AUTH_TOKEN)

message = messaging.messages.create(
    body='Hey Tony, its Yvan.  Dont respond - I wont get the message...', 
    from_='+18448805679', 
    to=['+17145854165', '+17862511624']
)

print(message.sid)