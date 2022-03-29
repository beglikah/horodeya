from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User


# Register your models here.
class MyUserAdmin(UserAdmin):
    model = User
    readonly_fields = ('date_joined',)


admin.site.register(User, MyUserAdmin)
