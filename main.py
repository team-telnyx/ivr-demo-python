import telnyx
from flask import Flask, request, Response


telnyx.api_key = "YOUR_API_KEY"

app = Flask(__name__)

class my_IVR_info:
    call_control_id: ''
    client_state: ''

my_ivr = my_IVR_info()

@app.route('/webhook', methods=['POST'])
def respond():

    # Activate global variable within function
    global my_ivr

    # Get the data from the request
    data = request.json
    # print(data) For testing purposes, you could print out the data object received

    # Check record_type
    if data.get('record_type') == 'event':
        # Check event type
        event = data.get('event_type')
        # print(event, flush=True) For testing purposes you can print out the event if you'd like

        # When call is initiated, add the call control id to the my_ivr object
        if event == "call_initiated":
            my_ivr.call_control_id = data.get('payload').get('call_control_id')
            
            # Answer the call
            print(telnyx.Call.answer(my_ivr), flush=True)

        # When the call is answered, initiate gather_using_speak
        elif event == "call_answered":
            print(telnyx.Call.gather_using_speak(my_ivr, payload="Press 1 to record a voicemail or 2 to have the application hang up", valid_digits="12", language = "en-US", voice = "male"), flush=True)
        
        # When gather is ended, collect the digit pressed and speak them
        elif event == "gather_ended":
            speak_str = "The digits you pressed were" + " ".join(data.get('payload').get('digits'))
            print(telnyx.Call.speak(my_ivr, payload=speak_str, language = "en-US", voice = "male"), flush=True)

        # Each time a dtmf signal is received, repeat it back to the user
        elif event == "dtmf":
            # Extract the digit pressed from the data object
            digit = data.get('payload').get('digit')

            # Construct the string to be spoken based on the digit
            speak_str = "You pressed " + digit

            # Initiate speak
            print(telnyx.Call.speak(my_ivr, payload=speak_str, language = "en-US", voice = "male"), flush=True)

    #print(request.json, flush=True); For testing purposes, you can print out the entire json received
    
    return Response(status=200)