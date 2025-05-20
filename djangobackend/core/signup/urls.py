from django.urls import path, include
from signup import views

urlpatterns = [
    path("signup/", views.UserView.as_view(),name='signup'),
]