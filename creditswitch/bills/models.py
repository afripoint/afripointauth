from django.db import models

AIRTIME_PROVIDER = (
    ("Airtel", "Airtel"),
    ("MTN", "MTN"),
    ("9-Mobile", "9-Mobile"),
    ("Globacom", "Globacom"),
)


DATA = (
    ("Airtel", "Airtel"),
    ("9-Mobile", "9-Mobile"),
    ("Globacom", "Globacom"),
    ("Globacom", "Globacom"),
    ("Smile", "Smile"),
    ("NTEL", "NTEL"),
)


ELECTRICITY = (
    (
        "Ikeja Electric Disco (Prepaid Accounts)",
        "Ikeja Electric Disco (Prepaid Accounts)",
    ),
    ("Ikeja Electric Disco (Post Accounts)", "Ikeja Electric Disco (Post Accounts)"),
    (
        "Ibadan Electric Disco (Prepaid Accounts)",
        "Ibadan Electric Disco (Prepaid Accounts)",
    ),
    (
        "Ibadan Electric Disco (Postpaid Accounts)",
        "Ibadan Electric Disco (Postpaid Accounts)",
    ),
    ("Eko Electric Disco (Prepaid Accounts)", "Eko Electric Disco (Prepaid Accounts)"),
    (
        "Eko Electric Disco (Postpaid Accounts)",
        "Eko Electric Disco (Postpaid Accounts)",
    ),
    (
        "Abuja Electric Disco (Prepaid Accounts)",
        "Abuja Electric Disco (Prepaid Accounts)",
    ),
    (
        "Abuja Electric Disco (Postpaid Accounts)",
        "Abuja Electric Disco (Postpaid Accounts)",
    ),
    (
        "Port Harcourt Electric Disco (Prepaid Accounts)",
        "Port Harcourt Electric Disco (Prepaid Accounts)",
    ),
    (
        "Port Harcourt Electric Disco (Postpaid Accounts)",
        "Port Harcourt Electric Disco (Postpaid Accounts)",
    ),
    (
        "Kaduna Electric Disco (Prepaid Accounts)",
        "Kaduna Electric Disco (Prepaid Accounts)",
    ),
    (
        "Kaduna Electric Disco (Postpaid Accounts)",
        "Kaduna Electric Disco (Postpaid Accounts)",
    ),
    ("Jos Electric Disco (Prepaid Accounts)", "Jos Electric Disco (Prepaid Accounts)"),
    (
        "Jos Electric Disco (Postpaid Accounts)",
        "Jos Electric Disco (Postpaid Accounts)",
    ),
    (
        "Enugu Electric Disco (Prepaid Accounts)",
        "Enugu Electric Disco (Prepaid Accounts)",
    ),
    (
        "Enugu Electric Disco (Postpaid Accounts)",
        "Enugu Electric Disco (Postpaid Accounts)",
    ),
    (
        "Kano Electric Disco (Prepaid Accounts)",
        "Kano Electric Disco (Prepaid Accounts)",
    ),
    (
        "Kano Electric Disco (Postpaid Accounts)",
        "Kano Electric Disco (Postpaid Accounts)",
    ),
)

SHOWMAX = (("S0MX", "Showmax"),)


class CreditSwitchAirTimeService(models.Model):
    provider = models.CharField(max_length=50, choices=AIRTIME_PROVIDER)
    code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.provider} - {self.code}"


class CreditSwitchDataService(models.Model):
    provider = models.CharField(max_length=50, choices=DATA)
    code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.provider} - {self.code}"


class CreditSwitchEletricityService(models.Model):
    provider = models.CharField(max_length=50, choices=ELECTRICITY)
    code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.provider} - {self.code}"


class CreditSwitchShowmaxService(models.Model):
    provider = models.CharField(max_length=50, choices=SHOWMAX)
    code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.provider} - {self.code}"
