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
        # "Authorization": "App be84566f9b9482cf4a032e2fb5ff0329-54f2cfa2-dfec-4626-acb9-04c47c973c27",
        "Authorization": "App 3df98d304005e2af8be66e75da70e9d1-3a6bfd6c-dc94-4200-bd34-0caaa778543c",
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


def merchant_info_checksum():
    login_id = settings.LOGIN_ID
    private_key = settings.PRIVATE_KEY
    concat_string = f"{login_id}|{private_key}"
    hashed = bcrypt.hashpw(concat_string.encode("utf-8"), bcrypt.gensalt())
    checksum = base64.urlsafe_b64encode(hashed).decode("utf-8")

    return checksum


def multichoice_validate_customer_checksum(customer_no):
    login_id = settings.LOGIN_ID
    private_key = settings.PRIVATE_KEY
    concat_string = f"{login_id}|{private_key}|{customer_no}"
    hashed = bcrypt.hashpw(concat_string.encode("utf-8"), bcrypt.gensalt())
    checksum = base64.urlsafe_b64encode(hashed).decode("utf-8")

    return checksum


def multichoice_vend_checksum(customer_no, amount):
    login_id = settings.LOGIN_ID
    private_key = settings.PRIVATE_KEY
    transactionref = generate_random_id()
    concat_string = f"{login_id}|{private_key}|{customer_no}|{transactionref}|{amount}"
    hashed = bcrypt.hashpw(concat_string.encode("utf-8"), bcrypt.gensalt())
    checksum = base64.urlsafe_b64encode(hashed).decode("utf-8")

    return checksum, transactionref


def electricity_validate_request_checksum(service_id, customer_account_id):
    login_id = settings.LOGIN_ID
    private_key = settings.PRIVATE_KEY
    concat_string = f"{login_id}|{service_id}|{private_key}|{customer_account_id}"
    hashed = bcrypt.hashpw(concat_string.encode("utf-8"), bcrypt.gensalt())
    checksum = base64.urlsafe_b64encode(hashed).decode("utf-8")

    return checksum


def electricity_purchase_checksum(service_id, customer_account_id, amount):
    login_id = settings.LOGIN_ID
    private_key = settings.PRIVATE_KEY
    request_id = generate_random_id()
    concat_string = f"{login_id}|{service_id}|{private_key}|{customer_account_id}|{request_id}|{amount}"
    hashed = bcrypt.hashpw(concat_string.encode("utf-8"), bcrypt.gensalt())
    checksum = base64.urlsafe_b64encode(hashed).decode("utf-8")

    return checksum


