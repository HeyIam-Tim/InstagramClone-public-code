from rest_framework import serializers

from .models import Publication, SwitchTheme, Comment


class PublicationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Publication
    fields = ['liked']


class SwitchThemeSerializer(serializers.ModelSerializer):
  class Meta:
    model = SwitchTheme
    fields = ['theme']


class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = ['author', 'body']