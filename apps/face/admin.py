from django.contrib import admin

from face.models import UserSession
from face.models import Friends

admin.site.register(UserSession)
admin.site.register(Friends)
