import django_filters
from django_filters import CharFilter
from django.contrib.auth.models import User
from django.forms.widgets import TextInput

class FollowingFilter(django_filters.FilterSet):
  first_name = CharFilter(field_name='first_name', lookup_expr='icontains', label='', widget=TextInput(attrs={'placeholder': 'type here...'}))
  class Meta:
    model = User
    fields = 'first_name',


class FollowerFilter(django_filters.FilterSet):
  first_name = CharFilter(field_name='first_name', lookup_expr='icontains', label='', widget=TextInput(attrs={'placeholder': 'type here...'}))
  class Meta:
    model = User
    fields = 'first_name',