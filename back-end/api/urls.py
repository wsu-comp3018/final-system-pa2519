from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    path('login/', views.loginUser),
    path('logout/', views.logoutUser),
    path('update-account/', views.updateAccountDetails),
    path('create-account/', views.createAccount),
    path('delete-account/', views.deleteAccount),
    path('create-session/', views.createSession),
    path('get-usersettings', views.getAccountSettings),
    path('session-list/', views.getSessionList),
    path('delete-session/', views.deleteSession),
    path('transcribe/', views.transcribe),
    path('summary/', views.getSummary),
    path('generate/', views.generateStatement),
    path('get-statement/', views.getStatement),
    path('update-statement/', views.updateStatement),
    path('delete-statement/', views.deleteStatement),
    path('statement-list', views.getStatementList),
    path('upload-recording/', views.uploadRecordings),
    path('test/', views.test),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]