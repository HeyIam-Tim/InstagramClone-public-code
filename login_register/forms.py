from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):
  password1 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
  password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
  class Meta:
    model = User
    fields = ['username', 'first_name', 'email', 'password1', 'password2',]
    widgets = {
      'username':forms.TextInput(attrs={'placeholder': 'Username'}),
      'first_name':forms.TextInput(attrs={'placeholder': 'Full Name'}),
      'email':forms.EmailInput(attrs={'placeholder': 'Email'}),
    }