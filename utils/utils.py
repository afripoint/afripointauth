import threading
import http.client
import json

# from infobip_channels.sms.channel import SMSChannel
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy as _


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.fail_silently = False
        self.email.send()


def send_html_email(subject, body, from_email=None, to_email=None):
    email = EmailMessage(subject, body, from_email, to_email)
    email.content_subtype = "html"
    EmailThread(email).start()


def infobip_send_sms(phone_number, message):
    conn = http.client.HTTPSConnection("432n2n.api.infobip.com")
    payload = json.dumps(
        {
            "messages": [
                {
                    "destinations": [{"to": phone_number}],
                    "from": "ServiceSMS",
                    "text": message,
                }
            ]
        }
    )
    headers = {
        "Authorization": "App be84566f9b9482cf4a032e2fb5ff0329-54f2cfa2-dfec-4626-acb9-04c47c973c27",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    conn.request("POST", "/sms/2/text/advanced", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
