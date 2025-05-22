from django.db import models
from datetime import date

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

    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    # INVESTIGATOR- Investigator, INSURER- Insurer, LEGAL TEAM - Legal Team
    role = models.CharField(choices=ROLE_CHOICES, default=ROLE_INVESTIGATOR, max_length=100)
    password = models.CharField(max_length=128)

class StatementTemplates(models.Model):
    id = models.IntegerField(primary_key=True)
    slug = models.SlugField(unique=True, max_length=250)
    name = models.CharField(max_length=250)
    template_path = models.FileField(upload_to='templates/', blank=True, null=True)

class Sessions(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    template_id = models.ForeignKey(StatementTemplates, null=True, on_delete=models.CASCADE)
    session_name = models.CharField(max_length=250)
    session_date = models.DateField(default=date.today)
    transcription = models.TextField(blank=True, null=True)
    summarisation = models.TextField(blank=True, null=True)

class Audits(models.Model):
    EVENT_CREATED="CREATED"
    EVENT_UPDATED="UPDATED"
    EVENT_DELETED="DELETED"
    EVENT_CHOICES=[
        (EVENT_CREATED, "created"),
        (EVENT_UPDATED, "updated"), 
        (EVENT_DELETED, "deleted"),
    ]

    id = models.IntegerField(primary_key=True)
    auditable_type = models.TextField()
    auditable_id = models.IntegerField()
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    updated_content = models.TextField(null=True, blank=True)
    event = models.CharField(choices=EVENT_CHOICES, default=EVENT_CREATED, max_length=100)
    old_value = models.TextField()
    new_value = models.TextField()


class Interviewees(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    session_id = models.ForeignKey(Sessions, null=True, on_delete=models.CASCADE)

# class Cases(models.Model):
#     id = models.IntegerField(primary_key=True)
#     case_number = models.IntegerField()
#     case_type = models.TextField()
#     user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
#     date_opened = models.DateField
#     date_closed = models.DateField
#     status = models.TextField()
#     interviewee_id = models.ForeignKey(Interviewees, null=True, on_delete=models.SET_NULL)

 

class Statements(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    interviewee_id = models.ForeignKey(Interviewees, null=True, on_delete=models.SET_NULL)
    statement_content = models.TextField(null=True, blank=True)

 
class AudioRecordings(models.Model):
    id = models.IntegerField(primary_key=True)
    session_id = models.ForeignKey(Sessions, on_delete=models.CASCADE)
    audio_name = models.CharField(max_length=250)
    length = models.DurationField()
    size = models.IntegerField()
    audio_path = models.FileField(upload_to='audio/', blank=True, null=True)
    # audio_path=models.TextField(blank=True, null=True)
    #comment
 

