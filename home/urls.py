from django.conf.urls import url
from cookielaw import views


urlpatterns = [
    url(r'^get-user-ip/$', views.get_user_ip, name='get-user-ip'),
    url(r'^track_user/$', views.track_user, name='track_user'),
    url(r'^cookie/$', views.test_cookie, name='cookie'),
]
