from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from GitUserSearcher.views import views
#from GitUserSearcher.views.authviews import obtain_jwt_token
from GitUserSearcher.views.views import user_detail, git_user

urlpatterns = [
    path('admin/', admin.site.urls),
    #url(r'^auth/login/', obtain_jwt_token),
    path('', views.SearchHistory.as_view(), name="search-history"),
    path('users/<int:pk>/', views.UserDetails.as_view(), name="git-user-detail"),
    #url(r'^(?P<gitUsername>\s+)', user_detail),
    path("fabrids23", git_user ),
]
