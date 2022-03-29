from __future__ import unicode_literals

from django.urls import reverse

import rules
from rules.contrib.models import RulesModelBase, RulesModelMixin

from django.db import models
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator

from django.utils import timezone
from django.utils.translation import gettext, gettext_lazy as _

# from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, AbstractUser

from django_countries.fields import CountryField

from photologue.models import Photo
from vote.models import UP, DOWN
# from projects.models import Report


@rules.predicate
def has_a_project(user):
    return user.projects.count() > 0


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


class User(RulesModelMixin, AbstractUser, metaclass=RulesModelBase):
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
    is_administrator = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    privacy_policy = models.BooleanField(default=False)
    platform_policy = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def page_name(self):
        return "%s %s" % (gettext('User'), str(self))

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('accounts:account', kwargs={'pk': self.pk})

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def total_support_count(self):
        return self.moneysupport_set.count() + self.timesupport_set.count()

    # def total_votes_count(self):
        # return len(Report.votes.all(self.pk, UP)) + len(Report.votes.all(self.pk, DOWN))

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


class Timestamped(RulesModelMixin, models.Model, metaclass=RulesModelBase):

    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()

        self.updated_at = timezone.now()
        return super(Timestamped, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class DonatorData(Timestamped):

    class Meta:
        rules_permissions = {
            "add": rules.is_authenticated,
            "delete": rules.always_deny,
            "change": myself,
            "view": rules.is_authenticated
        }

    phone = models.CharField(_('phone'), max_length=20, blank=False)
    citizenship = CountryField(_('citizenship'), max_length=30, blank=False)
    postAddress = models.CharField(
        _('postAdress'), max_length=200, blank=False)
    TIN = models.CharField(_('TIN'), max_length=10,
                           blank=False, default=None, null=True)


class LegalEntityDonatorData(Timestamped):
    class Meta:
        rules_permissions = {
            "add": rules.is_authenticated,
            "delete": rules.always_deny,
            "change": myself,
            "view": rules.is_authenticated,
        }

    name = models.CharField(_('name'), max_length=50, blank=False)
    type = models.CharField(_('type'), max_length=50, blank=False)
    headquarters = CountryField(
        _('headquarters'), max_length=30, blank=False, null=True)
    EIK = models.CharField(_('EIK'), max_length=50, blank=False)
    DDORegistration = models.BooleanField(_('DDORegistration'))
    phoneNumber = models.CharField(
        _('phoneNumber'), max_length=30, blank=False)
    postAddress = models.CharField(
        _('postAdress'), max_length=200, blank=False)
    TIN = models.CharField(_('TIN'), max_length=10,
                           blank=False, default=None, null=True)
    website = models.CharField(_('website'), blank=True, max_length=100)


class AuthorAdmin(Timestamped):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    # additional fields
    activation_key = models.CharField(max_length=255, default=1)
    email_validated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()


