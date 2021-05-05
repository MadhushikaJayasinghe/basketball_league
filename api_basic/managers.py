from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The email must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_player(self, email, password, **extra_fields):
        extra_fields.setdefault('role', 'PLAYER')

        if extra_fields.get('role') != 'PLAYER':
            raise ValueError('Player must have role of PLAYER')
        return self.create_user(email, password, **extra_fields)

    def create_coach(self, email, password, **extra_fields):
        extra_fields.setdefault('role', 'COACH')

        if extra_fields.get('role') != 'COACH':
            raise ValueError('COACH must have role of COACH')
        return self.create_user(email, password, **extra_fields)

    def create_admin(self, email, password, **extra_fields):
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('role') != 'ADMIN':
            raise ValueError('ADMIN must have role of ADMIN')
        return self.create_user(email, password, **extra_fields)
