from django.contrib import admin
from .models import GitUser, SearchHistory


class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'hireable']


admin.site.register(GitUser, UserAdmin)
