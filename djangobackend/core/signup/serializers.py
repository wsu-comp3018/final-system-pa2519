from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Users


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ("first_name", "last_name", "email", "password")
