from django.contrib import admin
from .models import Users

admin.site.register(Users)

class UsersAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','email','password']