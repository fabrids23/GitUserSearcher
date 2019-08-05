from django.db import models

# Create your models here.


#class UserSearchManager(models.Manager):
    #def get_by_natural_key(self, username, hireable, numberOfSearchs):
     #   return self.get(username=username, hireable=hireable, numberOfSearchs=numberOfSearchs)


class GitUser(models.Model):
    #objects = UserSearchManager()

    username = models.CharField(max_length=100)
    numberOfSearchs = models.IntegerField(default=0)
    hireable = models.BooleanField(default=False)

    #def natural_key(self):
    #    return (self.username, self.hireable, self.numberOfSearchs)

    def __str__(self):
        return self.username


class SearchHistory(models.Model):
    searcherUser = models.CharField(max_length=100)
    gitUser = models.ForeignKey(GitUser, on_delete=models.CASCADE)
    time = models.DateTimeField()

    def __str__(self):
        return self.searcherUser + " searched " + self.gitUser.username
