from django.contrib import admin
from .models import AccountActivity, AccountTable, AccountTypeTable, AccountName

admin.site.register(AccountActivity)
admin.site.register(AccountTable)
admin.site.register(AccountTypeTable)
admin.site.register(AccountName)
