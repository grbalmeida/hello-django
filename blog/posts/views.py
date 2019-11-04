from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.db.models import Q, Count, Case, When
from .models import Post

class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 3
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-id').filter(post_published=True)
        queryset = queryset.annotate(
            number_of_comments=Count(
                Case(
                    When(comment__comment_published=True, then=1)
                )
            )
        )

        return queryset

class PostSearch(PostIndex):
    pass

class PostCategory(PostIndex):
    pass

class PostDetails(UpdateView):
    pass
