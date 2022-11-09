from django.contrib import admin
from .models import RmsModel, ChainModel

class RmsAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'chain']


class ChainAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']


admin.site.register(RmsModel, RmsAdmin)
admin.site.register(ChainModel, ChainAdmin)
