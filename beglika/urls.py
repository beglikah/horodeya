from django.urls import path

from . import views

app_name = 'beglika'

urlpatterns = [
    path('', views.home_page)
]
