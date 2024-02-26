from django.urls import path
from rest_framework import routers
from .api import UserViewSet, RmsList, ChainList, RevisionList, RemoteList

router = routers.DefaultRouter()

router.register(r'usermodel', UserViewSet)

urlpatterns = [
    path('rms/', RmsList.as_view(), name='get_rms'),
    path('chain/', ChainList.as_view(), name='get_chain'),
    path('revision/', RevisionList.as_view(), name='get_rev'),
    path('remote/', RemoteList.as_view(), name='get_rem'),
    # path('', include(router.urls)),
    # path('ask-for-all/', ask_for_all_view, name='ask_for_all'),
    # path('load-json/', load_json_view, name='load_json'),
    # path('get-one-task/', get_one_task_view, name='get_one_task'),

]
