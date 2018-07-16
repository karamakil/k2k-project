#https://pypi.python.org/pypi/django-nexmo/1.0.0
from nexmo import send_message

'''
Nexmo SMS Sender Integration,
you need to add the following to the settings file

NEXMO_USERNAME = ''
NEXMO_PASSWORD = ''
NEXMO_FROM = ''
'''
     
def send(phone_number, message_text):
    """
    send sms using nexmo api 
    @param phone_number: phone number to send sms 
    @param message_text: text message content
    @return: True if succeeded, else False
    """
    result = False
    #stop sending to USA numbers from nexmo
    if phone_number.startswith('+1'):
        return result
    
    response = send_message(to = phone_number, message = message_text)
    if response['messages'][0]['status'] == '0':
        result = True
    return result