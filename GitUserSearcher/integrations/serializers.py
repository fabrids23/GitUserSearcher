from rest_framework import serializers
from GitUserSearcher.models import User, SearchHistory


class SearchHistorySerializer(serializers.HyperlinkedModelSerializer):
    gitUser = serializers.HyperlinkedRelatedField(many=True, view_name='git-user-detail', read_only=True)

    class Meta:
        model = SearchHistory
        fields = ['searcherUser', 'gitUser', 'time']


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'numberOfSearchs', 'hireable']