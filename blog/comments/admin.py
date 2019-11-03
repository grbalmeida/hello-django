from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'comment_author',
        'comment_email',
        'comment',
        'comment_creation_date',
        'comment_published',
    )

    list_display_links = (
        'id',
        'comment_author',
        'comment_email',
    )

admin.site.register(Comment, CommentAdmin)
