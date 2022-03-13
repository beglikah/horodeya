"""horodeya URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

from home import views as home_views

import notifications.urls
from django.conf.urls import url

urlpatterns = [
    path('accounts/profile/notifications',
         home_views.notifications, name='notifications'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('anymail/', include('anymail.urls')),
    path('accounts/profile/', home_views.account, name='my_account'),
    path('accounts/profile/<int:pk>', home_views.account, name='account'),
    path('accounts/', include('allauth.urls')),
    path('projects/', include('projects.urls')),
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
    path('check-qr/', include('check_qr.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^photologue/', include('photologue.urls', namespace='photologue')),
    re_path(r'^cms/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'', include(wagtail_urls)),
    # path('accounts/profile/update/<int:pk>', home_views.UserUpdate.as_view(), name='user_update'),
    url('^inbox/notifications/',
        include(notifications.urls, namespace='notifications')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
