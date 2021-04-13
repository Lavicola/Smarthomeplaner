from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from django.utils.translation import gettext_lazy as _

#https://testdriven.io/blog/django-custom-user-model/
#https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#custom-users-admin-full-example
#https://testdriven.io/blog/django-custom-user-model/

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_('Superuser must have is_active=True.'))


        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
        primary_key=True
    )

    # we do save the region of the user as well e.g to show him the right time. But it is not used right now
    class Language(models.TextChoices):
        ENGLISH_US = "en-us", _("English-US")
        ENGLISH_GB = "en-gb", _("English-GB")
        GERMAN = "de-de" , _("German-DE")
       
    language_choice = models.CharField(
        max_length=5,
        choices= Language.choices,
        default=Language.ENGLISH_US,
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def __str__(self):
        return self.email

  