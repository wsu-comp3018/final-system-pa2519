from django.urls import path
from signup import views

urlpatterns = [
    path('users/', views.UsersList.as_view()),
]