from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from posts.models import Post

class Comment(models.Model):
    comment_author = models.CharField(max_length=150, verbose_name='Autor')
    comment_email = models.EmailField(verbose_name='E-mail')
    comment = models.TextField(verbose_name='Comentário')
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post')
    comment_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Usuário')
    comment_creation_date = models.DateTimeField(default=timezone.now, verbose_name='Data de criação')
    comment_published = models.BooleanField(default=False, verbose_name='Publicado')

    def __str__(self):
        return self.comment
