from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, update_session_auth_hash

from .models import User
from .forms import *
from .token import activation_token
from movie.models import CustomerRating


# Create your views here.


# def activate(request, uidb64, token):
#     try:
#         id = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=id)
#     except(TypeError, ValueError, User.DoesNotExist):
#         user = None
#
#     if user is not None and activation_token.check_token(user, token) :
#         user.is_verified = True
#         user.save()
#         return HttpResponse("verify success")
#     else:
#         return HttpResponse('verify fail')


class RegisterView(View):
    template_name = "register.html"
    Model = User

    def get(self, request):
        context = {
            'form' : RegisterForm(),
            'current_tab' : 'register'
        }
        return TemplateResponse(request, self.template_name, context)

    def post(self, request):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            request.session['register'] = 'Register successfully'
            messages.success(request, 'Registration successful. You can now log in.')
            return HttpResponseRedirect('login')
        else:
            print(form.errors)
            messages.error(request, 'Registration failed. Please check the form and try again.')
        return HttpResponseRedirect("register")


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        context = {
            'form' : LoginForm(),
            'current_tab' : 'login'
        }
        return TemplateResponse(request, self.template_name, context)

    def post(self, request):
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                print("login ne")
                request.session['login'] = 'login Successfully'
                return HttpResponseRedirect("/")
            else:
                print('cut')
                messages.error(request, 'Login failed. Please check the username and password carefully.')
                return HttpResponseRedirect("/login")
        else:
            request.session['login'] = 'login fail'
            print(form.errors)
            messages.error(request, 'Login failed. Please check the username and password carefully.')
            return HttpResponseRedirect("/login")
        


@login_required(login_url='/login')
def profile(request, id):
    user = User.objects.get(id=id)

    if user.score < 100 :
        user.membership = 'standard'
    elif 100 <= user.score < 300:
        user.membership = 'premium'
    else :
        user.membership = 'VIP'

    if not user.avatar:
        user.avatar = "/static/popcorn.png"
    user.save()
    review = CustomerRating.objects.filter(user=user)
    return render(request, 'profile.html', {'user': user, 'review': review})


@login_required(login_url='/login')
def update_profile(request, id):
    user = User.objects.get(id=id)
    form = UpdateProfileForm(instance=user)

    if request.method == "POST":
        form = UpdateProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            user.save()
            request.session['update_profile'] = 'update profile Successfully'
            return redirect(f'/profile/{id}')
        else :
            print(form.errors)
            request.session['login'] = 'update profile fail'
    else:
        print(request.method)
    return render(request, "update_profile.html", {"form": form})


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })