from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from accounts.models import User
from projects.models import Project
from projects.views import neat_photo

from stream_django.feed_manager import feed_manager
from stream_django.enrich import Enrich

from rules.contrib.views import permission_required, objectgetter
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django import forms


# Create your views here.
def account(request, pk=None):
    if pk:
        account = get_object_or_404(User, pk=pk)
    else:
        account = request.user

    projectsSet = []

    for project in Project.objects.filter(verified_status='accepted'):
        projectsSet.append(project)

    account.projects = projectsSet
    return render(request, 'account/account.html', {'object': account})


class UploadFileForm(forms.Form):
    file = forms.FileField(required=False)
    delete = forms.BooleanField(initial=False, required=False)


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
