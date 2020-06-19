from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Profile,FriendManager


admin.site.unregister(Group)
admin.site.register(Profile)
admin.site.register(FriendManager)
