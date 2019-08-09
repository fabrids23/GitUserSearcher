from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from GitUserSearcher.models import GitUser, SearchHistory
from rest_framework import generics, viewsets
from GitUserSearcher.integrations.serializers import SearchHistorySerializer, GitUserSerializer, \
    SearchHistoryListViewSerializer
from GitUserSearcher.integrations.api import make_request
from django_filters import FilterSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class SearchHistoryList(generics.ListAPIView):
    serializer_class = SearchHistoryListViewSerializer

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        if user.is_superuser:
            queryset = SearchHistory.objects.all()
        else:
            queryset = SearchHistory.objects.filter(searcher_user=self.request.user)
        return queryset


class GitUserFilter(FilterSet):
    class Meta:
        model = GitUser
        fields = ('hireable', 'username', 'id',)


class GitUserView(viewsets.ReadOnlyModelViewSet):
    serializer_class = GitUserSerializer
    queryset = GitUser.objects.all()
    search_fields = ('hireable', 'username', 'id',)
    filter_class = GitUserFilter
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['username', 'hireable']


@api_view(['GET'])
def history_count(request):
    if request.user.is_superuser:
        searchs_by_this_user = SearchHistory.objects.all().values('searcher_user', 'git_user').annotate(count=Count('git_user'))
        return Response(searchs_by_this_user)
    else:
        searchs_by_this_user = SearchHistory.objects.filter(searcher_user=request.user).values('git_user').annotate(count=Count('git_user'))
        return Response(searchs_by_this_user)


@api_view(['GET'])
def git_user(request, gitUsername):
    data = make_request(gitUsername)
    try:
        isHireable = True
        if data["hireable"] is None:
            isHireable = False
        git_user_data = {"username": data["login"], "hireable": isHireable}
        git_user_instance = GitUserSerializer(data=git_user_data)
        try:
            prevUser = GitUser.objects.get(username=data["login"])
            if git_user_instance.is_valid():
                git_user_instance.update(prevUser, git_user_data)
        except GitUser.DoesNotExist:
            if git_user_instance.is_valid():
                git_user_instance.save()
        id = GitUser.objects.get(username=data["login"]).id
        search_history_data = {"searcher_user": request.user.id, "git_user": id}
        search_history_instance = SearchHistorySerializer(data=search_history_data)
        if search_history_instance.is_valid():
            search_history_instance.save()
        return Response(git_user_instance.data)
    except Exception:
        return Response("User not found")
