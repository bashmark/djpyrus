from django.contrib import admin
from .models import RmsModel, ChainModel

class RmsAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'login', 'password', 'port', 'scheme', 'version', 'chain']


class ChainAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'login', 'password', 'port', 'scheme', 'version',]


admin.site.register(RmsModel, RmsAdmin)
admin.site.register(ChainModel, ChainAdmin)
