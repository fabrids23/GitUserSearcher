from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from GitUserSearcher.models import GitUser, SearchHistory
from django.shortcuts import get_object_or_404


class GitUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    hireable = serializers.BooleanField(default=False)

    class Meta:
        model = GitUser
        fields = ['id', 'username', 'hireable']
        read_only_fields = ('id',)

    def create(self, validated_data):
        return GitUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        isHireable = True
        if validated_data["hireable"] is None:
            isHireable = False
        instance.username = validated_data.get('login', instance.username)
        instance.hireable = isHireable
        instance.save()
        return instance


class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class CurrentUserWithoutPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username',]
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class SearchHistorySerializer(serializers.ModelSerializer):
    git_user = GitUserSerializer()
    searcher_user = CurrentUserWithoutPasswordSerializer()

    class Meta:
        model = SearchHistory
        fields = ['searcher_user', 'git_user', 'time']

    def create(self, validated_data):
        searcher_user_data = validated_data.get("searcher_user")
        git_user_data = validated_data.get("git_user")
        git_user = get_object_or_404(GitUser, username=git_user_data["username"])
        searcher_user = get_object_or_404(User, username=searcher_user_data["username"])
        search_history = SearchHistory(searcher_user=searcher_user, git_user=git_user)
        search_history.save()
        return search_history
