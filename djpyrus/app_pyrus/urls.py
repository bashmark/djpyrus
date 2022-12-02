
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views import RmsList, ChainList, RevisionView

from django.views.static import serve as mediaserve

router = routers.DefaultRouter()



urlpatterns = [
    path('rms/', RmsList.as_view(), name='get_rms'),
    path('chain/', ChainList.as_view(), name='get_rms'),
    path('revision/', RevisionView.as_view(), name='get_rev'),
    # path('ask-for-all/', ask_for_all_view, name='ask_for_all'),
    # path('load-json/', load_json_view, name='load_json'),
    # path('get-one-task/', get_one_task_view, name='get_one_task'),

]
