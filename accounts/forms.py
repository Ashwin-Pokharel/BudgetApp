from .models import User,Expense,Incomes,Category
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms

class SignInForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=False)
    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2',)

class loginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', widget=forms.PasswordInput())


class Expense_form(ModelForm):
    class Meta:
        model = Expense
        exclude = ('user',)
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class Income_form(ModelForm):
    class Meta:
        model = Incomes
        exclude = ('user',)
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

