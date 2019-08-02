from django.contrib import admin
from .models import GitUser, SearchHistory


class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'numberOfSearchs', 'hireable']


admin.site.register(GitUser, UserAdmin)
