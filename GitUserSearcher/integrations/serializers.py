from django.contrib.auth.models import User
from rest_framework import serializers
from GitUserSearcher.models import GitUser, SearchHistory

class GitUserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True)

    class Meta:
        model = GitUser
        fields = ['id', 'username', 'numberOfSearchs', 'hireable']
        read_only_fields = ('id',)

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        return GitUser.objects.create(**validated_data)


class SearchHistorySerializer(serializers.ModelSerializer):
    #gitUser = serializers.RelatedField(read_only=True, source='models.GitUser')
    #gitUser = serializers.ReadOnlyField(source='GitUser')
    gitUser = GitUserSerializer()

    class Meta:
        model = SearchHistory
        fields = ['searcherUser', 'gitUser', 'time']


class CurrentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')
