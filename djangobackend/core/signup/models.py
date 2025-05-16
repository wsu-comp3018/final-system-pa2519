from django.db import models
# from django.db import models
# import enum
# from django import forms
# from django.contrib.auth.models import User
# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# from home.models import Users

# class MyUserManager(BaseUserManager):
#     def create_user(self, email, first_name, last_name, password=None):
#         """
#         Creates and saves a User with the given email, first name, last name
#         and password.
#         """
#         if not email:
#             raise ValueError("Users must have an email address")

#         user = self.model(
#             email=self.normalize_email(email),
#             first_name=first_name,
#             last_name=last_name
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, first_name, last_name, password=None):
#         """
#         Creates and saves a superuser with the given email, date of
#         birth and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#             first_name=first_name,
#             last_name=last_name
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

# class User(AbstractBaseUser):
#     email = models.EmailField(
#         verbose_name="email address",
#         max_length=255,
#         unique=True,
#     )
#     first_name=models.CharField(max_length=250)
#     last_name=models.CharField(max_length=250)
#     # email=models.CharField(max_length=250)
#     # password=models.CharField(max_length=128)
#     is_active = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     created_at=models.DateField(auto_now_add=True)
#     updated_at=models.DateTimeField(auto_now=True)

#     objects=MyUserManager()

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["first_name","last_name","email","password"]

#     def __str__(self):
#         return self.email
    
#     def get_full_name(self):
#         return f"{self.first_name} {self.last_name}"

#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True

#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True

#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         # Simplest possible answer: All admins are staff
#         return self.is_admin

class Users(models.Model):

    ROLE_INVESTIGATOR="INVESTIGATOR"
    ROLE_INSURER="INSURER"
    ROLE_LEGAL_TEAM="LEGAL TEAM"
    ROLE_CHOICES=[
        (ROLE_INVESTIGATOR, "Investigator"),
        (ROLE_INSURER, "Insurer"), 
        (ROLE_LEGAL_TEAM, "Legal Team"),
    ]

    id=models.IntegerField(primary_key=True)
    first_name=models.CharField(max_length=250)
    last_name=models.CharField(max_length=250)
    email=models.CharField(max_length=250)
    DOB=models.DateField
    # INVESTIGATOR- Investigator, INSURER- Insurer, LEGAL TEAM - Legal Team
    role=models.CharField(choices=ROLE_CHOICES, default=ROLE_INVESTIGATOR, max_length=100)
    organisation=models.CharField(max_length=250, null=True, blank=True)
    password=models.CharField(max_length=128)