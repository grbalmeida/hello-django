from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from categories.models import Category

class Post(models.Model):
    post_title = models.CharField(max_length=255, verbose_name='Título')
    post_author = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Autor')
    post_creation_date = models.DateTimeField(default=timezone.now, verbose_name='Data de criação')
    post_content = models.TextField(verbose_name='Conteúdo')
    post_summary = models.TextField(verbose_name='Resumo')
    post_category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='Categoria')
    post_image = models.ImageField(upload_to='post_img/%Y/%m/%d', blank=True, null=True, verbose_name='Imagem')
    post_published = models.BooleanField(default=False, verbose_name='Publicado')

    def __str__(self):
        return self.post_content