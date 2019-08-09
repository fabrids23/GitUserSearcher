"""djangoUserSearcher URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls

from djangoUserSearcher import settings

if settings.DEBUG:
    import debug_toolbar
urlpatterns = [
    path('_debug_/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    url(r'^docs/', include_docs_urls(
        title='Git User Searcher',
        description='An API to interact with the GitHub',
        permission_classes=[],
    )),
    path('search/', include('GitUserSearcher.urls')),
]
