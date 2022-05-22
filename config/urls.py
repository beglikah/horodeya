"""ITEC URL Configuration

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

from home import views as home_views

import notifications.urls
from django.conf.urls import url

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('anymail/', include('anymail.urls')),
    path('', home_views.home, name='home'),
    path('home/', include('home.urls')),
    path('projects/', include('projects.urls')),
    path('accounts/', include('accounts.urls')),
    path('documents/', include('documents.urls', namespace="documents")),
    path('questionnaires/', include('questionnaires.urls')),
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
    path('check-qr/', include('check_qr.urls')),
    path('admin/', admin.site.urls),
    re_path(
        r'^photologue/', include('photologue.urls', namespace='photologue')
    ),
    url('^inbox/notifications/',
        include(notifications.urls, namespace='notifications')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
