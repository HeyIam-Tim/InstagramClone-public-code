from django.apps import AppConfig


class IgcloneConfig(AppConfig):
    name = 'igclone'

    def ready(self):
      import igclone.signals