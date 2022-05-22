from django.urls import path

from questionnaires import views


urlpatterns = [
    path('', views.QuestionnairesList.as_view(), name='questionnaires_list'),
    path(
        'create/', views.QuestionnaireCreate.as_view(),
        name='create_questionnaire'
    ),
    path(
        '<int:pk>/', views.QuestionnaireDetail.as_view(),
        name='questionnaire_detail'
    ),
]
