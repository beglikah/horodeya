from django.contrib import admin
from django import forms
# from django.contrib.auth.admin import UserAdmin

from . import models as _models
from accounts.models import User
from accounts.models import DonatorData, LegalEntityDonatorData
from vote.models import Vote


class ProjectAdminForm(forms.ModelForm):
    administrators = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = _models.Project
        fields = [
            'name',
            'verified_status',
            'administrators',
            'members',
            'prezentation',
        ]

        def __init__(self, *args, **kwargs):
            super(ProjectAdminForm, self).__init__(*args, **kwargs)
            if self.instance:
                self.fields['administrators'].initial = self.instance.administrators.all()
                self.fields['members'].initial = self.instance.members.all()


class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm

    list_display = (
        'name',
        'verified_status',
        'author_admin',
        'all_administrators',
        'all_members',
    )
    list_editable = (
    )

    def save_model(self, request, project, form, change):
        original_administrators = project.administrators.all()
        new_administrators = form.cleaned_data.get('administrators')
        remove_a = original_administrators.exclude(
            id__in=new_administrators.values('id')
        )
        add_a = new_administrators.exclude(
            id__in=original_administrators.values('id')
        )
        project.save()

        if new_administrators:
            for administrator in new_administrators.all():
                if administrator.is_administrator is not True:
                    administrator.is_administrator = True
                    administrator.save()

        if remove_a:
            project.administrators.remove(*remove_a)
        if add_a:
            project.administrators.add(*add_a)

        original_members = project.members.all()
        new_members = form.cleaned_data.get('members')
        remove_m = original_members.exclude(id__in=new_members.values('id'))
        add_m = new_members.exclude(id__in=original_members.values('id'))
        project.save()

        if new_members:
            for member in new_members.all():
                if member.is_member is not True:
                    member.is_member = True
                    member.save()

        if remove_m:
            project.members.remove(*remove_m)
        if add_m:
            project.members.add(*add_m)


admin.site.register(_models.Project, ProjectAdmin)
admin.site.register(Vote)
admin.site.register(_models.MoneySupport)
admin.site.register(_models.TimeSupport)
admin.site.register(_models.ThingSupport)
admin.site.register(_models.Announcement)
admin.site.register(_models.QuestionPrototype)
admin.site.register(_models.Question)
admin.site.register(_models.Answer)
admin.site.register(_models.Report)
admin.site.register(DonatorData)
admin.site.register(LegalEntityDonatorData)
admin.site.register(_models.BugReport)
admin.site.register(_models.EpayMoneySupport)
admin.site.register(_models.TimeNecessity)
admin.site.register(_models.ThingNecessity)
admin.site.register(_models.TicketQR)
