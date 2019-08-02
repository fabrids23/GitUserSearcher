from django.db import models

# Create your models here.


class GitUser(models.Model):
    username = models.CharField(max_length=100)
    numberOfSearchs = models.IntegerField(default=0)
    hireable = models.BooleanField(default=False)


class SearchHistory(models.Model):
    searcherUser = models.CharField(max_length=100)
    gitUser = models.ForeignKey(GitUser, on_delete=models.CASCADE)
    time = models.DateTimeField()
