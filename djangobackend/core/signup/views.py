from django.shortcuts import render
from .models import Users
from rest_framework.generics import ListAPIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status, authentication, permissions

class UsersList(ListAPIView):
    def get(self,request,format=None):
        users=Users.objects.all()
        serializer=UserSerializer(Users)

        return Response(serializer.data)