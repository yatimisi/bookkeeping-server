import os
import time

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as AuthUerManager
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.utils.translation import gettext_lazy as _


def user_image_path(instance, filename):
    ext = os.path.splitext(filename)[-1]
    return os.path.join('user-profile', f'{instance.username}{ext}')


class UserManager(AuthUerManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField('電子郵件', unique=True)
    profile = models.ImageField(
        blank=True, null=True, upload_to=user_image_path)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def send_password_set_email(self):
        subject = loader.render_to_string('email/set-password-subject.txt')
        subject = ''.join(subject.splitlines())

        body = loader.render_to_string('email/set-password-content.html', {
            'uid': urlsafe_base64_encode(force_bytes(self.pk)),
            'token': default_token_generator.make_token(self),
            'user': self,
        })

        self.email_user(subject, body)

    @property
    def username(self):
        return f'{self.first_name} {self.last_name}'.strip() or self.email.split('@')[0]

    def __str__(self):
        return self.username
