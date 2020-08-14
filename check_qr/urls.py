from django.contrib import admin
from django.urls import path
from .views import check_qr, qr_reader

urlpatterns = [
    path('', check_qr, name='check_qr'),
    path('reader/', qr_reader, name='qr_reader')
]
