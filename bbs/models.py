from django.db import models
from django.utils import timezone
from register.models import User


class Post(models.Model):
    """投稿"""
    writer = models.CharField('投稿者', default='名無し', max_length=32)
    title = models.CharField('タイトル', max_length=256)
    text = models.TextField('本文')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """コメント"""
    writer = models.CharField('名前', default='名無し', max_length=32)
    text = models.TextField('本文')
    target = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='対象記事')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.text[:20]


class LikeForPost(models.Model):
    """投稿に対するいいね"""
    target = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)


class LikeForComment(models.Model):
    """コメントに対するいいね"""
    target = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
