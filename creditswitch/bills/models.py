from django.db import models


# AIRTIME_CATEGORY = (
#     ("airtime", "Airtime"),
#     ("data", "Data"),
#     ("logical_pins", "Logical Pins"),
#     ("electricity", "Electricity"),
#     ("insurance", "Insurance"),
#     ("showmax", "ShowMax"),
# )

AIRTIME_PROVIDER = (
    ("airtel", "Airtel"),
    ("mtn", "MTN"),
    ("9-mobile", "9-Mobile"),
    ("globacom", "Globacom"),
)


# DATA = (
#     ("D01D", "Airtel"),
#     ("D02D", "9-Mobile"),
#     ("D03D", "Globacom"),
#     ("D04D", "Mtn"),
#     ("D05D", "Smile"),
#     ("D06D", "NTEL"),
# )

# AIRTIME = (
#     ("A01E", "Airtel"),
#     ("A02E", "9-Mobile"),
#     ("A03E", "Globacom"),
#     ("A04E", "Mtn"),
# )

# ELECTRICITY = (
#     ("E01E", "Ikeja Electric Disco (Prepaid Accounts)"),
#     ("E02E", "Ikeja Electric Disco (Post Accounts)"),
#     ("E03E", "Ibadan Electric Disco (Prepaid Accounts)"),
#     ("E04E", "Ibadan Electric Disco (Postpaid Accounts)"),
#     ("E05E", "Eko Electric Disco (Prepaid Accounts)"),
#     ("E06E", "Eko Electric Disco (Postpaid Accounts)"),
#     ("E07E", "Abuja Electric Disco (Prepaid Accounts)"),
#     ("E08E", "Abuja Electric Disco (Postpaid Accounts)"),
#     ("E09E", "Port Harcourt Electric Disco (Prepaid Accounts)"),
#     ("E10E", "Port Harcourt Electric Disco (Postpaid Accounts)"),
#     ("E11E", "Kaduna Electric Disco (Prepaid Accounts)"),
#     ("E12E", "Kaduna Electric Disco (Postpaid Accounts)"),
#     ("E13E", "Jos Electric Disco (Prepaid Accounts)"),
#     ("E14E", "Jos Electric Disco (Postpaid Accounts)"),
#     ("E15E", "Enugu Electric Disco (Prepaid Accounts)"),
#     ("E16E", "Enugu Electric Disco (Postpaid Accounts)"),
#     ("E17E", "Kano Electric Disco (Prepaid Accounts)"),
#     ("E18E", "Kano Electric Disco (Postpaid Accounts)"),
# )

# LOGICALPINS = (
#     ("P01N", "Airtel"),
#     ("P02N", "9 Mobile"),
#     ("P03N", "Globacom"),
#     ("P04N", "Mtn"),
#     ("P05N", "Spectranet"),
#     ("P06N", "WAEC"),
#     ("P07N", "JAMB"),
#     ("P08N", "NECO"),
#     ("P09N", "NABTECH"),
# )

# INSURANCE = (("INS0", "Insurance"),)

# SHOWMAX = (("S0MX", "Showmax"),)


# class CreditSwitchService(models.Model):
#     category = models.CharField(max_length=50, choices=CATEGORY)
#     airtime = models.CharField(max_length=50, choices=AIRTIME, blank=True, null=True)
#     data = models.CharField(max_length=50, choices=DATA, blank=True, null=True)
#     electricity = models.CharField(
#         max_length=50, choices=ELECTRICITY, blank=True, null=True
#     )
#     pins = models.CharField(max_length=50, choices=LOGICALPINS, blank=True, null=True)
#     insurance = models.CharField(
#         max_length=50, choices=INSURANCE, blank=True, null=True
#     )
#     showmax = models.CharField(max_length=50, choices=SHOWMAX, blank=True, null=True)

#     def __str__(self):
#         return "CreditSwitch Services"


class CreditSwitchAirTimeService(models.Model):
    provider = models.CharField(max_length=50, choices=AIRTIME_PROVIDER)
    code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.provider} - {self.code}"
