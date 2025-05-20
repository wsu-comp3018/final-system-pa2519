from django.shortcuts import render
from .models import Users
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response

class UserView(APIView):

    def get(self,request,format=None):
        users=Users.objects.first()
        serializer=UserSerializer(users)
        return Response(serializer.data)