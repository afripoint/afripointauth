import threading

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
