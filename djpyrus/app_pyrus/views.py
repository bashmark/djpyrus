import json
import os
import re

from django.shortcuts import render
from django.conf import settings
from rest_framework.permissions import IsAuthenticated

from .functions.load_dict_item_in_db import load_dict_item_in_db
from .pyrus_api import get_rms_servers, get_chain_servers
from .models import RmsModel, ChainModel
from .serializers import ChainSerializer, RmsSerializer
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin
from rest_framework.generics import GenericAPIView
import rest_framework.permissions

from .froms import AskVersionForm, AskForAllForm, LoadJsonForm
from .functions.ask_version import ask_version, ask_for_all


def import_rms(request):
    """
    устаревший функционал. импорт из справочников
    :param request:
    :return:
    """
    content = []
    lines = get_rms_servers()
    if request.method == 'POST':
        for line in lines:
            if RmsModel.objects.filter(address=line[0]):
                pass
                # print(f"Server {line[0]} already imported.")
            else:
                version = ask_version(scheme=line[2], address=line[0], port=line[3])

                RmsModel.objects.create(name=line[1], address=line[0], port=line[3], scheme=line[2], login="admin",
                                        password="resto#tb", version=version)
                error = 'not available'
                content.append(
                    [f"Server name: {line[1]}, address: {line[0]}, version: {version if version else error} imported."])

    return render(request, 'app_pyrus/import_rms.html', {'content': content})


def import_chain(request):
    """
    устаревший функционал. импорт из справочников
    :param request:
    :return:
    """
    lines = get_chain_servers()
    content = []
    if request.method == 'POST':
        for line in lines:
            if ChainModel.objects.filter(address=line[0]):
                pass
            else:
                version = ask_version(scheme=line[1], address=line[0], port=line[2])
                ChainModel.objects.create(address=line[0], port=line[2], scheme=line[1], login='admin',
                                          password='resto#tb', version=version)
                error = 'not available'
                content.append([f"Server address: {line[0]}, version: {version if version else error} imported."])

    return render(request, 'app_pyrus/import_chain.html', {'content': content})


class RmsList(ListModelMixin, CreateModelMixin, GenericAPIView):
    serializer_class = RmsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = RmsModel.objects.all()
        return queryset

    def get(self, request):
        return self.list(request)


class ChainList(ListModelMixin, CreateModelMixin, GenericAPIView):
    serializer_class = ChainSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = ChainModel.objects.all()
        return queryset

    def get(self, request):
        return self.list(request)


def ask_version_view(request):
    if request.method == 'POST':
        form = AskVersionForm(request.POST)
        if form.is_valid():
            scheme = form.cleaned_data.get('scheme')
            address = form.cleaned_data.get('address')
            port = str(form.cleaned_data.get('port'))
            content = ask_version(scheme, address, port)
            return render(request, 'app_pyrus/ask_version.html', {'form': form, 'content': content})
    else:

        form = AskVersionForm()
    return render(request, 'app_pyrus/ask_version.html', {'form': form})


def ask_for_all_view(request):
    if request.method == "POST":
        form = AskForAllForm(request.POST)
        if form.is_valid():
            content = ask_for_all()
            return render(request, 'app_pyrus/ask-for-all.html', {'form': form, 'content': content})
    else:
        form = AskForAllForm()
    return render(request, 'app_pyrus/ask-for-all.html', {'form': form})


def load_json_view(request):
    if request.method == "POST":
        form = LoadJsonForm(request.POST)
        if form.is_valid():
            path = os.path.join(os.path.abspath(settings.MEDIA_ROOT), 'out.json')
            with open(path, 'r') as file:
                data = json.load(file)
                for item in data:
                    load_dict_item_in_db(item)

            return render(request, 'app_pyrus/load_json.html', {'form': form, 'data': data})

    else:
        form = LoadJsonForm()
    return render(request, 'app_pyrus/load_json.html', {'form': form})
