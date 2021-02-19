from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from .models import InstagramUser, Publication


class InstagramUserForm(ModelForm):
  profile_pic = forms.ImageField(widget=forms.FileInput)
  class Meta:
    model = InstagramUser
    fields = ['profile_pic']


class UpdateUserForm(ModelForm):
  class Meta:
    model = User
    fields = ['username', 'first_name']


class UpdatePublicationForm(ModelForm):
  image = forms.ImageField(widget=forms.FileInput)
  class Meta:
    model = Publication
    fields = ['image', 'description']