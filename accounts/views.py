from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from accounts.models import User
from projects.views import neat_photo

from stream_django.feed_manager import feed_manager
from stream_django.enrich import Enrich

from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from rules.contrib.views import permission_required, objectgetter
from rules.contrib.views import AutoPermissionRequiredMixin

from django.utils.text import slugify
from django.utils.translation import gettext as _
from accounts.forms import UploadFileForm


# Create your views here.
def account(request, pk=None):
    if pk:
        account = get_object_or_404(User, pk=pk)
    else:
        account = request.user

    print(account.projects)
    return render(request, 'account/account.html', {'object': account})


@permission_required('accounts.change_user', fn=objectgetter(User, 'user_id'))
def user_photo_update(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    print(user)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            title = str(user)
            slug = slugify(title, allow_unicode=True)

            if user.photo:
                user.photo.delete()

            if form.cleaned_data.get('delete'):
                messages.success(request, _('Image deleted'))
            else:
                photoFile = request.FILES.get('file')
                if(photoFile):
                    user.photo = neat_photo('user', str(
                        user_id), photoFile)
                    user.save()

                messages.success(request, _('Image uploaded'))
            next = request.GET.get('next')
            if next:
                return redirect(request.GET['next'])
            else:
                return redirect(user)
    else:
        form = UploadFileForm(
            initial={'file': user.photo.image if user.photo else None})

    return render(request, 'account/user_photo_update.html', {
        'form': form, 'user': user
    })


def notifications(request):
    user = request.user

    notification_feed = feed_manager.get_notification_feed(user.id)
    notification_stats = notification_feed.get(limit=10, mark_seen=True)
    enricher = Enrich()
    notifications = enricher.enrich_aggregated_activities(
        notification_stats['results'])

    return render(
        request, 'activity/aggregated/report.html', {
            'notifications': notifications
        }
    )


class UserDetailView(AutoPermissionRequiredMixin, DetailView):
    template_name = 'account/user_form.html'
    model = User


class UserUpdateView(UpdateView):
    template_name = 'account/user_update.html'
    model = User
    fields = [
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
        'platform_policy'
    ]
