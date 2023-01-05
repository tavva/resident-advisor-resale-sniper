import os
import sys
import time
import argparse
import datetime
import requests
import subprocess
import clicksend_client
from clicksend_client import SmsMessage
from clicksend_client.rest import ApiException

import urllib.request
import urllib.parse

from fake_useragent import UserAgent

parser = argparse.ArgumentParser(
    description="Poll a given Resident Advisor URL and notify if resale tickets are available.",
)
parser.add_argument('url', help="Resident Advisor event page URL")
args = parser.parse_args()

CLICKSEND_USERNAME = os.getenv('CLICKSEND_USERNAME')
CLICKSEND_PASSWORD = os.getenv('CLICKSEND_PASSWORD')
PHONE_NUMBER = os.getenv('PHONE_NUMBER')

headers = {'User-Agent': UserAgent().chrome}

# Configure HTTP basic authorization: BasicAuth
configuration = clicksend_client.Configuration()
configuration.username = CLICKSEND_USERNAME
configuration.password = CLICKSEND_PASSWORD

# create an instance of the API class
api_instance = clicksend_client.SMSApi(clicksend_client.ApiClient(configuration))

def send_sms(message):
    sms_message = SmsMessage(
        source="python",
        body="This is a tst",
        to=PHONE_NUMBER,
    )

    sms_messages = clicksend_client.SmsMessageCollection(messages=[sms_message])

    try:
        # Send sms message(s)
        api_response = api_instance.sms_send_post(sms_messages)
        print(api_response)
    except ApiException as e:
        print("Exception when calling SMSApi->sms_send_post: %s\n" % e)

text_sent = False
while True:
    response = requests.get(args.url, headers=headers)

    tickets_available = not "Check back to purchase tickets as they become available." in response.text

    if tickets_available:
        print("%s: Tickets available for %s" % (str(datetime.datetime.now()), args.url))

        if not text_sent:
            send_sms("Tickets available! %s" % args.url)
            text_sent = True
    else:
        print("%s: Tickets not available." % (str(datetime.datetime.now()),))

    time.sleep(20)