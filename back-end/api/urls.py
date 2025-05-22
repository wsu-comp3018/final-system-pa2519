from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('login/', views.loginUser),
    path('createAccount/', views.createAccount),
    path('createSession/', views.createSession),
    path('getSessionList/', views.getSessionList),
    path('deleteSession/', views.deleteSession),
    path('transcribe/', views.transcribe),
    path('summary/', views.getSummary),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]