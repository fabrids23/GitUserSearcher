from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from GitUserSearcher.models import GitUser, SearchHistory


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
        instance.username = validated_data.get('login', instance.username)
        instance.hireable = validated_data.get('hireable', instance.hireable)
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
    git_user = serializers.PrimaryKeyRelatedField(queryset=GitUser.objects.all())
    searcher_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = SearchHistory
        fields = ['searcher_user', 'git_user', 'time']


class SearchHistoryListViewSerialzier(serializers.ModelSerializer):

    git_user = GitUserSerializer()
    searcher_user = CurrentUserWithoutPasswordSerializer()

    class Meta:
        model = SearchHistory
        fields = ['searcher_user', 'git_user', 'time']


