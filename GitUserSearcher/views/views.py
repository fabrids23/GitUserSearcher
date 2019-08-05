from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view
from django.views.generic import *
from GitUserSearcher.models import GitUser, SearchHistory
from rest_framework import generics
from GitUserSearcher.integrations.serializers import SearchHistorySerializer, GitUserSerializer
from GitUserSearcher.integrations.api import make_request


class SearchHistoryList(generics.ListAPIView):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer


class GitUserList(generics.ListAPIView):
    queryset = GitUser.objects.all()
    serializer_class = GitUserSerializer


class GitUserDetails(DetailView):
    model = GitUser
    slug_field = 'username'
    serializer_class = GitUserSerializer
    slug_url_kwarg = 'gitUsername'
    #queryset = GitUser.objects.get(username=slug_field)

    #
    # def get_queryset(self):
    #     serializer = GitUserSerializer
    #     queryset = GitUser.objects.all()
    #     lookup_url_kwarg = 'gitUsername'
    #     return GitUser.objects.filter(username=self.kwargs.get('gitUsername'))
    #
    # def get_object(self):
    #     return get_object_or_404(GitUser, username=self.kwargs.get('gitUsername'))


@api_view(['GET'])
def git_user(request, gitUsername, format=None):
    data = make_request(gitUsername)
    isHireable = True
    #todo si no existe en git, que no lo cree
    if data["hireable"] is None:
        isHireable = False
    try:
        # todo usar create y update en serializers
        prevUser = GitUser.objects.get(username=data["login"])
        newNumberOfSearchs = prevUser.numberOfSearchs + 1
        prevUser.hireable = isHireable
        prevUser.numberOfSearchs = newNumberOfSearchs
        user = prevUser
    except GitUser.DoesNotExist:
        user = GitUser(username=data["login"], numberOfSearchs=1, hireable=isHireable)
    user.save()
    # todo que el usuario que busca lo obtengamos de la app
    searchHistory = SearchHistory(searcherUser="test", gitUser=user, time=timezone.now())
    searchHistory.save()
    # serializer = GitUserSerializer(user)
    return redirect('userDetail', user.username)


# Testing make_request(username)
# @api_view(['GET'])
# def git_user(request, format=None):
#     data = make_request("fabrids23")
#     print(data["login"])
#     isHireable = True
#     if data["hireable"] is None:
#         isHireable = False
#     user = User(username=data["login"], numberOfSearchs=1, hireable=isHireable)
#     serializer = UserSerializer(user)
#     print(serializer.data)
#     return Response(serializer.data)
#




