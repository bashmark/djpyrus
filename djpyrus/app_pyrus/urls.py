from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views import get_rms, get_chain, RmsList, ChainList, ask_version_view

router = routers.DefaultRouter()



urlpatterns = [
    path('rms/', RmsList.as_view(), name='get_rms'),
    path('chain/', ChainList.as_view(), name='get_rms'),
    path('ask/', ask_version_view, name='ask')

]
