from django.contrib import admin
from .models import *


class PublicationAdmin(admin.ModelAdmin):
  list_display = ('description', 'likes')

class SwitchThemeAdmin(admin.ModelAdmin):
  list_display = ('user', 'theme')

admin.site.register(InstagramUser)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(SwitchTheme, SwitchThemeAdmin)
admin.site.register(Comment)
