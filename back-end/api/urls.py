from django.contrib import admin
from . import views
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework.routers import DefaultRouter
from .views import uploadTemplates


# router=DefaultRouter()
# router.register(r'StatementTemplates',uploadTemplates)

urlpatterns = [
    path('login/', views.loginUser),
    path('logout/', views.logoutUser),
    path('reset/', views.resetPassword),
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
    #path('downloadRecording/', views.downloadRecording),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)