class CreditSwitch(object):
    def __init__(self):
        self.base_url = "http://176.58.99.160:9012/api/v1"
        self.headers = {
            "Content-Type": "application/json",
        }

    def make_post_request(self, endpoint, payload):
        url = f"{self.base_url}/{endpoint}/"
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        return response.json()

    def make_get_request(self, endpoint, payload):
        url = f"{self.base_url}/{endpoint}/"
        response = requests.get(url, headers=self.headers, data=json.dumps(payload))
        return response.json()

    def purchase_airtime(self, service_id, amount, recipient):
        checksum, request_id = airtime_checksum(service_id, amount, recipient)
        date_now = datetime.datetime.now().strftime("%d-%b-%Y %H:%M GMT")

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

        return self.make_post_request("mvend", payload)

    def purchase_data(self, service_id, amount, recipient, product_id):
        checksum, request_id = airtime_checksum(service_id, amount, recipient)
        date_now = datetime.datetime.now().strftime("%d-%b-%Y %H:%M GMT")

        payload = {
            "loginId": settings.LOGIN_ID,
            "key": settings.PUBLIC_KEY,
            "requestId": request_id,
            "serviceId": service_id,
            "productId": product_id,
            "amount": str(amount),  # Convert Decimal to string
            "recipient": recipient,
            "date": date_now,
            "checksum": checksum,
        }

        return self.make_post_request("dvend", payload)

    def merchant_details(self):
        checksum = merchant_info_checksum()
        payload = {
            "loginId": settings.LOGIN_ID,
            "key": settings.PUBLIC_KEY,
            "checksum": checksum,
        }

        return self.make_post_request("mdetails", payload)

    def purchase_multichoice_product(
        self,
        service_id,
        amount,
        customer_no,
        customer_name,
        products_codes,
        invoice_period,
    ):
        checksum, transactionref = multichoice_vend_checksum(customer_no, amount)

        payload = {
            "loginId": settings.LOGIN_ID,
            "key": settings.PUBLIC_KEY,
            "transactionRef": transactionref,
            "serviceId": service_id,
            "customerNo": customer_no,
            "amount": str(amount),  # Convert Decimal to string
            "customerName": customer_name,
            "productsCodes": products_codes,
            "checksum": checksum,
            "invoicePeriod": invoice_period,
        }

        return self.make_post_request("cabletv/multichoice/vend", payload)

    def multichoice_validate_customer_number(self, customer_no, service_id):
        checksum = multichoice_validate_customer_checksum(customer_no)

        payload = {
            "loginId": settings.LOGIN_ID,
            "key": settings.PUBLIC_KEY,
            "checksum": checksum,
            "customerNo": customer_no,
            "serviceId": service_id,
        }

        return self.make_post_request("cabletv/multichoice/validate", payload)

    def transaction_status(self, service_id):
        payload = {
            "loginId": settings.LOGIN_ID,
            "key": settings.PUBLIC_KEY,
            "serviceId": service_id,
            "requestId": "d777df15bdfe40f49",
        }

        return self.make_get_request("requery", payload)

    def data_plans(self, service_id):

        payload = {
            "loginId": settings.LOGIN_ID,
            "key": settings.PUBLIC_KEY,
            "serviceId": service_id,
        }

        return self.make_post_request("mdataplans", payload)

    def showmax(self):
        payload = {
            "loginId": settings.LOGIN_ID,
            "key": settings.PUBLIC_KEY,
        }

        return self.make_get_request("showmax/packages/", payload)

    def startimes(self):
        payload = {
            "loginId": settings.LOGIN_ID,
            "key": settings.PUBLIC_KEY,
        }

        return self.make_post_request("startimes/fetchProductList/", payload)

    def showmax_recharge(
        self,
        service_id,
        amount,
        subscriptionType,
        customerNo,
        invoicePeriod,
        packageName,
    ):
        request_id = generate_random_id()
        payload = {
            "loginId": settings.LOGIN_ID,
            "key": settings.PUBLIC_KEY,
            "requestId": request_id,
            "serviceId": service_id,
            "customerNo": customerNo,
            "amount": str(amount),  # Convert Decimal to string
            "subscriptionType": subscriptionType,
            "invoicePeriod": invoicePeriod,
            "packageName": packageName,
        }

        return self.make_post_request("showmax/pay", payload)

    def multichoice_product_codes(self, service_id):

        payload = {
            "loginId": settings.LOGIN_ID,
            "key": settings.PUBLIC_KEY,
            "serviceId": service_id,
        }

        return self.make_post_request("cabletv/multichoice/fetchproducts", payload)

    def multichoice_product_addons(self, service_id):

        payload = {
            "loginId": settings.LOGIN_ID,
            "key": settings.PUBLIC_KEY,
            "serviceId": service_id,
        }

        return self.make_post_request("cabletv/multichoice/productaddons", payload)

    def electricity_validate_request(self, service_id, customer_account_id):
        checksum = electricity_validate_request_checksum(
            service_id, customer_account_id
        )

        payload = {
            "loginId": settings.LOGIN_ID,
            "key": settings.PUBLIC_KEY,
            "checksum": checksum,
            "customerAccountId": customer_account_id,
            "serviceId": service_id,
        }

        return self.make_post_request("evalidate", payload)

    def electricity_validate_request(self, service_id, customer_account_id):
        checksum = electricity_validate_request_checksum(
            service_id, customer_account_id
        )

        payload = {
            "loginId": settings.LOGIN_ID,
            "key": settings.PUBLIC_KEY,
            "checksum": checksum,
            "customerAccountId": customer_account_id,
            "serviceId": service_id,
        }

        return self.make_post_request("evalidate", payload)

    def electricity_purchase(
        self, service_id, customer_account_id, amount, customer_name, customer_address
    ):
        checksum = electricity_purchase_checksum(
            service_id,
            customer_account_id,
            amount,
        )

        request_id = generate_random_id()

        payload = {
            "loginId": settings.LOGIN_ID,
            "key": settings.PUBLIC_KEY,
            "checksum": checksum,
            "customerAccountId": customer_account_id,
            "serviceId": service_id,
            "amount": amount,
            "customerName": customer_name,
            "customerAddress": customer_address,
            "requestId": request_id,
        }

        return self.make_post_request("evend", payload)
