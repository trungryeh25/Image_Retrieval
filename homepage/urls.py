from django.contrib import admin
from django.urls import path, include
from homepage.views import HomePage
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomePage.as_view(), name='HomePage'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)