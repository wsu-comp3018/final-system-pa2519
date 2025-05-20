from django.db import models
from django.core.files import File

class Users(models.Model):

    ROLE_INVESTIGATOR = "INVESTIGATOR"
    ROLE_INSURER = "INSURER"
    ROLE_LEGAL_TEAM = "LEGAL TEAM"
    ROLE_CHOICES = [
        (ROLE_INVESTIGATOR, "Investigator"),
        (ROLE_INSURER, "Insurer"),
        (ROLE_LEGAL_TEAM, "Legal Team"),
    ]

    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    DOB = models.DateField
    # INVESTIGATOR- Investigator, INSURER- Insurer, LEGAL TEAM - Legal Team
    role = models.CharField(
        choices=ROLE_CHOICES, default=ROLE_INVESTIGATOR, max_length=100
    )
    organisation = models.CharField(max_length=250, null=True, blank=True)
    password = models.CharField(max_length=128)
