from django.views import generic
from .models import Post, Comment, LikeForPost, LikeForComment
from django.http import JsonResponse  # 追加
from django.shortcuts import get_object_or_404  # 追加


class PostList(generic.ListView):
    template_name = 'bbs/post_list.html'
    model = Post


class PostDetail(generic.DetailView):
    template_name = 'bbs/post_detail.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        like_for_post_count = self.object.likeforpost_set.count()
        # ポストに対するイイね数
        context['like_for_post_count'] = like_for_post_count
        # ログイン中のユーザーがイイねしているかどうか
        if self.object.likeforpost_set.filter(user=self.request.user).exists():
            context['is_user_liked_for_post'] = True
        else:
            context['is_user_liked_for_post'] = False

        # {'pk':{'count':コメント数,'is_user_like_for_comment':bool},}という辞書を追加していく
        d = {}
        for comment in self.object.comment_set.all():
            like_for_comment_count = comment.likeforcomment_set.count()
            if comment.likeforcomment_set.filter(user=self.request.user).exists():
                is_user_liked_for_comment = True
            else:
                is_user_liked_for_comment = False
            d[comment.pk] = {'count': like_for_comment_count, 'is_user_liked_for_comment': is_user_liked_for_comment}

        context[f'comment_like_data'] = d

        return context


def like_for_post(request):
    post_pk = request.POST.get('post_pk')
    context = {
        'user': f'{request.user.last_name} {request.user.first_name}',
    }
    post = get_object_or_404(Post, pk=post_pk)
    like = LikeForPost.objects.filter(target=post, user=request.user)

    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(target=post, user=request.user)
        context['method'] = 'create'

    context['like_for_post_count'] = post.likeforpost_set.count()

    return JsonResponse(context)


def like_for_comment(request):
    comment_pk = request.POST.get('comment_pk')
    context = {
        'user': f'{request.user.last_name} {request.user.first_name}',
    }
    comment = get_object_or_404(Comment, pk=comment_pk)
    like = LikeForComment.objects.filter(target=comment, user=request.user)
    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(target=comment, user=request.user)
        context['method'] = 'create'

    context['like_for_comment_count'] = comment.likeforcomment_set.count()

    return JsonResponse(context)
