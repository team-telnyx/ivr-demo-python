import telnyx
import os
from flask import Flask, request, Response
from dotenv import load_dotenv
import base64
load_dotenv()

class Phone_number_response:
    def __init__(self, valid, phone_number=''):
        self.valid = valid
        self.phone_number = phone_number

class IVR_Controller:
    def __init__(self, config):
        self.intro = config['intro']
        self.iterable = config['iterable']
        self.items = config['items']
        self.phone_number_table = {}
        self.valid_inputs = ''
        self.prompt = self.intro
        self._build_ivr()

    def get_prompt(self):
        return self.prompt

    def get_valid_digits(self):
        return self.valid_inputs

    def _build_ivr(self):
        length = len(self.items)
        for i in range(length):
            context = self.items[i]['context']
            phone_number = self.items[i]['phone number']
            digit = str(i+1)
            prompt = self._fill_iterable(context, digit)
            self.prompt = f'{self.prompt}, {prompt}'
            self.phone_number_table[digit] = phone_number
            self.valid_inputs = f'{self.valid_inputs}{digit}'

    def get_phone_number_from_digit(self, digit):
        if (digit in self.phone_number_table):
            return Phone_number_response(True, self.phone_number_table[digit])
        else:
            return Phone_number_response(False)

    def _fill_iterable(self, context, digit):
        return self.iterable % (context, digit)


IVR_Config = {
    'intro': 'Thank you for calling the Weather Hotline.',
    'iterable': 'For weather in %s press %s',
    'items':  [
        {
            'context': 'Chicago, Illinois',
            'phone number': '+18158340675'
        },
        {
            'context': 'Raleigh, North Carolina',
            'phone number': '+19193261052'
        }
    ]
}

my_ivr = IVR_Controller(IVR_Config)

telnyx.api_key = os.getenv('TELNYX_API_KEY')

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
        # When call is initiated, add the call control id to the my_ivr object
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
            if (phone_number_lookup.valid):
                to = phone_number_lookup.phone_number
                res = my_call.transfer(to=to)
                print(res, flush=True)
    #print(request.json, flush=True); For testing purposes, you can print out the entire json received

    return Response(status=200)

if __name__ == '__main__':
    app.run()
