from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, username, **extra_fields):
        if not username:
            raise ValueError(_('Username must be set'))

        user = self.model(username=username, **extra_fields)
        user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, username, **extra_fields):
        extra_fields.setdefault('is_active', True)

        return self.create_user(username, **extra_fields)
