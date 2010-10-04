from blog.models import Post
from blog.models import  Tag
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
