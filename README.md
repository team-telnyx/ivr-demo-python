<div align="center">

# Telnyx Python IVR Demo Code

![Telnyx](logo-dark.png)

A simple demo project to demonstrate an IVR application using Python, Flask, and the Telnyx SDK

</div>

## Documentation & Tutorial

The full documentation and tutorial is available on [developers.telnyx.com](https://developers.telnyx.com/docs/v2/call-control/tutorials/ivr-demo?lang=python&utm_source=referral&utm_medium=github_referral&utm_campaign=cross-site-link)

## Pre-Reqs

You will need to set up:

* [Telnyx Account](https://telnyx.com/sign-up?utm_source=referral&utm_medium=github_referral&utm_campaign=cross-site-link)
* [Telnyx Phone Number](https://portal.telnyx.com/#/app/numbers/my-numbers?utm_source=referral&utm_medium=github_referral&utm_campaign=cross-site-link) enabled with:
  * [Telnyx Call Control Application](https://portal.telnyx.com/#/app/call-control/applications?utm_source=referral&utm_medium=github_referral&utm_campaign=cross-site-link)
  * [Telnyx Outbound Voice Profile](https://portal.telnyx.com/#/app/outbound-profiles?utm_source=referral&utm_medium=github_referral&utm_campaign=cross-site-link)
* [Python 3](https://www.python.org/) installed with [PIP](https://pypi.org/project/pip/)
* Ability to receive webhooks (with something like [ngrok](https://developers.telnyx.com/docs/v2/development/ngrok?utm_source=referral&utm_medium=github_referral&utm_campaign=cross-site-link))

## Usage

The following environmental variables need to be set

| Variable            | Description                                                                                                                                              |
|:--------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `TELNYX_API_KEY`    | Your [Telnyx API Key](https://portal.telnyx.com/#/app/api-keys?utm_source=referral&utm_medium=github_referral&utm_campaign=cross-site-link)              |
| `TELNYX_PUBLIC_KEY` | Your [Telnyx Public Key](https://portal.telnyx.com/#/app/account/public-key?utm_source=referral&utm_medium=github_referral&utm_campaign=cross-site-link) |

### .env file

This app uses the excellent [python-dotenv](https://github.com/theskumar/python-dotenv) package to manage environment variables.

Make a copy of [`.env.sample`](./.env.sample) and save as `.env` **📁 in the root directory** and update the variables to match your creds.

```
TELNYX_API_KEY=
TELNYX_PUBLIC_KEY=
```

### Callback URLs For Telnyx Call Control Applications

| Callback Type          | URL                                   |
|:-----------------------|:--------------------------------------|
| Inbound Voice Callback | `{ngrok-url}/Callbacks/Voice/Inbound` |

### Install

Run the following commands to get started

```
pip install -r requirements.txt
```

### Ngrok

This application uses Flask's built in server serving on port 5000. Be sure to route inbound requests to port 5000

```
./ngrok http 5000
```

> Terminal should look _something_ like

```
ngrok by @inconshreveable                                                                                                                               (Ctrl+C to quit)

Session Status                online
Account                       Little Bobby Tables (Plan: Free)
Version                       2.3.35
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://your-url.ngrok.io -> http://localhost:5000
Forwarding                    https://your-url.ngrok.io -> http://localhost:5000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

At this point you can point your call control application to generated ngrok URL + path  (Example: `http://{your-url}.ngrok.io/Callbacks/Voice/Inbound`).

### Run

Run the app with the Flask servering on port 5000

```
python app.py
```

### Call your number

You can now call your Telnyx phone number and listen to the weather hotline. You can make your selection and will be transfered to the National Weather Service for that city.

### Adding more cities

To change or add see the [Dial-a-forecast](https://www.weather.gov/dial-a-forecast/) website.

You can add more selections to the `ivrConfig.json` file in the `items` array. The app easily supports up to 9 total selections (mapping to DTMF button presses of 1-9).

```json
{
    "intro": "Thank you for calling the Weather Hotline.",
    "iterable": "For weather in %s press %s",
    "items":  [
        {
            "itemName": "Chicago, Illinois",
            "phoneNumber": "+18158340675"
        },
        {
            "itemName": "Raleigh, North Carolina",
            "phoneNumber": "+19193261052"
        }
    ]
}
```

To add a new item to the list add a new object to the items with two key/value pairs, the `itemName` is spoken to the user and the phoneNumber is the transferred destination.  The app will rebuild the IVR next launch.

```json
{
  "itemName": "Denver, Colorado",
  "phoneNumber": "+13034944221"
}
```


