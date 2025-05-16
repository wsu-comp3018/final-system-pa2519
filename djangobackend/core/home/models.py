# from django.db import models
# import enum
# from django import forms
# # from django.contrib.auth.models import User
# # from phonenumber_field.modelfields import PhoneNumberField

# # Create your models here.
# class Users(models.Model):

#     ROLE_INVESTIGATOR="INVESTIGATOR"
#     ROLE_INSURER="INSURER"
#     ROLE_LEGAL_TEAM="LEGAL TEAM"
#     ROLE_CHOICES=[
#         (ROLE_INVESTIGATOR, "Investigator"),
#         (ROLE_INSURER, "Insurer"), 
#         (ROLE_LEGAL_TEAM, "Legal Team"),
#     ]

#     id=models.IntegerField(primary_key=True)
#     first_name=models.CharField(max_length=250)
#     last_name=models.CharField(max_length=250)
#     email=models.CharField(max_length=250)
#     DOB=models.DateField
#     # INVESTIGATOR- Investigator, INSURER- Insurer, LEGAL TEAM - Legal Team
#     role=models.CharField(choices=ROLE_CHOICES, default=ROLE_INVESTIGATOR, max_length=100)
#     organisation=models.CharField(max_length=250, null=True, blank=True)
#     password=models.CharField(max_length=128)

# class Interviewees(models.Model):
#     id=models.IntegerField(primary_key=True)
#     first_name=models.CharField(max_length=250)
#     last_name=models.CharField(max_length=250)
#     email=models.CharField(max_length=250)
#     DOB=models.DateField
#     phone_no=models.CharField(max_length=15)
#     language_pref=models.TextField(null=True, blank=True)

# class Cases(models.Model):
#     id=models.IntegerField(primary_key=True)
#     case_number=models.IntegerField()
#     case_type=models.TextField()
#     user_id=models.IntegerField()
#     date_opened=models.DateField
#     date_closed=models.DateField
#     status=models.TextField()
#     interviewee_id=models.IntegerField()

# class Audits(models.Model):
#     EVENT_CREATED="CREATED"
#     EVENT_UPDATED="UPDATED"
#     EVENT_DELETED="DELETED"
#     EVENT_CHOICES=[
#         (EVENT_CREATED, "created"),
#         (EVENT_UPDATED, "updated"), 
#         (EVENT_DELETED, "deleted"),
#     ]

#     id=models.IntegerField(primary_key=True)
#     auditable_type=models.TextField()
#     auditable_id=models.IntegerField()
#     user_id=models.IntegerField()
#     updated_content=models.TextField(null=True, blank=True)
#     event=models.CharField(choices=EVENT_CHOICES, default=EVENT_CREATED, max_length=100)
#     old_value=models.TextField()
#     new_value=models.TextField()
    
# class Statements(models.Model):
#     id=models.IntegerField(primary_key=True)
#     case_id=models.IntegerField()
#     user_id=models.IntegerField()
#     interviewee_id=models.IntegerField()
#     audio_id=models.IntegerField()
#     audio_transcript=models.TextField(null=True, blank=True)
#     updated_content=models.TextField(null=True, blank=True)

# class Sessions(models.Model):
#          id = models.IntegerField(primary_key=True)
#          case_id = models.IntegerField()
#          user_id = models.IntegerField()
#          interviewee_id = models.IntegerField()
#          template_id = models.IntegerField()
#          session_name = models.CharField(max_length=250)
#          session_date = models.DateField
 
# class AudioRecordings(models.Model):
#     id = models.IntegerField(primary_key=True)
#     session_id = models.IntegerField()
#     statement_id = models.IntegerField()
#     audio_name = models.CharField(max_length=250)
#     length = models.DurationField()
#     size = models.IntegerField()
#     audio_transcript = models.TextField(blank=True, null=True)
#     audio_path = models.FileField(upload_to='audio/', blank=True, null=True)
#     # audio_path=models.TextField(blank=True, null=True)
#     #comment
 
# class StatementTemplates(models.Model):
#     id = models.IntegerField(primary_key=True)
#     slug = models.SlugField(unique=True, max_length=250)
#     name = models.CharField(max_length=250)

