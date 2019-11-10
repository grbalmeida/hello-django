from django.forms import ModelForm
from .models import Comment

class CommentForm(ModelForm):
    def clean(self):
        data = self.cleaned_data
        comment_author = data.get('comment_author')
        comment_email = data.get('comment_email')
        comment = data.get('comment')

        if len(comment_author) < 5:
            self.add_error(
                'comment_author',
                'Name must be at least 5 characters'
            )

    class Meta:
        model = Comment
        fields = (
            'comment_author',
            'comment_email',
            'comment'
        )