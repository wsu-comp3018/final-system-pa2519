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
    path('createAccount/', views.createAccount),
    path('createSession/', views.createSession),
    path('getSessionList/', views.getSessionList),
    path('deleteSession/', views.deleteSession),
    path('transcribe/', views.transcribe),
    path('summary/', views.getSummary),
    path('upload/',views.uploadTemplates,name='templates'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)