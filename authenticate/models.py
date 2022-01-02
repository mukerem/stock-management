
from django.utils.safestring import mark_safe
from django.core.exceptions  import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.timezone import now

class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password='admin', role=None):
        """
        Creates and saves a User with the given email 
        and <li ><a href="#">{{user.username}}</a></li>password.
        """
        if not username:
            raise ValueError('Users must have an user name')
        
        if not first_name:
            raise ValueError('Users must have an first name')

        if not last_name:
            raise ValueError('Users must have an last name')

        if not role:
            raise ValueError('Users must have at least 1 role')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            role=role,
            register_date=timezone.now().date(),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, password):
        """
        Creates and saves a superuser with the given email, password ...
        """
        user = self.create_user(
            username=username,
            first_name=' ',
            last_name=' ',
            password=password,
            role='manager',
        )
        
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name='user name',
        max_length=255,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        blank=True,
    )

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,15}$',
        message='Phone number must be entered in the format : 09******** or +2519******** up to 15 digits allowed',
        )
        
    phone = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    sex = models.CharField(max_length=200, choices=(('male', 'male'), ('female', 'female')))
    photo = models.ImageField(blank=True, upload_to='', default='null.png')
    is_admin = models.BooleanField(default=False)
    role = models.CharField(max_length=200, choices=(('manager', 'manager'), ('seller', 'seller')))
    register_date = models.DateField(default = now)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150"/>' % self.photo.url)

    image_tag.short_description = 'Photo'
    image_tag.allow_tags = True

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
