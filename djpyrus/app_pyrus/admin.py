from django.contrib import admin
from .models import RmsModel, ChainModel, RevisionModel

class RmsAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'login', 'password', 'port', 'scheme', 'version', 'chain']


class ChainAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'login', 'password', 'port', 'scheme', 'version',]


class RevisionAdmin(admin.ModelAdmin):
    list_display = ['revision']


admin.site.register(RmsModel, RmsAdmin)
admin.site.register(ChainModel, ChainAdmin)
admin.site.register(RevisionModel, RevisionAdmin)
