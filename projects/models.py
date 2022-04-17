from django.db import models
from django.urls import reverse
from django.conf import settings

import rules

import datetime
from django.utils import timezone
from django.utils.translation import get_language, gettext_lazy as _

from stream_django.activity import Activity

from model_utils import Choices
from photologue.models import Gallery
from vote.models import VoteModel
from accounts.models import User, Timestamped


def determine_project(object):
    if isinstance(object, Project):
        return object
    elif isinstance(object, Report) or isinstance(object, Support):
        return object.project
    return object


@rules.predicate
def is_author_admin(user, object):
    if determine_project(object) is not None:
        return user == determine_project(object).author_admin


@rules.predicate
def is_author(user):
    if user.is_author:
        return user.is_author(determine_project(object))


@rules.predicate
def member_of_project(user, object):
    if determine_project(object) is not None:
        for member in determine_project(object).members.all():
            if user == member:
                return user == member


@rules.predicate
def administrator_of_project(user, object):
    if determine_project(object) is not None:
        for administrator in determine_project(object).administrators.all():
            if user == administrator:
                return user == administrator


@rules.predicate
def myself(user, user2):
    if isinstance(user2, User):
        return user == user2

    return user == user2.user


@rules.predicate
def has_a_project(user):
    return user.projects.count() > 0


@rules.predicate
def is_accepted(user, support):
    return support.status == support.STATUS.accepted


PROJECT_ACTIVYTY_TYPES = [
    (
        'Creativity',
        '''Проекти от областта на науката или изкуството, които развиват
        градивната енергия на индивида и неговата сила за себе реализация.'''
    ), (
        'Education',
        '''Проекти, стъпили на принципа на висшата справедливост и въплащение
        на благородни мисли и желания в живота на човека, при което
        интуитивните и творческите му способности достигат нови нива.'''
    ), (
        'Art',
        ''' Проекти в областта на културата, които събуждат естественото ни
        чувство за споделяне и придават финес на взаимоотношенията
        в обществото.'''
    ), ('Administration',
        ''' Проекти, свързани със системи за създаване и прилагане на правила
        за истинно и честно социално взаимодействие. Механизми за разрешаване
        на спорове.'''
        ), ('Willpower',
            '''Проекти, които развиват смелост, устрем, воля за победа, воля за
        индивидуална и колективна изява, като спорт и туризъм.'''
            ), (
        'Health',
        '''Проекти, които следват естествения ритъм на човешкия организъм и са
        мост между Висшия и конкретния ум.'''
    ), (
        'Food',
        '''Проекти развиващи това, което най-пряко влияе върху нашите бит и
        ежедневие, допринасят за оцеляването и изхранването на обществото.'''
    )
]


# TODO notify user on new project added


CATEGORY_TYPES = [('Creativity', 'Наука и творчество'),
                  ('Education', 'Просвета и възпитание'),
                  ('Art', 'Култура и артистичност'),
                  ('Administration', 'Администрация и финанси'),
                  ('Willpower', 'Спорт и туризъм'),
                  ('Health', 'Бит и здравеопазване'),
                  ('Food', 'Земеделие и изхранване')]

REPORT_TIMESPAN_CHOICES = Choices(
    ('weekly', _('weekly')),
    ('monthly', _('montly')),
    ('twoweeks', _('twoweeks'))
)
VERIFY_TYPES_CHOICES = Choices(
    ('review', _('review')),
    ('accepted', _('accepted')),
    ('rejected', _('rejected'))
)


def get_verify_types_choices():
    return VERIFY_TYPES_CHOICES


def get_report_translated_choices():
    return REPORT_TIMESPAN_CHOICES


