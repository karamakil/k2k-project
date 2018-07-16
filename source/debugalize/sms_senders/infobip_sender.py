#https://github.com/infobip/infobip-api-python-client
from infobip import clients
from infobip.util.configuration import Configuration
from infobip.api.model.sms.mt.send.textual.SMSTextualRequest import SMSTextualRequest

'''
InfoBip SMS Sender Integration,
you need to add the following to the settings file
INFOBIP_USERNAME = ''
INFOBIP_PASSWORD = ''
'''
class infobip_sender:
    
    def __init__(self, username, password):
        self.send_sms_client = clients.send_single_textual_sms(Configuration("https://api.infobip.com", username, password))
    
    def send(self, phone_number, message_text):
        """
        Send sms using infobip api 
        @param phone_number: phone number to send sms 
        @param message_text: text message content
        @return: True if succeeded, else False
        """
        
        result = False
        request = SMSTextualRequest()
        request.text = message_text
        request.to = [phone_number]
        response = self.send_sms_client.execute(request)           
        if not response.messages[0].status.action:
            result = True
            
        return result