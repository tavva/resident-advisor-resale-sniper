import sys
import time
import datetime
import requests
import subprocess

from lxml import html

url = sys.argv[1]

while True:
    response = requests.get(url)
    root = html.document_fromstring(response.content)

    tickets_with_resale = root.xpath('//li[@id="tickets"]/ul/li[@data-resale-tickets-available > 0]')

    if len(tickets_with_resale) > 0:
        print("%s: Tickets available for %s" % (str(datetime.datetime.now()), url))
        subprocess.Popen(['notify-send', "Tickets available"])

    time.sleep(10)
