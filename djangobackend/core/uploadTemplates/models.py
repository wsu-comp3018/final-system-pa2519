from django.db import models

class template(models.Model):
    id=models.IntegerField(primary_key=True)
    slug=models.SlugField(unique=True, blank=True)
    name=models.CharField(max_length=250)
    file=models.FileField(upload_to='templates/')