class Project(Timestamped):
    class Meta:
        rules_permissions = {
            "add": is_author,
            "delete": is_author_admin,
            "change": is_author_admin | administrator_of_project,
            "view": rules.always_allow,
            "follow": rules.is_authenticated,
            "create": is_author,
            "add_administrators": is_author_admin,
            "add_members": is_author_admin | administrator_of_project,
        }

    name = models.CharField(_('Name'), max_length=50)
    location = models.CharField(_('location'), max_length=30, null=True)
    goal = models.TextField(_('goal'), null=True)
    description = models.CharField(_('description'), max_length=300)
    text = models.TextField(_('text'), max_length=5000)
    start_date = models.DateField(_('start_date'), null=True, blank=False)
    end_date = models.DateField(_('end_date'), null=True, blank=False)
    end_date_tasks = models.DateField(
        _('end_date_tasks'), null=True, blank=False)
    gallery = models.ForeignKey(Gallery, on_delete=models.PROTECT, null=True)
    report_period = models.CharField(
        _('report_period'),
        choices=get_report_translated_choices(),
        max_length=50, default='weekly'
    )
    category = models.CharField(
        _('category'),
        choices=CATEGORY_TYPES,
        max_length=50, default='Education'
    )
    slack_channel = models.CharField(
        _('slack_channel'), max_length=100, null=True, blank=True)
    verified_status = models.CharField(
        _('verified_status'),
        max_length=20, choices=get_verify_types_choices(),
        default=VERIFY_TYPES_CHOICES.review, null=True
    )
    author_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    administrators = models.ManyToManyField(
        User,
        related_name='administrator_of_project', blank=True)
    members = models.ManyToManyField(
        User,
        related_name='member_of_project',
        blank=True
    )

    def all_administrators(self):
        return ", ".join([str(a) for a in self.administrators.all()])

    def all_members(self):
        return ", ".join([str(m) for m in self.members.all()])

    def latest_reports(self):
        show_reports = 3
        ordered = self.report_set.order_by('-published_at')
        return ordered[:show_reports], ordered.count() - show_reports

    def key(self):
        return 'project-%d' % self.id

    def __str__(self):
        return ' - '.join([self.name])

    def get_absolute_url(self):
        return reverse('projects:details', kwargs={'pk': self.pk})

    # TODO normalize to a field, update on signal
    def supporters_stats(self):
        money_supporters = set()
        time_supporters = set()
        money = 0
        time = datetime.timedelta(days=0)
        for money_support in self.moneysupport_set.all():
            money_supporters.add(money_support.user)
            money += money_support.leva

        for time_support in self.timesupport_set.all():
            time_supporters.add(time_support.user)
            time += time_support.duration()

        return len(money_supporters), money, len(time_supporters), time

    def total_supporters(self):
        supporters = set()
        for money_support in self.moneysupport_set.all():
            supporters.add(money_support.user)
        for time_support in self.timesupport_set.all():
            supporters.add(time_support.user)

        return len(supporters)

    def money_support(self):
        s = 0
        for money_support in self.moneysupport_set.filter(status__in=[Support.STATUS.accepted, Support.STATUS.delivered]):
            s += money_support.leva

        return s

    def things_fulfilled(self):
        s = 0
        money_support = self.money_support()
        for necessity in self.thingnecessity_set.all():
            accepted = necessity.accepted_support()
            s += accepted

        return s

    def things_still_needed(self):
        return self.things_needed() - self.things_fulfilled()

    def things_needed(self):
        s = 0
        for thing in self.thingnecessity_set.all():
            s += thing.count

        return s

    def time_fulfilled(self):
        s = 0
        for necessity in self.timenecessity_set.all():
            s += necessity.accepted_support()

        return s

    def time_still_needed(self):
        return self.time_needed() - self.time_fulfilled()

    def time_needed(self):
        s = 0
        for time in self.timenecessity_set.all():
            s += time.count

        return s

    def money_still_needed(self):
        return self.money_needed() - self.money_support()

    def money_needed(self):
        s = 0
        for thing in self.thingnecessity_set.all():
            s += thing.count * thing.price

        return s

    def money_support_percent(self):
        money_needed = self.money_needed()
        if money_needed == 0:
            return 0

        return int(100*self.money_support() / money_needed)

    def thing_support_percent(self):
        things_needed = self.things_needed()
        if things_needed == 0:
            return 0

        return int(100*self.things_fulfilled() / things_needed)

    def time_support_percent(self):
        time_needed = self.time_needed()
        if time_needed == 0:
            return 0

        return int(100*self.time_fulfilled() / time_needed)

    def recent_time_support(self):
        return self.timesupport_set.order_by('-status_since')

    def recent_money_support(self):
        return self.moneysupport_set.order_by('-status_since')


class Announcement(Timestamped, Activity):
    class Meta:
        rules_permissions = {
            "add": is_author_admin | administrator_of_project | member_of_project,
            "delete": is_author_admin,
            "change": is_author_admin | administrator_of_project | member_of_project,
            "view": rules.is_authenticated,
        }

    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    text = models.TextField(verbose_name=_('announcement'))

    @property
    def activity_author_feed(self):
        return 'project'

    @property
    def activity_actor_attr(self):
        return self.project

    def get_absolute_url(self):
        return reverse('projects:announcement_details', kwargs={'pk': self.pk})


