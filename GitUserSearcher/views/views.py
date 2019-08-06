from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from requests import Response
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

    def list(self, request):
        queryset = GitUser.objects.all()
        serializer = GitUserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = GitUser.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = GitUserSerializer(user)
        return Response(serializer.data)


# class GitUserDetail(View):

    # def get(self, request, *args, **kwargs):
    #     gitUser = get_object_or_404(GitUser, username=kwargs['gitUsername'])
    #     context = {'gitUser': gitUser}
    #     return render(request, 'GitUserSearch/userDetail.html', context)


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
        print(git_user_instance.data)
        return Response(git_user_instance.data)
    except Exception:
        #print(str(Exception))
        return userNotFound(request)


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




