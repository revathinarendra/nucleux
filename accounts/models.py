from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from nucleux import settings  
from django.utils.text import slugify
import uuid


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email address")

        if not username:
            raise ValueError("User must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superadmin', True)

        return self.create_user(first_name, last_name, email, username, password, **extra_fields)


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(default=timezone.now)

    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other")
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    username = models.CharField(max_length=100, unique=True,blank=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15,null=True)
    referral = models.ForeignKey('Referral', on_delete=models.SET_NULL, null=True, blank=True)
    profession = models.ForeignKey('Profession', on_delete=models.SET_NULL, null=True, blank=True)
    university = models.ForeignKey('University', on_delete=models.SET_NULL, null=True, blank=True)
    expected_graduation_date = models.CharField(null=True, blank=True)
    current_area_of_focus = models.ForeignKey(
        'Objectives', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='focused_accounts'
    )
    objectives = models.ForeignKey(
        'Objectives', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='objective_accounts'
    )


    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "date_of_birth", "gender"]

    objects = MyAccountManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email  # Set username to email if not provided
        super().save(*args, **kwargs)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="userprofile")
    address_line_1 = models.CharField(blank=True,null=True, max_length=100)
    address_line_2 = models.CharField(blank=True,null=True ,max_length=100)
    phone_number = models.CharField(null=True ,blank=True,max_length=15)
    profile_picture = models.ImageField(upload_to="userprofile", blank=True)
    city = models.CharField(blank=True, null=True ,max_length=20)
    state = models.CharField(blank=True, null=True ,max_length=20)
    country = models.CharField(blank=True, null=True ,max_length=20)

    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2}"


class Referral(models.Model):
    referral_name = models.CharField(max_length=100,null=True,blank=True)
    

    def __str__(self):
        return self.referral_name


class Profession(models.Model):
    profession_name = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.profession_name
    
class University(models.Model):
    country_name = models.CharField(max_length=200,default="india")
    university_name = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self):
        return self.university_name
    
class Objectives(models.Model):
    objective_name = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.objective_name

@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
class EmailVerificationToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        expiration_time = timezone.now() - timezone.timedelta(hours=24)
        return self.created_at < expiration_time

    def regenerate_token(self):
        self.token = uuid.uuid4()
        self.created_at = timezone.now()
        self.save()
