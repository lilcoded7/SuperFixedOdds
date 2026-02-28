# Django imports
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import uuid
from setup.basemodel import BaseModel
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


class MyAccountManager(BaseUserManager):
    def create_superuser(self, phone_number, password):
        if not phone_number:
            raise ValueError("Users must have a phone number.")
        if len(password) < 8:
            raise ValueError("Password must contain at least 8 characters")

        user = self.model(phone_number=phone_number)
        user.is_superuser = True
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password):
        if not phone_number:
            raise ValueError("enter phone number")
       
        if len(password) < 8:
            raise ValueError("Password 8 must contain at least 8 characters")

        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=100,  unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last joined", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name_plural = "Users"
        ordering = ["-id"]

    def __str__(self):
        return str(self.phone_number)


    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class UserVerificationCode(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_code = models.CharField(max_length=6, null=True, blank=True)
   
    phone_verified = models.BooleanField(default=False)
    phone_code_expires = models.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return f"{self.phone_code}"

    class Meta:
        verbose_name_plural = "Verification Codes"
        ordering = ["created_at"]
 


class LoggedInUserDevices(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="logged_in_user_user"
    )
    ip_address = models.GenericIPAddressField()
    os = models.CharField(max_length=255)
    browser = models.CharField(max_length=255)
    expires = models.DateTimeField(default=datetime.utcnow)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()}-{self.ip_address}"


    class Meta:
        ordering = ["-created_at"]