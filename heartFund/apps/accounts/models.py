from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            first_name = first_name,
            last_name = last_name,
            phone = phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, first_name, last_name, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        return self.create_user(email, first_name, last_name, phone, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length = 150)
    last_name = models.CharField(max_length = 150)
    email = models.EmailField(unique=True)

    phone_regex = RegexValidator(
        regex=r"^01[0-2,5][0-9]{8}$",
        message="Phone number must be a valid Egyptian mobile number (e.g., 010xxxxxxxx)"
    )
    phone = models.CharField(validators=[phone_regex], max_length=11, unique=True)
    payment_info = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="e.g. PayPal email, bank account number, or wallet ID"
    )
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"  
    REQUIRED_FIELDS = ["first_name", "last_name", "phone"]
    