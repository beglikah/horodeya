from django import forms

from django.utils.safestring import mark_safe
from django.utils.functional import lazy
from django.utils.translation import gettext as _
from django.utils.translation import ugettext_lazy as _translate
# from tempus_dominus.widgets import DatePicker

from allauth.account.forms import SignupForm
from allauth.account.forms import SetPasswordField, PasswordField

from accounts.models import User

mark_safe_lazy = lazy(mark_safe)


class NamesSignupForm(SignupForm):

    field_order = [
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2',
        'privacy_policy',
        'platform_policy'
    ]

    # TODO add validators - no space allowed
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=30)

    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=30)

    password1 = SetPasswordField(max_length=6, label=("Password"))
    password2 = PasswordField(max_length=6, label=("Password (again)"))

    privacy_policy = forms.BooleanField(
        required=True,
        label=mark_safe_lazy(_translate(
            '''I read and understood the contents of<a target="_blank" href="">
            Privacy Policy</a>'''
        ))
    )
    platform_policy = forms.BooleanField(
        required=True,
        label=mark_safe_lazy(_translate(
            '''I read and understood the contents of<a target="_blank" href="">
            Conditions for work with platform </a> and I accept them.'''
        ))
    )

    def clean_password2(self):
        if ("password1" in self.cleaned_data and "password2" in self.cleaned_data):
            if (self.cleaned_data["password1"] != self.cleaned_data["password2"]):
                raise forms.ValidationError(("You must type the same password each time."))
        return self.cleaned_data["password2"]

    def signup(self, request, user):
        user.set_password(self.user, self.cleaned_data["password1"])
        user.save()

    def save(self, request):
        user = super(NamesSignupForm, self).save(request)

        user.set_password(self.user, self.cleaned_data["password1"])
        user.first_name = request.POST['first_name']
        user.second_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.birthdate = request.POST['birthdate']
        user.privacy_policy = True
        user.platform_policy = True
        user.save()
        return user


class UploadFileForm(forms.Form):
    file = forms.FileField(required=False)
    delete = forms.BooleanField(initial=False, required=False)
