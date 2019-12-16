from django import forms
from django.contrib.auth.models import User
from . import models

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = '__all__'
        exclude = ('user',)

class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Password'
    )

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirm password'
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password',
            'password2',
            'email'
        )

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data

        validation_error_messages = {}

        username = cleaned.get('username')
        password = cleaned.get('password')
        password2 = cleaned.get('password2')
        email = cleaned.get('email')

        user_db = User.objects.filter(username=username).first()
        email_db = User.objects.filter(email=email).first()

        user_already_exists_error_message = 'User already exists'
        email_already_exists_error_message = 'Email already registered'
        password_match_error_message = 'Password don\'t match'
        password_short_error_message = 'Password must be at least 6 characters'
        required_field_error_message = 'This field is required'

        if self.user:
            if user_db:
                if username != user_db.username:
                    validation_error_messages['username'] = user_already_exists_error_message

            if password:
                if password != password2:
                    validation_error_messages['password'] = password_match_error_message
                    validation_error_messages['password2'] = password_match_error_message

                if len(password) < 6:
                    validation_error_messages['password'] = password_short_error_message

            if email_db:
                if email != email_db.email:
                    validation_error_messages['email'] = email_already_exists_error_message
        else:
            if user_db:
                validation_error_messages['username'] = user_already_exists_error_message

            if email_db:
                validation_error_messages['email'] = email_already_exists_error_message

            if not password:
                validation_error_messages['password'] = required_field_error_message

            if not password2:
                validation_error_messages['password2'] = required_field_error_message

            if password != password2:
                validation_error_messages['password'] = password_match_error_message
                validation_error_messages['password2'] = password_match_error_message

            if len(password) < 6:
                validation_error_messages['password'] = password_short_error_message

        if validation_error_messages:
            raise(forms.ValidationError(validation_error_messages))
