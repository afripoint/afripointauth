from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from creditswitch.bills.models import (
    CreditSwitchAirTimeService,
    CreditSwitchDataService,
    CreditSwitchEletricityService,
    CreditSwitchShowmaxService,
    ServiceProviders,
)

admin.site.register(CreditSwitchAirTimeService, ImportExportModelAdmin)
admin.site.register(CreditSwitchDataService, ImportExportModelAdmin)
admin.site.register(CreditSwitchEletricityService, ImportExportModelAdmin)
admin.site.register(CreditSwitchShowmaxService, ImportExportModelAdmin)
admin.site.register(ServiceProviders, ImportExportModelAdmin)
