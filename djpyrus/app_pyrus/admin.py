from django.contrib import admin
from .models import RmsModel, ChainModel, RevisionModel, RemotesModel

class RmsAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'login', 'password', 'port', 'scheme', 'version', 'chain']
    search_fields = ['name', 'address']


class ChainAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'login', 'password', 'port', 'scheme', 'version']
    search_fields = ['name', 'address']


class RevisionAdmin(admin.ModelAdmin):
    list_display = ['revision']


class RemotesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'remote', 'rms', 'chain']
    search_fields = ['name', 'remote']


admin.site.register(RmsModel, RmsAdmin)
admin.site.register(ChainModel, ChainAdmin)
admin.site.register(RevisionModel, RevisionAdmin)
admin.site.register(RemotesModel, RemotesAdmin)

