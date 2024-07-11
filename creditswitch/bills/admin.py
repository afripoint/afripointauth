from django.contrib import admin

from creditswitch.bills.models import (
    CreditSwitchAirTimeService,
    CreditSwitchDataService,
    CreditSwitchEletricityService,
    CreditSwitchShowmaxService,
)

admin.site.register(CreditSwitchAirTimeService)
admin.site.register(CreditSwitchDataService)
admin.site.register(CreditSwitchEletricityService)
admin.site.register(CreditSwitchShowmaxService)
