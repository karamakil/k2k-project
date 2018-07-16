#https://github.com/clickatell/clickatell-python
from clickatell.http import Http

'''
Clickatell SMS Sender Integration,
you need to add the following to the settings file
CLICKATELL_USERNAME = ''
CLICKATELL_PASSWORD = ''
CLICKATELL_API_ID = ''
'''

class clickatell_sender:
    def __init__(self, username, password, api_id):
        self.clickatell = Http(username, password, api_id)
        
    def send(self, phone_number, message_text):
        """
        Send sms using clickatell api 
        @param phone_number: phone number to send sms 
        @param message_text: text message content
        @return: True if succeeded, else False
        """
        
        response = self.clickatell.sendMessage([phone_number], message_text)
        return response[0]['error']