from django.utils.safestring import mark_safe
from allauth.account.forms import SignupForm
from django import forms

from django.utils.translation import gettext as _


from django.utils.functional import lazy
from django.utils.translation import ugettext_lazy as translate_lazy
from tempus_dominus.widgets import DateTimePicker, DatePicker

mark_safe_lazy = lazy(mark_safe)


class NamesSignupForm(SignupForm):

    field_order = ['first_name', 'last_name',
                   'birthdate', 'email', 'password1', 'privacy_policy', 'platform_policy']

    # TODO add validators - no space allowed
    first_name = forms.CharField(
        label=_("First Name"),
        max_length=30)

    second_name = forms.CharField(
        label=_("Second Name"),
        max_length=30)

    last_name = forms.CharField(
        label=_("Last Name"),
        max_length=30)

    # accept_tos = forms.BooleanField(
    #     label=mark_safe_lazy(translate_lazy('Accept <a href="/условия-за-ползване">Terms of Service</a>')))

    birthdate = forms.DateField(label=_('birthdate'))

    privacy_policy = forms.BooleanField(required=True, label=mark_safe_lazy(
        translate_lazy('Прочетох и разбрах съдържанието на<a target="_blank" href="https://horodeya.com/%D0%BF%D0%BE%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0-%D0%B7%D0%B0-%D0%BF%D0%BE%D0%B2%D0%B5%D1%80%D0%B8%D1%82%D0%B5%D0%BB%D0%BD%D0%BE%D1%81%D1%82/">  Политика за поверителност на Платформата.</a>')))
    platform_policy = forms.BooleanField(required=True, label=mark_safe_lazy(translate_lazy(
        'Прочетох и разбрах съдържанието на<a target="_blank" href="https://horodeya.com/%D1%83%D1%81%D0%BB%D0%BE%D0%B2%D0%B8%D1%8F-%D0%B7%D0%B0-%D0%BF%D0%BE%D0%BB%D0%B7%D0%B2%D0%B0%D0%BD%D0%B5/"> Условията за работа с Платформата </a>и приемам същите.')))

    def save(self, request):

        user = super(NamesSignupForm, self).save(request)

        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.birthdate = request.POST['birthdate']
        user.privacy_policy = True
        user.platform_policy = True
        user.save()
        return user
