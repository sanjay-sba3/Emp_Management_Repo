from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AbstractUser
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    id = models.SmallAutoField(primary_key=True,unique=True)
    username = models.CharField(max_length = 25, unique = True,blank=False,null=False)
    email = models.EmailField(_('email address'), unique = True,)
    country_code = models.CharField(max_length=4, blank=True,null=True)
    phone_no = models.CharField(max_length = 15,blank=True,null=True)
    failed_login_count = models.PositiveIntegerField(default=0)
    is_password_change = models.BooleanField(default=False)
    password = models.CharField(max_length=250)
    created_by = models.IntegerField(null=True,blank=True)
    updated_by = models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    is_active = models.BooleanField(default=1)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','first_name', 'last_name']

    objects = UserManager()

    class Meta:
        db_table = "user_Table"