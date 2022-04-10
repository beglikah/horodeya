from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

from . import models
from accounts.models import DonatorData, LegalEntityDonatorData
from vote.models import Vote


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'verified_status',
        'administrators',
        'members',
    ]
    list_display = (
        'name',
        'verified_status',
        'author_admin',
        'all_administrators',
        'all_members',
    )
    list_editable = (
    )


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(Vote)
admin.site.register(models.MoneySupport)
admin.site.register(models.TimeSupport)
admin.site.register(models.ThingSupport)
admin.site.register(models.Announcement)
admin.site.register(models.QuestionPrototype)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Report)
admin.site.register(DonatorData)
admin.site.register(LegalEntityDonatorData)
admin.site.register(models.BugReport)
admin.site.register(models.EpayMoneySupport)
admin.site.register(models.TimeNecessity)
admin.site.register(models.ThingNecessity)
admin.site.register(models.TicketQR)
