from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group

from .models import InstagramUser, SwitchTheme


def instagramUser(sender, instance, created, **kwagrs):
  if created:
    group, group_created = Group.objects.get_or_create(name='instagramuser')
    instance.groups.add(group)
    instance.username = instance.username.lower()
    instance.save()
    InstagramUser.objects.create(user=instance)


post_save.connect(instagramUser, sender=User)


def switchTheme(sender, instance, created, **kwagrs):
  if created:
    SwitchTheme.objects.create(user=instance.instagramuser)


post_save.connect(switchTheme, sender=User)