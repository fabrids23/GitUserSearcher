from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from GitUserSearcher.models import GitUser, SearchHistory
from rest_framework import generics, viewsets
from GitUserSearcher.integrations.serializers import SearchHistorySerializer, GitUserSerializer, SearchHistoryListViewSerialzier
from GitUserSearcher.integrations.api import make_request


class SearchHistoryList(generics.ListAPIView):
    serializer_class = SearchHistoryListViewSerialzier

    def get_queryset(self):
        queryset = SearchHistory.objects.filter(searcher_user=self.request.user)
        return queryset


class SearchHireable(generics.ListAPIView):
    queryset = GitUser.objects.filter(hireable=True)
    serializer_class = GitUserSerializer


class GitUserList(generics.ListAPIView):
    queryset = GitUser.objects.all()
    serializer_class = GitUserSerializer


class GitUserDetail(viewsets.ReadOnlyModelViewSet):
    serializer_class = GitUserSerializer
    queryset = GitUser.objects.all()


@api_view(['GET'])
def history_count(request, format=None):
    all_git_user = GitUser.objects.all()
    count = []
    for git_user in all_git_user:
        count.append(number_of_searchs_to_this_git_username(request, git_user))
    result = []
    for search in count:
        if(search[1] != 0):
            result.append(search)
    return HttpResponse(result)


def number_of_searchs_to_this_git_username(request, gitUsername, format=None):
    try:
        queryset = SearchHistory.objects.filter(searcher_user=request.user, git_user=get_object_or_404(GitUser, username=gitUsername))
        searchs = [gitUsername.__str__(), queryset.count()]
        return searchs
    except:
         return HttpResponse("NO EXISTE")


@api_view(['GET'])
def git_user(request, gitUsername, format=None):
    data = make_request(gitUsername)
    try:
        isHireable = True
        if data["hireable"] is None:
            isHireable = False
        git_user_data = {"username": data["login"], "hireable": isHireable}
        git_user_instance = GitUserSerializer(data=git_user_data)
        try:
            #use get_object_or_404
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
        return JsonResponse(git_user_instance.data)
        #todo quiere el id tambien en la respuesta?
    except Exception:
         return HttpResponse("User not found")