class Report(VoteModel, Timestamped, Activity):
    class Meta:
        rules_permissions = {
            "add": is_author_admin | administrator_of_project | member_of_project,
            "delete": is_author_admin,
            "change": is_author_admin | member_of_project | administrator_of_project,
            "view": rules.is_authenticated,
        }
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    text = models.TextField(_('text'))
    published_at = models.DateTimeField(_('published_at'))

    @property
    def activity_author_feed(self):
        return 'project'

    @property
    def activity_actor_attr(self):
        return self.project

    def __str__(self):
        return self.published_at.isoformat()

    def get_absolute_url(self):
        return reverse('projects:report_details', kwargs={'pk': self.pk})

# TODO notify in feed


class TimeNecessity(Timestamped):
    class Meta:
        rules_permissions = {
            "add": is_author_admin | administrator_of_project,
            "delete": is_author_admin,
            "change": is_author_admin | administrator_of_project | member_of_project,
            "view": rules.is_authenticated,
            "list": rules.is_authenticated,
        }

    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    description = models.CharField(_('description'), max_length=300)
    price = models.IntegerField(_('price'))
    count = models.IntegerField(_('count'), default=1)
    start_date = models.DateField(_('start_date'))
    end_date = models.DateField(_('end_date'))

    def __str__(self):
        return self.name

    def still_needed(self):
        return self.count - self.accepted_support()

    def accepted_support(self):
        return self.supports.filter(status=Support.STATUS.accepted).count()

    def support_candidates(self):
        return self.supports.filter(status=Support.STATUS.review)

    def get_absolute_url(self):
        return reverse('projects:time_necessity_details', kwargs={'pk': self.pk})

# TODO notify in feed


class ThingNecessity(Timestamped):
    class Meta:
        rules_permissions = {
            "add": is_author_admin | administrator_of_project,
            "delete": is_author_admin | administrator_of_project | member_of_project,
            "change": is_author_admin | administrator_of_project | member_of_project,
            "view": rules.is_authenticated,
            "list": rules.is_authenticated,
        }
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    name = models.CharField(_('Name'), max_length=50)
    description = models.CharField(_('description'), max_length=300)
    price = models.IntegerField(_('price'))
    count = models.IntegerField(_('count'))

    def create_thing_support_from_unused_money_support(self):
        unused_money_support = list(filter(
            lambda s: not s.thingsupport_set.all().exists(),
            self.accepted_money_support()
        ))

        price = self.price
        use_supports = []

        if self.still_needed() == 0:
            return False

        for support in unused_money_support:
            use_supports.append(support)

            if support.leva < price:
                price -= support.leva
                continue

            remaining = support.leva - price
            while remaining >= 0:
                thing_support = self.supports.create(
                    price=self.price,
                    project=self.project,
                    user=self.project.admin,
                    comment='Auto generated',
                    status=Support.STATUS.accepted,
                    status_since=timezone.now(),
                )

                thing_support.from_money_supports.set(use_supports)
                use_supports = []
                price = self.price

                if remaining == 0:
                    break

                if self.still_needed() == 0:
                    self.money_supports.create(
                        leva=remaining,
                        project=self.project,
                        user=support.user,
                        comment='reminder from %d' % support.id,
                        # so that admin is forced to choose Necessity to spend it on
                        status=Support.STATUS.review,
                        status_since=timezone.now(),
                    )
                    return True

                if remaining > 0:
                    use_supports.append(support)
                    saved_price = price
                    price -= remaining
                    remaining -= saved_price

        return True

    def __str__(self):
        return "%s" % self.name

    def still_needed(self):
        return self.count - self.accepted_support()

    def accepted_support(self):
        return self.supports.filter(status=Support.STATUS.accepted).count()

    def accepted_support_price(self):
        return self.accepted_support() * self.price

    def total_price(self):
        return self.count * self.price

    def total_price_still_needed(self):
        return self.still_needed() * self.price

    def accepted_money_support(self):
        return self.money_supports.filter(status=Support.STATUS.accepted).all()

    def accepted_money_support_leva(self):
        return sum(self.money_supports.filter(status=Support.STATUS.accepted).values_list('leva', flat=True))

    def support_candidates_count(self):
        return self.supports.filter(status=Support.STATUS.review).count() + self.money_supports.filter(status=Support.STATUS.review).count()

    def get_absolute_url(self):
        return reverse('projects:thing_necessity_details', kwargs={'pk': self.pk})


