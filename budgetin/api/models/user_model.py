from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from api.models.abstract_model import TimestampModel, UserTrackModel
from django_softdelete.models import SoftDeleteModel

from api.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimestampModel, UserTrackModel, SoftDeleteModel):
    username = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=100, default='user')
    is_active = models.BooleanField(default=True)
    password = None
    is_superuser = None
    date_joined = None
    last_login = None

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username
