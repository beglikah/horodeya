from django.urls import path
from documents import views


app_name = 'documents'


urlpatterns = [
    path('', views.DocumentsList.as_view(), name='documents_list'),
    path('create/', views.DocumentCreate.as_view(), name='create'),
    path('pdf-create/', views.upload_doc, name='pdf-create')
]
