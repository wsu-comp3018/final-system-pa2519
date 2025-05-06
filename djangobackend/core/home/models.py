from django.db import models
import enum
from django import forms
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Users(models.Model):

    ROLE_INVESTIGATOR="INVESTIGATOR"
    ROLE_INSURER="INSURER"
    ROLE_LEGAL_TEAM="LEGAL TEAM"
    ROLE_CHOICES=[
        (ROLE_INVESTIGATOR, "Investigator"),
        (ROLE_INSURER, "Insurer"), 
        (ROLE_LEGAL_TEAM, "Legal Team"),
    ]

    id = models.IntegerField()
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    DOB = models.DateField
    # INVESTIGATOR- Investigator, INSURER- Insurer, LEGAL TEAM - Legal Team
    role = models.CharField(choices=ROLE_CHOICES, default=ROLE_INVESTIGATOR)
    organisation = models.CharField(max_length=250, null=True, blank=True)
    password = models.CharField(max_length=128)

class Interviewees(models.Model):
    id = models.IntegerField()
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    DOB = models.DateField
    phone_no = PhoneNumberField()
    language_pref = models.TextField(null=True, blank=True)

class Cases(models.Model):
    id = models.IntegerField()
    case_number = models.IntegerField()
    case_type = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    DOB = models.DateField
    phone_no = PhoneNumberField()
    language_pref = models.TextField(null=True, blank=True)

    class Sessions(models.Model):
        id = models.IntegerField()
        case_id = models.IntegerField()
        user_id = models.IntegerField()
        interviewee_id = models.IntegerField()
        template_id = models.IntegerField()
        session_name = models.CharField(max_length=250)
        session_date = models.DateField

    class AudioRecordings(models.Model):
        id = models.IntegerField()
        session_id = models.IntegerField()
        statement_id = models.IntegerField()
        audio_name = models.CharField(max_length(250))
        length = models.DurationField()
        size = models.IntegerField()
        audio_transcript = models.TextField(blank=True, null=True)
        audio_path = models.FileField(upload_to='audio/', blank=True, null=True)
        # audio_path=models.TextField(blank=True, null=True)

    class StatementTemplates(models.Model):
        id = models.IntegerField()
        slug = models.SlugField(unique=True, max_length=250)
        name = models.CharField(max_length=250)
