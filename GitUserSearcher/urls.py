from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from GitUserSearcher.views import views
from GitUserSearcher.views.authviews import obtain_jwt_token
#from GitUserSearcher.views.views import user_detail, git_user

app_name = "GitUserSearch"
router = routers.DefaultRouter()
router.register(r'users', views.GitUserDetail)

urlpatterns = [
    url(r'^', include(router.urls)),
    path('admin/', admin.site.urls),
    url(r'^auth/login/', obtain_jwt_token),
    path('view/history', views.SearchHistoryList.as_view(), name="searchHistory"),
    path('view/userList', views.GitUserList.as_view(), name="userList"),
    # path('users/<slug:gitUsername>/', views.GitUserDetails.as_view(), name="userDetail"),
    path('hireable/', views.SearchHireable.as_view(), name='hireable'),
    #path('users/<str:gitUsername>/', views.GitUserDetails.as_view(), name="userDetail"),
    #path('^(?P<gitUsername>\s+)/', views.GitUserDetails.git_user),
    path('<str:gitUsername>/', views.git_user),
    #path('fabrids23/', views.git_user),
    path('error/errorNotFound', views.userNotFound, name="errorNotFound"),
]

# urlpatterns = format_suffix_patterns(urlpatterns)


