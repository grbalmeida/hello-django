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
    template_name = 'posts/post_search.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        term = self.request.GET.get('term')

        if not term:
            return queryset

        queryset = queryset.filter(
            Q(post_title__icontains=term) |
            Q(post_author__first_name__iexact=term) |
            Q(post_content__icontains=term) |
            Q(post_summary__icontains=term) |
            Q(post_category__category_name__iexact=term)
        )

        return queryset

class PostCategory(PostIndex):
    template_name = 'posts/post_category.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        category = self.kwargs.get('category')

        if not category:
            return queryset

        queryset = queryset.filter(post_category__category_name__iexact=category)

        return queryset

class PostDetails(UpdateView):
    pass
