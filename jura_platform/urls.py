from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("auth/", include('authentication.urls')),
]

# Admin only in development
if settings.DEBUG:
    urlpatterns.append(path("admin/", admin.site.urls))