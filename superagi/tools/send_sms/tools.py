import time
from typing import Type
from pydantic import BaseModel, Field
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from superagi.tools.base_tool import BaseTool



class SMSInput(BaseModel):
    to: str = Field(..., description="Phone number of the receiver, default it's +40729789449")
    # from_: str = Field(..., description="From who is the SMS sent,default is +16183614195")
    body: str = Field(..., description="The message that needs to be sent in SMS")


class SMSTool(BaseTool):
    name = "Send SMS"
    args_schema: Type[SMSInput] = SMSInput
    description  = "Send an SMS to a phone number"   
    # client.messages.create(
    #     to="+15558675310",
    #     from_="+15017122661",
    #     body="This is the ship that made the Kessel Run in fourteen parsecs?"
    # )
 
    def _execute(self, to: str, body: str) -> str:
   
        account_sid = "AC4ef0adcf797825207590f30f82e5c54a"
        auth_token = "cfea53a12cfa835d9baaededc33aacff"
        
        client = Client(account_sid, auth_token)
        
        # to_numbers = ["+40756544550", "+40743500656", "+40729789449", "+40740149416"]
        
        to_numbers = []
        for number in to.split(","):
            formatted_number = "+" + number.strip()
            to_numbers.append(formatted_number)
        
        for to_number in to_numbers:
            client.messages.create(
            to=to_number,
            from_="+16183614195",
            body=body
            )
         # Make a call and play a text-to-speech message
        # client.calls.create(
        #         twiml=self._generate_twiml_message(),
        #         to="+40768689196",
        #         from_="+16183614195",
        #         record=True
        #  )

        return f"SMS-ul a fost trimis cu succes catre {to}"
  