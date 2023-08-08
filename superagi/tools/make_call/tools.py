import time
from typing import Type
import requests
import openai

from pydantic import BaseModel, Field
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
from superagi.tools.base_tool import BaseTool

class CALLInput(BaseModel):
    to: str = Field(..., description="Phone number of the receiver, default it's +40729789449")
    # from_: str = Field(..., description="From who is the SMS sent,default is +16183614195")
    body: str = Field(..., description="The message that needs to be sent in SMS")

class CALLTool(BaseTool):
    name = "DIMA CALL"
    args_schema: Type[CALLInput] = CALLInput
    description = "Make a phone call"

    def _execute(self, to: str, body: str) -> str:

        account_sid = "AC4ef0adcf797825207590f30f82e5c54a"
        auth_token = "cfea53a12cfa835d9baaededc33aacff"
        


        client = Client(account_sid, auth_token)

        # Generate TwiML to say a message and then gather the response
        body_encoded = body.replace(' ', '%20')  # Replace spaces with '%20' for URL encoding
        response = VoiceResponse()
        gather = Gather(action='https://convo-gpt-5593.twil.io/transcribe?body=' + body_encoded, input='speech')
        gather.say(body)
        response.append(gather)
        twiml_message = str(response)

        # Make a call and play a text-to-speech message
        call = client.calls.create(
            twiml=twiml_message,
            to=to,
            from_="+16183614195",
            record=True
        )

        # Save the call SID
        call_sid = call.sid

        # Wait for the call to be completed
        while True:
            call = client.calls(call_sid).fetch()
            if call.status == 'completed':
                break
            time.sleep(1)  # Wait for 1 second before checking again

        # Get the recording URL
        recordings = client.recordings.list(call_sid=call_sid)
        if recordings:
            recording_url = f"https://api.twilio.com{recordings[0].uri[:-5]}.mp3"
            audio_player = f'<audio controls src="{recording_url}"></audio>'
            # transcript = openai.Audio.transcribe("whisper-1", recording_url)
        else:
            recording_url = "There is no recording"
            audio_player = ""

        return f"Am finalizat apelul catre {to} cu <b>SUCCES</b>. Recording URL:<audio controls src='{recording_url}'></audio></br> <a target='_blank' href='{recording_url}'>Apasa aici</a>. Transcription: soon"
