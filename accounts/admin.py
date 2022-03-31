from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User


# Register your models here.
class MyUserAdmin(UserAdmin):
    model = User
    readonly_fields = ('date_joined',)
    list_display = (
        'email',
        'photo',
        'first_name',
        'second_name',
        'last_name',
        'country',
        'city',
        'address',
        'phone',
        'bank_account_iban',
        'bank_account_bank_code',
        'bank_account_name',
        'birthdate',
        'slack_channel',
        'privacy_policy',
        'platform_policy',
    )


admin.site.register(User, MyUserAdmin)
