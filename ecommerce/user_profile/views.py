from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from . import models
from . import forms

class BaseUserProfile(View):
    template_name = 'user_profile/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        if self.request.user.is_authenticated:
            self.context = {
                'user_form': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user
                ),

                'user_profile_form': forms.UserProfileForm(
                    data=self.request.POST or None
                )
            }
        else:
            self.context = {
                'user_form': forms.UserForm(
                    data=self.request.POST or None
                ),

                'user_profile_form': forms.UserProfileForm(
                    data=self.request.POST or None
                )
            }

        self.render = render(
            self.request,
            self.template_name,
            self.context
        )

    def get(self, *args, **kwargs):
        return self.render

class Create(BaseUserProfile):
    def post(self, *args, **kwargs):
        return self.render

class Update(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Update')

class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')

class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Logout')
