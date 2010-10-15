from django.contrib import admin

from face.models import UserSession
from face.models import Friend
from face.models import FriendCompare

admin.site.register(UserSession)
admin.site.register(Friend)
admin.site.register(FriendCompare)
