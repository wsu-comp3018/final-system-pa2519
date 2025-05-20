from django.contrib import admin
from django.urls import path, include
from home.views import *

urlpatterns = [
    path('',home,name='home'),
    path('api/v1/', include('signup.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/',include('djoser.urls.authtoken')),
    
]
