from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from GitUserSearcher.views import views
from GitUserSearcher.views.authviews import obtain_jwt_token


app_name = "GitUserSearch"
router = routers.DefaultRouter()
router.register(r'users', views.GitUserView)

urlpatterns = [
    url(r'^', include(router.urls)),
    path('admin/', admin.site.urls),
    url(r'^auth/login/', obtain_jwt_token),
    path('view/history', views.SearchHistoryList.as_view(), name="searchHistory"),
    path('view/countHistory', views.history_count),
    path('<str:gitUsername>/', views.git_user),
]