class Support(Timestamped):

    class Meta:
        rules_permissions = {
            "add": rules.is_authenticated,
            "delete": myself & ~is_accepted,
            "change": (myself & ~is_accepted) | is_author_admin | administrator_of_project,
            "view": myself | is_author_admin | administrator_of_project | member_of_project,
            "accept": is_author_admin | administrator_of_project | member_of_project,
            "mark_delivered": is_author_admin | administrator_of_project | member_of_project,
            "list": is_author_admin | administrator_of_project | member_of_project,
        }

        abstract = True

    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    supportType = models.CharField(max_length=30, null=True)

    comment = models.TextField(
        blank=True, verbose_name=_('Do you have a comment'))

    STATUS = Choices(
        ('review', _('review')),
        ('delivered', _('delivered')),
        ('accepted', _('accepted')),
        ('declined', _('declined')),
        ('expired', _('expired'))
    )

    status = models.CharField(_('status'),
                              max_length=20, choices=STATUS, default=STATUS.review)
    status_since = models.DateTimeField(
        _('status_since'), default=timezone.now)
    __original_status = None

    def __init__(self, *args, **kwargs):
        super(Support, self).__init__(*args, **kwargs)
        self.__original_status = self.status

    def save(self, *args, **kwargs):
        if self.status != self.__original_status:
            self.status_since = timezone.now()

        res = super(Support, self).save(*args, **kwargs)
        self.__original_status = self.status
        return res

    def delivery_expires(self):
        if not self.status == 'accepted':
            return None

        return self.status_since + datetime.timedelta(days=30)

    def expired(self):
        if self.status == 'expired':
            return True

        expires = self.delivery_expires()
        if expires and expires < timezone.now():
            self.status = 'expired'
            self.save()
            return True

        return False

    def set_accepted(self, accepted=True):
        if accepted is True:
            self.status = self.STATUS.accepted
        elif accepted is False:
            self.status = self.STATUS.declined
        else:
            self.status = self.STATUS.review

#        if accepted is not None:
#            self.accepted_at = timezone.now()

        self.save()

        return accepted

# TODO notify in feed


class MoneySupport(Support):
    class Meta:
        rules_permissions = {
            "add": rules.is_authenticated,
            "delete": myself & ~is_accepted,
            "change": (myself & ~is_accepted) | is_author_admin | administrator_of_project | member_of_project,
            "view": myself |is_author_admin | administrator_of_project |  member_of_project,
            "accept": is_author_admin | administrator_of_project |  member_of_project,
            "mark_delivered": is_author_admin | administrator_of_project |  member_of_project,
            "list": is_author_admin | administrator_of_project |  member_of_project,
            "list-user": myself
        }

    necessity = models.ForeignKey(ThingNecessity, on_delete=models.PROTECT, related_name='money_supports',
                                  null=True, blank=True, verbose_name=_('Which necessity do you wish to donate to'))
    leva = models.FloatField(verbose_name=_('How much do you wish to donate'))

    payment_method = models.CharField(max_length=20, verbose_name=_(
        'Choose a payment method'), default='Unspecified')

    pay_time = models.DateTimeField(null=True, blank=True, editable=False)

    def get_absolute_url(self):
        return reverse('projects:money_support_details', kwargs={'pk': self.pk})

    def get_type(self):
        return 'money'

    def set_accepted(self, accepted=True):
        super(MoneySupport, self).set_accepted(accepted)

        if accepted:
            if not self.necessity:
                raise RuntimeError(
                    'Expected necessity to be set when accepting money support')

            new_accepted = self.necessity.create_thing_support_from_unused_money_support()

            if new_accepted != accepted:
                return super(MoneySupport, self).set_accepted(None)

        return accepted

    def __str__(self):
        return "%s (%s)" % (self.user.first_name, self.leva) + (" for %s" % self.necessity if self.necessity else "")

# TODO notify in feed


