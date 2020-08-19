import telnyx
import os
import base64
import json
from flask import Flask, request, Response
from dotenv import load_dotenv
from ivr import IVR



def open_IVR_config_json(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)
        return data

ivr_config = open_IVR_config_json('ivrConfig.json')
my_ivr = IVR(intro = ivr_config['intro'],
            iterable = ivr_config['iterable'],
            items = ivr_config['items'])

app = Flask(__name__)

@app.route('/Callbacks/Voice/Inbound', methods=['POST'])
def respond():
    global my_ivr
    # Get the data from the request
    data = request.json.get('data')
    # print(data) For testing purposes, you could print out the data object received
    # Check record_type
    if data.get('record_type') == 'event':
        # Check event type
        event = data.get('event_type')


        # print(event, flush=True) For testing purposes you can print out the event if you'd like
        call_control_id = data.get('payload').get('call_control_id')
        my_call = telnyx.Call()
        my_call.call_control_id = call_control_id
        if event == 'call.initiated':
            direction = data.get('payload').get('direction')
            if (direction == 'incoming'):
                encoded_client_state = base64.b64encode(direction.encode('ascii'))
                client_state_str = str(encoded_client_state, 'utf-8')
                res = my_call.answer(client_state=client_state_str)
                print(res, flush=True)

        # When the call is answered, initiate gather_using_speak
        elif event == 'call.answered':
            client_state = data.get('payload').get('client_state')
            if (client_state):
                speak_str = my_ivr.get_prompt()
                res = my_call.gather_using_speak(
                    payload=speak_str,
                    valid_digits=my_ivr.get_valid_digits(),
                    language = 'en-US',
                    voice = 'male')
                print(res, flush=True);

        # When gather is ended, collect the digit pressed and speak them
        elif event == 'call.gather.ended':
            digits_pressed = data.get('payload').get('digits')
            phone_number_lookup = my_ivr.get_phone_number_from_digit(digits_pressed)
            if (phone_number_lookup):
                to = phone_number_lookup
                res = my_call.transfer(to=to)
                print(res, flush=True)
    #print(request.json, flush=True); For testing purposes, you can print out the entire json received

    return Response(status=200)

if __name__ == '__main__':
    ## pythonic?
    load_dotenv()
    telnyx.api_key = os.getenv('TELNYX_API_KEY')
    app.run(port=8000)
