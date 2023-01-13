from django.contrib import admin
from django.contrib.auth.models import User, Group

from users.models import UserProfile
from .models import Tweet


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username']
    inlines = [UserProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Tweet)