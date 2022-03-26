from django.shortcuts import render, get_object_or_404
from projects.models import User
from projects.models import Project

from stream_django.feed_manager import feed_manager
from stream_django.enrich import Enrich


# Create your views here.
def home(request):
    return render(request, 'home/itec_home.html')


def account(request, pk=None):
    if pk:
        account = get_object_or_404(User, pk=pk)
    else:
        account = request.user

    projectsSet = []

    for project in Project.objects.filter(verified_status='accepted'):
        projectsSet.append(project)

    account.projects = projectsSet
    return render(request, 'home/account.html', {'object': account})


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
