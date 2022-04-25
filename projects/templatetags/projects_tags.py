from django import template
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

from vote.models import UP, DOWN
from projects.models import Support, Project

register = template.Library()


@register.simple_tag
def author_admin(user, project_pk, show_admin):
    project = get_object_or_404(Project, pk=project_pk)
    context = {}
    print("Project Author: ", project.author_admin)
    print("Is Author: ", project.author_admin == user)
    if project.author_admin == user and project.pk and show_admin:
        print("Show Admin: ", show_admin)
        if show_admin is False:
            show_admin = False
            context['as_regular_user'] = user.is_authenticated
            print(context)
        else:
            show_admin = True
            context['author_admin'] = user and show_admin
    print("Tag Context: ", context)
    print()
    return context


@register.simple_tag
def administrator_admin(user, project_pk, show_admin):
    project = get_object_or_404(Project, pk=project_pk)
    context = {}

    administrators = project.all_administrators().split(',')
    print("Administrators: ", administrators)
    for administrator in administrators:
        print("Is administrator: ", administrator == user.get_full_name())
        if administrator == user.get_full_name() and project.pk and show_admin:
            if show_admin is False:
                context['as_regular_user'] = user.is_authenticated
                print("Current user: ", user)
            else:
                show_admin = True
                context['administrator_admin'] = user and show_admin
    print("Administrator tag: ", context)
    print()
    return context


@register.simple_tag
def member_admin(user, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    context = {}
    members = project.all_members().split(', ')
    print("Project Members:", members)
    for member in members:
        print("Is member: ", member == user.get_full_name())
        if member == user.get_full_name() and project.pk:
            context['member_admin'] = member
    print("Member:", context)
    print()
    return context


@register.simple_tag
def as_regular_user(user, project_pk, show_admin):
    project = get_object_or_404(Project, pk=project_pk)
    context = {}

    if show_admin is False and project.pk:
        context['as_regular_user'] = user.is_authenticated
        print("Current user: ", user)
    print("As Regular User tag: ", context)
    print()
    return context


@register.simple_tag
def vote_exists(report, user_pk):
    vote_up = report.votes.exists(user_pk, action=UP)
    vote_down = report.votes.exists(user_pk, action=DOWN)
    return vote_up or vote_down


@register.simple_tag
def format_answer(answer):
    type = answer.question.prototype.type
    if type in ['CharField', 'TextField']:
        return answer.answer
    # TODO
    if type == 'FileField':
        return answer.answer
    if type == 'ChoiceField':
        return [gettext_lazy('Yes'), gettext_lazy('No')][int(answer.answer)-1]
    if type == 'Necessities':
        return ""

    return "not implemented"


@register.filter
def leva(value):
    if value == 0:
        return '0 ' + _('lv')

    if value is None:
        return _("unknown")

    return "%.2f " % value + _('lv')


STATUS_COLOR = {
    Support.STATUS.review: 'warning',
    Support.STATUS.delivered: 'success',
    Support.STATUS.accepted: 'default',
    Support.STATUS.declined: 'danger',
    Support.STATUS.expired: 'light',
    }


@register.filter
def status_color(status):
    return STATUS_COLOR.get(status, 'default')


@register.filter
def status_text(status):
    return gettext_lazy(status)
