from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer

from rest_framework.permissions import IsAuthenticated

from .models import RmsModel, ChainModel, RevisionModel, RemotesModel
from .serializers import ChainSerializer, RmsSerializer, RevisionSerializer, RemoteSerializer
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin
from rest_framework.generics import GenericAPIView


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RmsList(ListModelMixin, GenericAPIView):
    serializer_class = RmsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = RmsModel.objects.all()
        return queryset

    def get(self, request):
        return self.list(request)


class RevisionList(ListModelMixin, GenericAPIView):
    serializer_class = RevisionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = RevisionModel.objects.all()
        return queryset

    def get(self, request):
        return self.list(request)


class ChainList(ListModelMixin, GenericAPIView):
    serializer_class = ChainSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = ChainModel.objects.all()
        return queryset

    def get(self, request):
        return self.list(request)


class RemoteList(ListModelMixin, GenericAPIView):
    serializer_class = RemoteSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = RemotesModel.objects.all()
        return queryset

    def get(self, request):
        return self.list(request)
