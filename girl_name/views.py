from random import randint
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import generics
from girl_name.models import Names, Choice
from django.db.models import Q

from girl_name.serializers import ChoiceSerializer


class LandingPage(View):
    def get(self, request):
        return render(request, 'girl_name/index.html')


class GirlsNameView(LoginRequiredMixin, View):
    def get(self, request):
        sort = request.COOKIES.get(str(request.user.id))
        if not sort:
            sort = '-choice_change_date'
        girl_names = Choice.objects.filter(user=request.user).filter(name__gender=1).order_by(sort)
        return render(request, 'girl_name/girls.html', {'girls': girl_names})


class SetCookie(View):
    def get(self, request, sort):
        response = redirect('girls')
        response.set_cookie(key=str(request.user.id), value=sort, max_age=60*60*24*7)
        return response


class BoysNameView(LoginRequiredMixin, View):
    def get(self, request):
        sort = request.COOKIES.get(str(request.user.id))
        if not sort:
            sort = '-choice_change_date'
        boy_names = Choice.objects.filter(user=request.user).filter(name__gender=0).order_by(sort)
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
        name = []
        if names:
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


class ChoiceSerializerView(generics.RetrieveUpdateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class GirlComparison(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'girl_name/compare.html')

    def post(self, request):
        email = request.POST.get('email')
        self_user = request.user

        try:
            second_user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return render(request, 'girl_name/compare.html', {'error': 'Niema takiego użytkownika'})

        if second_user == self_user:
            return render(request, 'girl_name/compare.html', {'error': 'To jest twój email'})

        maybe_choices, yes_choices = yes_maybe_choices(second_user, self_user)

        return render(request, 'girl_name/compare_list.html', {'yeah': yes_choices,
                                                               'maybe': maybe_choices})


def yes_maybe_choices(second_user, self_user):
    yes_choices_self = Choice.objects.filter(choice=0).filter(user=self_user).filter(name__gender=1)
    yes_choices = choice_comp(second_user, yes_choices_self)
    maybe_choices_self = Choice.objects.filter(choice=2).filter(user=self_user).filter(name__gender=1)
    maybe_choices = choice_comp(second_user, maybe_choices_self)
    return maybe_choices, yes_choices


def choice_comp(second_user, yes_choices_self):
    yes_choices = [
        Choice.objects.filter(Q(choice=2) | Q(choice=0)).filter(user=second_user).filter(name_id=choice.name_id).first()
        for choice in yes_choices_self if
        Choice.objects.filter(Q(choice=2) | Q(choice=0)).filter(user=second_user).filter(name_id=choice.name_id)]
    return yes_choices


class BoyComparison(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'girl_name/compare_b.html')

    def post(self, request):
        email = request.POST.get('email')
        self_user = request.user

        try:
            second_user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return render(request, 'girl_name/compare_b.html', {'error': 'Niema takiego użytkownika'})

        if second_user == self_user:
            return render(request, 'girl_name/compare_b.html', {'error': 'To jest twój email'})

        maybe_choices, yes_choices = yes_maybe_choices(second_user, self_user)
        return render(request, 'girl_name/compare_list_b.html', {'yeah': yes_choices,
                                                                 'maybe': maybe_choices})
