import re
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django import forms


def password_valid(password):
    if len(password) < 8:
        raise ValidationError('Hasło musi posiadać conajmniej 8 znaków')
    regex_lst = ['[a-z]', '[A-Z]', '[0-9]', '[^a-zA-Z0-9\s]']
    check_list = [re.search(regex, password) is not None for regex in regex_lst]
    if not all(check_list):
        raise ValidationError('Hasło musi zawierać wielką literę, małą literę, cyfrę oraz znak specjalny')


class AddUserForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}), label='')
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}), label='')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Imię'}), label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}), label='', required=False)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise ValidationError('Hasła nie są identyczne')
        password_valid(cleaned_data['password1'])
        return cleaned_data

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}), label='')

    def clean(self):
        cleaned_data = super().clean()
        user = authenticate(**cleaned_data)
        try:
            user_form = User.objects.get(username=cleaned_data['username'])
        except ObjectDoesNotExist:
            raise ValidationError('Niema takiego użytkownika')
        if not user_form.check_password(cleaned_data['password']):
            raise ValidationError('Nie poprawne hasło')
        if user is None:
            raise ValidationError('Musisz aktywować swoje konto')
        cleaned_data['user'] = user
        return cleaned_data
