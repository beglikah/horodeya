from django import template
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

from vote.models import UP, DOWN
from ..models import Support, Project

register = template.Library()


@register.simple_tag
def author(user, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    print("Author: ", project.author_admin)
    if user == project.author_admin:
        author = project.author_admin
        print("Author: ", author)
        return author


@register.simple_tag
def administrator_of(user, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    administrators = project.all_administrators().split(',')
    print("Administrators: ", administrators)
    for administrator in administrators:
        if user.get_full_name() == administrator:
            administrator_of = administrator
            print("Administrator: ", administrator_of)
            return administrator_of


@register.simple_tag
def member_of(user, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    members = project.all_members().split(',')
    print("Memebers: ", members)
    for member in members:
        if user.get_full_name() == member:
            member_of = member
            print("Memeber: ", member)
            return member_of


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
