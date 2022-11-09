from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import get_dict

urlpatterns = [
    path('', get_dict, name='get_dict')
]
