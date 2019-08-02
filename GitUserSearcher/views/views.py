from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from requests import Response
from rest_framework.decorators import api_view


from GitUserSearcher.models import User , SearchHistory
from rest_framework import generics, status, request
from GitUserSearcher.integrations.serializers import SearchHistorySerializer, UserSerializer
from GitUserSearcher.integrations.api import make_request



class SearchHistory(generics.ListAPIView):
    queryset = SearchHistory.objects.filter(time=timezone.now())
    serializer_class = SearchHistorySerializer


class UserDetails(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def user_detail(request, gitUsername, format=None):
    try:
        user = make_request(gitUsername)
    except Exception:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)


# Testing make_request(username)
@api_view(['GET'])
def git_user(request, format=None):
    data = make_request("fabrids23")
    print(data["login"])
    isHireable = True
    if data["hireable"] is None:
        isHireable = False
    user = User(username=data["login"], numberOfSearchs=1, hireable=isHireable)
    serializer = UserSerializer(user)
    print(serializer.data)
    return Response(serializer.data)

