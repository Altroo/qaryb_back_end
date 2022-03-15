from django.db import models
from django.db.models import Model
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager
from places.base.models import City, Country, PlaceType
from os import path
from uuid import uuid4
from Qaryb_API_new.settings import API_URL
from io import BytesIO
from django.core.files.base import ContentFile


def get_avatar_path(instance, filename):
    filename, file_extension = path.splitext(filename)
    return path.join('user_avatars/', str(uuid4()) + file_extension)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Password (hidden)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    GENDER_CHOICES = (
        ('', 'Unset'),
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='', blank=True, null=True)
    birth_date = models.DateField(verbose_name="Date of birth", blank=True, null=True)
    city = models.ForeignKey(City, verbose_name='City', blank=True, null=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, verbose_name='Country', blank=True, null=True, related_name='users',
                                on_delete=models.SET_NULL, limit_choices_to={'type': PlaceType.COUNTRY})
    phone = models.CharField(verbose_name='Phone number', max_length=15, blank=True, null=True, default=None)
    avatar = models.ImageField(verbose_name='User Avatar', upload_to=get_avatar_path, blank=True, null=True,
                               default=None)
    avatar_thumbnail = models.ImageField(verbose_name='User Thumb Avatar', upload_to=get_avatar_path, blank=True,
                                         null=True, default=None)
    # permissions
    is_staff = models.BooleanField(_('staff status'),
                                   default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'), )
    is_active = models.BooleanField(_('active'),
                                    default=False,
                                    help_text=_(
                                        'Designates whether this user should be treated as active. '
                                        'Unselect this instead of deleting accounts.'
                                    ), )
    # DATES
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    # Codes
    activation_code = models.IntegerField(verbose_name='Account Activation Code', blank=True, null=True)
    password_reset_code = models.IntegerField(verbose_name='Password Reset Code', blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return '{}'.format(self.email)

    @property
    def get_absolute_avatar_img(self):
        if self.avatar:
            return "{0}/media{1}".format(API_URL, self.avatar.url)
        return None

    @property
    def get_absolute_avatar_thumbnail(self):
        if self.avatar_thumbnail:
            return "{0}/media{1}".format(API_URL, self.avatar_thumbnail.url)
        return None

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ('date_joined',)

    def save_image(self, field_name, image):
        if not isinstance(image, BytesIO):
            return

        getattr(self, field_name).save(f'{str(uuid4())}.jpg',
                                       ContentFile(image.getvalue()),
                                       save=True)


class BlockedUsers(Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             verbose_name='User', related_name='user_block_sender')
    user_blocked = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                     verbose_name='Blocked user', related_name='user_block_receiver')

    class Meta:
        unique_together = (('user', 'user_blocked'),)
        verbose_name = 'Blocked User'
        verbose_name_plural = 'Blocked Users'


class ReportedUsers(Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             verbose_name='User', related_name='user_report_sender')
    user_reported = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                      verbose_name='Reported user', related_name='user_report_receiver')

    REASONS_CHOICES = (
        ('1', 'Reason 1'),
        ('2', 'Reason 2'),
        ('3', 'Reason 3'),
        ('4', 'Reason 4'),
    )
    report_reason = models.CharField(verbose_name='Reason', choices=REASONS_CHOICES, default='1', max_length=1)

    class Meta:
        # TODO check if user can repport user multiple times
        # unique_together = (('user', 'user_reported'),)
        verbose_name_plural = "Reported items"
