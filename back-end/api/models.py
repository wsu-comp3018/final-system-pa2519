from django.db import models
from datetime import date
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Users(AbstractUser):

    ROLE_INVESTIGATOR="INVESTIGATOR"
    ROLE_INSURER="INSURER"
    ROLE_LEGAL_TEAM="LEGAL TEAM"
    ROLE_CHOICES=[
        (ROLE_INVESTIGATOR, "Investigator"),
        (ROLE_INSURER, "Insurer"), 
        (ROLE_LEGAL_TEAM, "Legal Team"),
    ]

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    # INVESTIGATOR- Investigator, INSURER- Insurer, LEGAL TEAM - Legal Team
    role = models.CharField(choices=ROLE_CHOICES, default=ROLE_INVESTIGATOR, max_length=100)
    password = models.CharField(max_length=128)

class StatementTemplates(models.Model):
    id = models.IntegerField(primary_key=True)
    slug = models.SlugField(unique=True, max_length=250,blank=True)
    name = models.CharField(max_length=250)
    template_path = models.FileField(upload_to='templates/', blank=True, null=True)
    
    def save(self,*args, **kwargs):
        self.slug=slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name
    class Meta:
        unique_together=('name','slug')
class Sessions(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    template_id = models.ForeignKey(StatementTemplates, null=True, on_delete=models.CASCADE)
    session_name = models.CharField(max_length=250)
    session_date = models.DateField(default=date.today)
    transcription = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)

class Audits(models.Model):
    EVENT_CREATED="CREATED"
    EVENT_UPDATED="UPDATED"
    EVENT_DELETED="DELETED"
    EVENT_CHOICES=[
        (EVENT_CREATED, "created"),
        (EVENT_UPDATED, "updated"), 
        (EVENT_DELETED, "deleted"),
    ]

    auditable_type = models.TextField()
    auditable_id = models.IntegerField()
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    updated_content = models.TextField(null=True, blank=True)
    event = models.CharField(choices=EVENT_CHOICES, default=EVENT_CREATED, max_length=100)
    old_value = models.TextField()
    new_value = models.TextField()


class Interviewees(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    session_id = models.ForeignKey(Sessions, null=True, on_delete=models.CASCADE)
    email = models.CharField(max_length=250)
 

class Statements(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    interviewee_id = models.ForeignKey(Interviewees, null=True, on_delete=models.CASCADE)
    statement_content = models.TextField(null=True, blank=True)
    date_created = models.DateField(default=date.today)

 
class AudioRecordings(models.Model):
    session_id = models.ForeignKey(Sessions, on_delete=models.CASCADE)
    audio_name = models.CharField(max_length=250)
    length = models.DurationField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    audio_path = models.FileField(upload_to='audio/', blank=True, null=True)
 

