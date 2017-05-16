from django.conf.urls import url, include
from django.contrib import admin
from capture.views import CapturePhoto

urlpatterns = [
    url(r'^$', CapturePhoto.as_view(), name='capture'),
]
