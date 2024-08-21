from django.db import models

AIRTIME_PROVIDER = (
    ("Airtel", "Airtel"),
    ("MTN", "MTN"),
    ("9-Mobile", "9-Mobile"),
    ("Globacom", "Globacom"),
)

AIRTIME_CODE = (
    ("A01E", "A01E - Airtel"),
    ("A02E", "A02E - 9-Mobile"),
    ("A03E", "A03E - Globacom"),
    ("A04E", "A04E - MTN"),
)

DATA = (
    ("Airtel", "Airtel"),
    ("9-Mobile", "9-Mobile"),
    ("Globacom", "Globacom"),
    ("Globacom", "MTN"),
    ("Smile", "Smile"),
    ("NTEL", "NTEL"),
)

DATA_CODE = (
    ("D01D", "D01D - Airtel"),
    ("D02D", "D02D - 9-Mobile"),
    ("D03D", "	D03D - Globacom"),
    ("D04D", "D04D - MTN"),
    ("D05D", "D05D - Smile"),
    ("D06D", "D06D - NTEL"),
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

ELECTRICITY_CODE = (
    ("E01E", "E01E - Ikeja Electric Disco (Prepaid Accounts)"),
    ("E02E", "E02E - Ikeja Electric Disco (Post Accounts)"),
    ("E03E", "E03E - Ibadan Electric Disco (Prepaid Accounts)"),
    ("E04E", "E04E - Ibadan Electric Disco (Postpaid Accounts)"),
    ("E05E", "E05E - Eko Electric Disco (Prepaid Accounts)"),
    ("E06E", "E06E - Eko Electric Disco (Postpaid Accounts)"),
    ("E07E", "E07E - Abuja Electric Disco (Prepaid Accounts)"),
    ("E08E", "E08E - Abuja Electric Disco (Postpaid Accounts)"),
    ("E09E", "E09E - Port Harcourt Electric Disco (Prepaid Accounts)"),
    ("E10E", "E10E - Port Harcourt Electric Disco (Postpaid Accounts)"),
    ("E11E", "E11E - Kaduna Electric Disco (Prepaid Accounts)"),
    ("E12E", "E12E - Kaduna Electric Disco (Postpaid Accounts)"),
    ("E13E", "E13E - Jos Electric Disco (Prepaid Accounts)"),
    ("E14E", "E14E - Jos Electric Disco (Postpaid Accounts)"),
    ("E15E", "E15E - Enugu Electric Disco (Prepaid Accounts)"),
    ("E16E", "E16E - Enugu Electric Disco (Postpaid Accounts)"),
    ("E17E", "E17E - Kano Electric Disco (Prepaid Accounts)"),
    ("E18E", "E18E - Kano Electric Disco (Postpaid Accounts)"),
)

SHOWMAX = (("S0MX", "Showmax"),)


class CreditSwitchAirTimeService(models.Model):
    provider = models.CharField(max_length=50, choices=AIRTIME_PROVIDER)
    code = models.CharField(max_length=50, choices=AIRTIME_CODE)

    def __str__(self):
        return f"{self.provider} - {self.code}"


class CreditSwitchDataService(models.Model):
    provider = models.CharField(max_length=50, choices=DATA)
    code = models.CharField(max_length=50, choices=DATA_CODE)

    def __str__(self):
        return f"{self.provider} - {self.code}"


class CreditSwitchEletricityService(models.Model):
    provider = models.CharField(max_length=50, choices=ELECTRICITY)
    code = models.CharField(max_length=50, choices=ELECTRICITY_CODE)

    def __str__(self):
        return f"{self.provider} - {self.code}"


class CreditSwitchShowmaxService(models.Model):
    provider = models.CharField(max_length=50, choices=SHOWMAX)
    code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.provider} - {self.code}"
