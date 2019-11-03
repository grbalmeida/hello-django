from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post

class PostAdmin(SummernoteModelAdmin):
    list_display = (
        'id',
        'post_title',
        'post_author',
        'post_creation_date',
        'post_category',
        'post_published',
    )

    list_editable = ('post_published',)

    list_display_links = (
        'id',
        'post_title',
    )

    summernote_fields = ('post_content',)

admin.site.register(Post, PostAdmin)
