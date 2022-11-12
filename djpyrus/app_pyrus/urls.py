from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views import import_rms, RmsList, ChainList, ask_version_view, ask_for_all_view, import_chain, load_json_view

router = routers.DefaultRouter()



urlpatterns = [
    path('import_rms/', import_rms, name='import_rms'),
    path('import_chain/', import_chain, name='import_chain'),
    path('rms/', RmsList.as_view(), name='get_rms'),
    path('chain/', ChainList.as_view(), name='get_rms'),
    path('ask/', ask_version_view, name='ask'),
    path('ask-for-all/', ask_for_all_view, name='ask_for_all'),
    path('load-json/', load_json_view, name='load_json'),

]
