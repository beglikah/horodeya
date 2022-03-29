from django.urls import include, path

from accounts import views


urlpatterns = [
    path('', include('allauth.urls')),
    # path(
    #     'accounts/profile/update/<int:pk>',
    #     home_views.UserUpdate.as_view(),
    #     name='user_update'
    # ),
    path('profile/<int:user_id>/photo/update',
         views.user_photo_update, name='user_photo_update'),
    path('profile/<int:pk>', views.account, name='account'),
    path('profile/', views.account, name='my_account'),
    path('profile/notifications', views.notifications, name='notifications'),
]
