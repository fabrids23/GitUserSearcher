from django.contrib import admin
from .models import User, SearchHistory


class UserAdmin(admin.ModelAdmin):
    fields = ['username', 'numberOfSearchs', 'hireable']


admin.site.register(User, UserAdmin)
