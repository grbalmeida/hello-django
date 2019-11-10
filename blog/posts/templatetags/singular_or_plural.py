from django import template

register = template.Library()

@register.filter(name='singular_or_plural')
def singular_or_plural(number_of_comments):
    try:
        number_of_comments = int(number_of_comments)

        if number_of_comments == 0:
            return 'No comment'
        elif number_of_comments == 1:
            return f'{number_of_comments} comment'
        else:
            return f'{number_of_comments} comments'

        return f'{number_of_comments} comment'
    except:
        return f'{number_of_comments} comment(s)'