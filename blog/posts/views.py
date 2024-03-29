from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.views import View
from django.db.models import Q, Count, Case, When
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post
from comments.forms import CommentForm
from comments.models import Comment

class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 3
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('post_category')
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

'''class PostDetails(UpdateView):
    template_name = 'posts/post_details.html'
    model = Post
    form_class = CommentForm
    context_object_name = 'post'

    def form_valid(self, form):
        post = self.get_object()
        comment = Comment(**form.cleaned_data)
        comment.comment_post = post

        if self.request.user.is_authenticated:
            comment.comment_user = self.request.user

        comment.save()
        
        messages.success(self.request, 'Comment successfully sent')

        return HttpResponseRedirect(self.request.path_info)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = Comment.objects.filter(
            comment_published=True,
            comment_post=post.id
        )

        context['comments'] = comments

        return context

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs.get('id'))'''

class PostDetails(View):
    template_name = 'posts/post_details.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        pk = self.kwargs.get('id')
        post = get_object_or_404(Post, pk=pk, post_published=True)
        comments = Comment.objects.filter(comment_post=post, comment_published=True)

        self.context = {
            'post': post,
            'comments': comments,
            'form': CommentForm(request.POST or None),
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.context.get('form')

        if not form.is_valid():
            return render(request, self.template_name, self.context)

        comment = form.save(commit=False)

        if request.user.is_authenticated:
            comment.comment_user = request.user

        comment.comment_post = self.context.get('post')

        comment.save()

        messages.success(request, 'Comment posted and awaiting review')

        return HttpResponseRedirect(request.path_info)