class ThingSupport(Support):
    class Meta:
        rules_permissions = {
            "add": rules.is_authenticated,
            "delete": myself & ~is_accepted,
            "change": myself & ~is_accepted,
            "view": myself |is_author_admin | administrator_of_project | member_of_project,
            "accept": is_author_admin | administrator_of_project |  member_of_project,
            "mark_delivered": is_author_admin | administrator_of_project | member_of_project,
            "list": is_author_admin | administrator_of_project | member_of_project,
            "list-user": myself
        }

    necessity = models.ForeignKey(
        ThingNecessity, on_delete=models.PROTECT, related_name='supports')
    price = models.IntegerField(_('price'))
    from_money_supports = models.ManyToManyField(MoneySupport, blank=True)

    def get_absolute_url(self):
        return reverse('projects:thing_support_details', kwargs={'pk': self.pk})

    def get_type(self):
        return 'thing'

    def __str__(self):
        return "%s (%s)" % (self.user.first_name, self.necessity.name)


class Answer(Timestamped):
    class Meta:
        rules_permissions = {
            "add": rules.is_authenticated,
            "delete": myself & ~is_accepted,
            "change": myself & ~is_accepted,
            "view": myself | is_author_admin | administrator_of_project | member_of_project,
            "list": myself | is_author_admin | administrator_of_project | member_of_project
        }
        unique_together = ['project', 'question', 'user']

    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    answer = models.TextField(_('answer'), null=False, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# TODO notify in feed


class TimeSupport(Support):
    class Meta:
        rules_permissions = {
            "add": rules.is_authenticated,
            "delete": myself & ~is_accepted,
            "change": (myself & ~is_accepted) | is_author_admin | administrator_of_project,
            "view": rules.is_authenticated,
            "accept": is_author_admin | administrator_of_project,
            "mark_delivered": is_author_admin | administrator_of_project | member_of_project,
            "list": is_author_admin | administrator_of_project | member_of_project,
        }
        unique_together = ['necessity', 'user']

    necessity = models.ForeignKey(
        TimeNecessity, on_delete=models.CASCADE, related_name='supports')
    price = models.IntegerField(_('price'))
    start_date = models.DateField(_('start_date'))
    end_date = models.DateField(_('end_date'))

    def get_absolute_url(self):
        return reverse('projects:time_support_details', kwargs={'pk': self.pk})

    def get_type(self):
        return 'time'

    def duration(self):
        return (self.end_date - self.start_date).days

    def __str__(self):
        return "%s: %s" % (self.necessity, self.user.first_name)

    def ordered_answers(self):
        return self.user.answer_set.filter(project=self.necessity.project).order_by('question__order')


class QuestionPrototype(Timestamped):
    class Meta:
        rules_permissions = {
            "add": rules.always_deny,
            "delete": rules.always_deny,
            "change": rules.always_deny,
            "view": rules.always_allow,
            "list": rules.always_allow
        }

    text_bg = models.CharField(max_length=100, unique=True)
    text_en = models.CharField(max_length=100, unique=True)
    TYPES = Choices('CharField', 'TextField', 'FileField',
                    'ChoiceField', 'Necessities')

    type = models.CharField(max_length=20, choices=TYPES)
    order = models.IntegerField()
    required = models.BooleanField(_('required'), default=True)

    def __str__(self):
        return self.text_bg


class Question(Timestamped):
    class Meta:
        rules_permissions = {
            "add": is_author_admin | administrator_of_project,
            "delete": is_author_admin | administrator_of_project,
            "change": is_author_admin | administrator_of_project,
            "view": rules.always_allow,
            "list": rules.always_allow
        }
        unique_together = ['prototype', 'project']

    prototype = models.ForeignKey(QuestionPrototype, on_delete=models.PROTECT)
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    required = models.BooleanField(_('required'), default=True)
    order = models.IntegerField()

    def __str__(self):
        return "%s. %s%s" % (self.order, self.prototype, ('*' if self.required else ''))

    def text(self):
        return getattr(self.prototype, 'text_%s' % get_language())


class TicketQR(Timestamped):
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    validation_code = models.TextField(_('validation_code'))
    validated_at = models.DateTimeField(_('validated_at'), null=True)

    def set_validated(self):
        self.validated_at = timezone.now()
        self.save()
        return self.validated_at


class BugReport(Timestamped):
    email = models.EmailField(_('email'))
    message = models.TextField(_('message'))


class EpayMoneySupport(Support):
    amount = models.FloatField(verbose_name=_(
        'How much do you wish to donate'))
