from django.db import models

class UploadTemplate(models.Model):
    id=models.IntegerField(primary_key=True)
    slug=models.SlugField(unique=True, blank=True)
    name=models.CharField(max_length=250)

    def save(self,*args, **kwargs):
        print("Check")
        super(UploadTemplate,self).save(*args, **kwargs)

