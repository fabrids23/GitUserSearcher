from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.utils import timezone


class GitUser(models.Model):

    username = models.CharField(max_length=100)
    hireable = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class SearchHistory(models.Model):
    searcher_user = models.ForeignKey(User, on_delete=models.CASCADE)
    git_user = models.ForeignKey(GitUser, on_delete=models.CASCADE)
    time = models.DateTimeField(default= timezone.now())

    def __str__(self):
        return self.searcher_user.username + " searched " + self.git_user.username
