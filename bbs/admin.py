from django.contrib import admin
from .models import Post, Comment, LikeForPost, LikeForComment

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(LikeForPost)
admin.site.register(LikeForComment)
