import copy
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import models
from . import forms

class BaseUserProfile(View):
    template_name = 'user_profile/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.cart = copy.deepcopy(self.request.session.get('cart', {}))
        self.profile = None

        if self.request.user.is_authenticated:
            self.profile = models.UserProfile.objects.filter(
                user=self.request.user
            ).first()

            self.context = {
                'user_form': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user
                ),

                'user_profile_form': forms.UserProfileForm(
                    data=self.request.POST or None,
                    instance=self.profile
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

        self.user_form = self.context['user_form']
        self.user_profile_form = self.context['user_profile_form']

        if self.request.user.is_authenticated:
            self.template_name = 'user_profile/update.html'

        self.render = render(
            self.request,
            self.template_name,
            self.context
        )

    def get(self, *args, **kwargs):
        return self.render

class Create(BaseUserProfile):
    def post(self, *args, **kwargs):
        if not self.user_form.is_valid() or not self.user_profile_form.is_valid():
            return self.render

        username = self.user_form.cleaned_data.get('username')
        password = self.user_form.cleaned_data.get('password')
        email = self.user_form.cleaned_data.get('email')
        first_name = self.user_form.cleaned_data.get('first_name')
        last_name = self.user_form.cleaned_data.get('last_name')

        if self.request.user.is_authenticated:
            user = get_object_or_404(
                User,
                username=self.request.user.username
            )

            user.username = username

            if password:
                user.set_password(password)

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            if not self.profile:
                self.user_profile_form.cleaned_data['user'] = user
                profile = models.UserProfile(**self.user_profile_form.cleaned_data)
                profile.save()
            else:
                profile = self.user_profile_form.save(commit=False)
                profile.user = user
                profile.save()
        else:
            user = self.user_form.save(commit=False)
            user.set_password(password)
            user.save()

            user_profile = self.user_profile_form.save(commit=False)
            user_profile.user = user
            user_profile.save()

        if password:
            authenticate_user = authenticate(
                self.request,
                username=user,
                password=password
            )

            if authenticate_user:
                login(self.request, user=user)

        self.request.session['cart'] = self.cart
        self.request.session.save()

        messages.success(
            self.request,
            'Your account has been successfully created or updated'
        )

        messages.success(
            self.request,
            'Your are signed in and can complete the purchase'
        )

        return redirect('user_profile:create')

class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(
                self.request,
                'Username or password is invalid'
            )

            return redirect('user_profile:create')

        user = authenticate(
            self.request,
            username=username,
            password=password
        )

        if not user:
            messages.error(
                self.request,
                'Username or password is invalid'
            )

            return redirect('user_profile:create')
        
        login(self.request, user=user)

        messages.success(
            self.request,
            'Login successfully'
        )

        return redirect('product:cart')

class Logout(View):
    def get(self, *args, **kwargs):
        cart = copy.deepcopy(self.request.session.get('cart'))
        logout(self.request)
        self.request.session['cart'] = cart
        self.request.session.save()
        return redirect('product:list')

