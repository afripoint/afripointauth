from django.contrib import admin

from OTP.models import MFATable, OTPSettings

admin.site.register(MFATable)
admin.site.register(OTPSettings)
