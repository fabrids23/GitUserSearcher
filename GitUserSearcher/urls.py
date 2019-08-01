from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from GitUserSearcher.views.authviews import obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^auth/login/', obtain_jwt_token),
]
