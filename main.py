import telnyx
from flask import Flask, request, Response


telnyx.api_key = "KEY01727BBFDD0BB2A5B12F723A5EC5B2D8_j4SJ4HzNw0gf4dwtsmDb3P"

app = Flask(__name__)

class my_IVR_info:
    call_control_id: ''
    client_state: ''

my_ivr = my_IVR_info()

@app.route('/webhook', methods=['POST'])
def respond():
    global my_ivr
    data = request.json
    if data.get('record_type') == 'event':

        event = data.get('event_type')
        print(event, flush=True)
        if event == "call_initiated":
            my_ivr.call_control_id = data.get('payload').get('call_control_id')
            print(telnyx.Call.answer(my_ivr), flush=True)
        elif event == "call_answered":
            print(telnyx.Call.gather_using_speak(my_ivr, payload="Press 1 to record a voicemail or 2 to have the application hang up", valid_digits="12", language = "en-US", voice = "male"), flush=True)
        elif event == "gather_ended":
            speak_str = "The digits you pressed were" + " ".join(data.get('payload').get('digits'))
            print(telnyx.Call.speak(my_ivr, payload=speak_str, language = "en-US", voice = "male"), flush=True)

    #print(request.json, flush=True);
    return Response(status=200)

def start_conference():
    print('hi', flush=True)

def main():
    ''' get input '''
    user_input = ""

    while user_input != "quit":
        user_input = input('Command: ')
        print(user_input)
        if user_input == "start":
            start_conference()


# Main Execution

if __name__ == '__main__':
    main()
