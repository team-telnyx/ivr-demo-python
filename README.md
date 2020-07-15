# IVR Demo Code
A simple demo project to demonstrate an IVR application using Python, Flask, and the Telnyx SDK

## Tutorial

Make sure to check out the corresponding tutorial [here](https://developers.telnyx.com/docs/v2/call-control/tutorials/ivr-demo?lang=python) on the [Telnyx Docs](https://developers.telnyx.com/docs)

## Troubleshooting

- Ensure that you have set the FLASK_APP variable with your main.py file so that `flask run` can find it
- Make sure that you add the correct webhook url to the Telnyx Developer Console. It changes every time you re-run `ngrok http 5000`
- Make sure you are up to date with the latest Telnyx Python SDK
