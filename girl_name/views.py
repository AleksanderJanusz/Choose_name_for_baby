from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from girl_name.models import Names, Choice
from django.db.models import Q


class LandingPage(View):
    def get(self, request):
        return render(request, 'girl_name/index.html')


class GirlsNameView(LoginRequiredMixin, View):
    def get(self, request):
        girl_names = Choice.objects.filter(user=request.user).filter(name__gender=1).order_by('name__name')
        return render(request, 'girl_name/girls.html', {'girls': girl_names})


class BoysNameView(LoginRequiredMixin, View):
    def get(self, request):
        boy_names = Choice.objects.filter(user=request.user).filter(name__gender=0).order_by('name__name')
        return render(request, 'girl_name/boys.html', {'boys': boy_names})


class GirlsNameResetView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'girl_name/reset.html')

    def post(self, request):
        user = request.user
        Choice.objects.filter(user_id=user.id).filter(name__gender=1).delete()
        return redirect('girls')


class BoysNameResetView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'girl_name/reset_b.html')

    def post(self, request):
        user = request.user
        Choice.objects.filter(user_id=user.id).filter(name__gender=0).delete()
        return redirect('boys')


class GirlsNameChoose(LoginRequiredMixin, View):
    def get(self, request):
        names = Names.objects.filter(~Q(user=request.user)).filter(gender=1)
        name = names[randint(0, len(names) - 1)]
        return render(request, 'girl_name/choose_girl.html', {'name': name})

    def post(self, request):
        choice = request.POST.get('button')
        name = request.POST.get('name')
        Choice.objects.create(name_id=name, user=request.user, choice=choice)
        return redirect('choose_girl')


class BoysNameChoose(LoginRequiredMixin, View):
    def get(self, request):
        names = Names.objects.filter(~Q(user=request.user)).filter(gender=0)
        name = names[randint(0, len(names) - 1)]
        return render(request, 'girl_name/choose_boy.html', {'name': name})

    def post(self, request):
        choice = request.POST.get('button')
        name = request.POST.get('name')
        Choice.objects.create(name_id=name, user=request.user, choice=choice)
        return redirect('choose_boy')
