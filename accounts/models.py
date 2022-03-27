from __future__ import unicode_literals

from django.urls import reverse

import rules
from rules.contrib.models import RulesModelBase, RulesModelMixin

from django.db import models
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator

from django.utils import timezone
from django.utils.translation import gettext, gettext_lazy as _

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager

from photologue.models import Photo
from vote.models import UP, DOWN


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        return user


@rules.predicate
def myself(user, user2):
    if isinstance(user2, User):
        return user == user2

    return user == user2.user


class User(AbstractBaseUser, RulesModelMixin, metaclass=RulesModelBase):
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    bal = models.IntegerField(default=20, validators=[MaxValueValidator(100)])
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True)
    donatorData = models.OneToOneField(
        'DonatorData', on_delete=models.PROTECT, null=True)
    legalEntityDonatorData = models.OneToOneField(
        'LegalEntityDonatorData', on_delete=models.PROTECT, null=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    second_name = models.CharField(_('second_name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    slack_channel = models.CharField(
        _('slack_channel'), max_length=100, null=True, blank=True)
    birthdate = models.DateField(
        _('birthdate'), blank=False, null=True)
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    privacy_policy = models.BooleanField(default=False)
    platform_policy = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        rules_permissions = {
            "add": rules.always_allow,
            "delete": rules.always_deny,
            "change": myself,
            "view": rules.is_authenticated,
        }
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'auth_user'

    def page_name(self):
        return "%s %s" % (gettext('User'), str(self))

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('account', kwargs={'pk': self.pk})

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def total_support_count(self):
        return self.moneysupport_set.count() + self.timesupport_set.count()

    def total_votes_count(self):
        return len(Report.votes.all(self.pk, UP)) + len(Report.votes.all(self.pk, DOWN))

    def administrator_of(self, project_pk):
        return self.projects.filter(pk=project_pk).exists()

    def member_of(self, project_pk):
        return self.projects.filter(pk=project_pk).exists()


class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, default=None)
    all_objects = models.Manager()
    objects = SoftDeleteManager()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        abstract = True
