from django.contrib.auth.models import User
from rest_framework import serializers
from GitUserSearcher.models import GitUser, SearchHistory


class SearchHistorySerializer(serializers.HyperlinkedModelSerializer):
    gitUser = serializers.HyperlinkedRelatedField(many=True, view_name='git-user-detail', read_only=True)

    class Meta:
        model = SearchHistory
        fields = ['searcherUser', 'gitUser', 'time']


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GitUser
        fields = ['username', 'numberOfSearchs', 'hireable']


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
