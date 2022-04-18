from django.urls import path, re_path
from documents import views


app_name = 'documents'


urlpatterns = [
    path('', views.DocumentsList.as_view(), name='documents_list'),
    path(
        '<int:pk>/<slug:slug>/', views.DocumentDetails.as_view(), name='document_details'
    ),
    re_path('download/(?P<path>.*)', views.download, ),
]
