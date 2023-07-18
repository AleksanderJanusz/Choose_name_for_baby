from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse

from accounts.forms import LoginForm, AddUserForm
from accounts.models import Token


def send_token_email(token, request, email, message, url_name):
    current_site = get_current_site(request)
    activation_url = reverse(url_name, kwargs={'token': token.token})
    activation_link = f'http://{current_site.domain}{activation_url}'
    subject = 'Wybierz imię'
    message = f'{message}{activation_link}'
    email_from = 'portfolio.givecare@gmail.com'
    recipient_list = [email]

    send_mail(subject, message, email_from, recipient_list)


class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        url_to_go = request.GET.get('next')
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            if user is not None:
                login(request, user)
            if url_to_go:
                return redirect(url_to_go)
            return redirect('index')
        is_user = User.objects.filter(username=form.cleaned_data['username'])
        if not is_user:
            return redirect('register')
        return render(request, 'accounts/login.html', {'form': form})


class Register(View):
    def get(self, request):
        form = AddUserForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.username = form.cleaned_data['email']
            user.is_active = False
            user.save()
            token = Token.objects.create(user=user)
            message = 'Kliknij w link aby aktywować konto: '
            url_name = 'activate'
            send_token_email(token, request, user.email, message, url_name)
            return redirect('login')
        return render(request, 'accounts/register.html', {'form': form})


class Logout(View):
    def get(self, request):
        url_to_go = request.GET.get('next')
        logout(request)
        if url_to_go:
            return redirect(url_to_go)
        return redirect('index')


class Activate(View):
    def get(self, request, token):
        try:
            activate_token = Token.objects.get(token=token)
        except ObjectDoesNotExist:
            return HttpResponse('Link jest nie aktywny, skontaktuj się z nami w celu rozwiązania problemu')
        if activate_token.active:
            user = User.objects.get(pk=activate_token.user_id)
            user.is_active = True
            user.save()
            activate_token.delete()
            return redirect('login')
        return HttpResponse('Link jest nie aktywny, skontaktuj się z nami w celu rozwiązania problemu')
