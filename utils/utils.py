import datetime
import threading
import http.client
import json
import random
import uuid
from django.conf import settings
import requests
import json
import base64
import bcrypt
import secrets


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


class UniqueOtpGenerator:
    def __init__(self):
        self.generated_otps = set()

    def generate_otp(self):
        while True:
            otp = random.randint(10000000, 99999999)
            if otp not in self.generated_otps:
                self.generated_otps.add(otp)
                return otp


def generate_random_id():
    return str(uuid.uuid4())[:20].replace("-", "").lower()


def airtime_checksum(service_id, request_amount, recipient):
    login_id = settings.LOGIN_ID
    private_key = settings.PRIVATE_KEY
    request_id = generate_random_id()
    concat_string = f"{login_id}|{request_id}|{service_id}|{request_amount}|{private_key}|{recipient}"
    hashed = bcrypt.hashpw(concat_string.encode("utf-8"), bcrypt.gensalt())
    checksum = base64.urlsafe_b64encode(hashed).decode("utf-8")

    return checksum, request_id


class CreditSwitch(object):
    def __init__(self, base_url):
        self.base_url = "http://176.58.99.160:9012/api/v1"
        self.headers = {
            "Content-Type": "application/json",
        }

    def make_request(self, endpoint, payload):
        url = f"{self.base_url}/{endpoint}/"
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        return response.json()

    def purchase_airtime(self, service_id, amount, recipient):
        checksum, request_id = airtime_checksum(service_id, amount, recipient)
        date_now = datetime.datetime.utcnow().strftime("%d-%b-%Y %H:%M GMT")

        payload = {
            "loginId": settings.LOGIN_ID,
            "key": settings.PUBLIC_KEY,
            "requestId": request_id,
            "serviceId": service_id,
            "amount": str(amount),  # Convert Decimal to string
            "recipient": recipient,
            "date": date_now,
            "checksum": checksum,
        }
        print(
            "payload",
            payload["checksum"],
        )

        return self.make_request("purchase_airtime", payload)


# afripoint = AfripointConsult()
# response = afripoint.post("payments", params=json.dumps(params)).json()

# print("Afripoint Consult: ", response)

# if response["status"] == "success":
#     afripoint_redirect_link = response["data"]["link"]
#     return HttpResponse(
#         status=204, headers={"HX-Redirect": afripoint_redirect_link}
#     )
# else:
#     messages.add_message(
#         request, messages.ERROR, "Payment gateway is not responding."
#     )
