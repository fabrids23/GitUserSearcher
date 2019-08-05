from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view
from django.views.generic import *
from rest_framework.permissions import IsAuthenticated

from GitUserSearcher.models import GitUser, SearchHistory
from rest_framework import generics, viewsets
from GitUserSearcher.integrations.serializers import SearchHistorySerializer, GitUserSerializer
from GitUserSearcher.integrations.api import make_request


class SearchHistoryList(generics.ListAPIView):
    #todo filtrar que solo me muestre los que busco el usuario logeado, o que solo el admin pueda ver esto
    queryset = SearchHistory.objects.all()
    for search in queryset:
        print(search)
    serializer_class = SearchHistorySerializer


class SearchHireable(generics.ListAPIView):
    queryset = GitUser.objects.filter(hireable=True)
    serializer_class = GitUserSerializer


class GitUserList(generics.ListAPIView):
    queryset = GitUser.objects.all()
    serializer_class = GitUserSerializer


class GitUserDetail(viewsets.ReadOnlyModelViewSet):
    serializer_class = GitUserSerializer
    queryset = GitUser.objects.all()


    # def get_queryset(self):
    #     serializer = GitUserSerializer
    #     queryset = GitUser.objects.all()
    #     lookup_url_kwarg = 'gitUsername'
    #     return GitUser.objects.filter(username=self.kwargs.get('gitUsername'))
    #
    # def get_object(self):
    #     return get_object_or_404(GitUser, username=self.kwargs.get('gitUsername'))


# class GitUserDetail(View):

    # def get(self, request, *args, **kwargs):
    #     gitUser = get_object_or_404(GitUser, username=kwargs['gitUsername'])
    #     context = {'gitUser': gitUser}
    #     return render(request, 'GitUserSearch/userDetail.html', context)


@api_view(['GET'])
def git_user(request, gitUsername, format=None):
    data = make_request(gitUsername)
    #todo trabajar con excepciones??
    try:
        isHireable = True
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
        instance = GitUserSerializer(data=data)
        if instance.is_valid():
            instance.save()
        searchHistory = SearchHistory(searcherUser=request.user, gitUser=user, time=timezone.now())
        searchHistory.save()
        return redirect('/search/users/' + user.username, slug=user.username)
    except Exception:
        return redirect('/search/error/errorNotFound')
    # serializer = GitUserSerializer(user)
    #return redirect('userDetail', user.username)


def userNotFound(request):
    return HttpResponse("User not found")


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




