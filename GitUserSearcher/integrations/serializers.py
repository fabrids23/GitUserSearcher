from django.contrib.auth.models import User
from rest_framework import serializers
from GitUserSearcher.models import GitUser, SearchHistory


class SearchHistorySerializer(serializers.ModelSerializer):
    gitUser = serializers.RelatedField(read_only=True, source='GitUser')
    #gitUser = serializers.ReadOnlyField(source='GitUser')
    #gitUser = serializers.ModelField(model_field='GitUser')

    class Meta:
        model = SearchHistory
        fields = ['searcherUser', 'gitUser', 'time']


class GitUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = GitUser
        fields = ['username', 'numberOfSearchs', 'hireable']

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        return GitUser.objects.create(**validated_data)


class CurrentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')
