from .models import Project
from django.http.request import HttpRequest


def author(request):
    if request.user.is_authenticated:
        projectsSet = []
        context = {}

        for project in Project.objects.filter(verified_status='accepted'):
            user = request.user
            if project.author_admin == user:
                projectsSet.append(project)

        user.projects = projectsSet
        context['author'] = user.projects
        return context
    else:
        return ""


def administrator_of(request):
    if request.user.is_authenticated:
        projectsSet = []
        context = {}

        for project in Project.objects.filter(verified_status='accepted'):
            user = request.user
            administrators = project.all_administrators().split(',')
            for administrator in administrators:
                if administrator == user.get_full_name():
                    projectsSet.append(project)

        user.administrator_of = projectsSet
        context['administrator_of'] = user.administrator_of
        return context
    else:
        return ""


def member_of(request):
    if request.user.is_authenticated:
        projectsSet = []
        context = {}
        for project in Project.objects.filter(verified_status='accepted'):
            user = request.user
            members = project.all_members().split(', ')
            for member in members:
                if member == user.get_full_name():
                    projectsSet.append(project)

        user.member_of = projectsSet
        context['member_of'] = user.member_of

        return context
    else:
        return ""
