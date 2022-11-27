import json
import os
import re

from django.shortcuts import render
from django.conf import settings
from rest_framework.permissions import IsAuthenticated

from .functions.load_kk_in_db import load_kk_in_db
from .pyrus_api import one_task, get_KK
from .models import RmsModel, ChainModel
from .serializers import ChainSerializer, RmsSerializer
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin
from rest_framework.generics import GenericAPIView
import rest_framework.permissions

from .froms import AskVersionForm, AskForAllForm, LoadJsonForm, GetOneTaskForm
from .functions.ask_version import ask_version, ask_for_all


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
            log = load_kk_in_db()

            return render(request, 'app_pyrus/load_json.html', {'form': form, 'log': log})

    else:
        form = LoadJsonForm()
    return render(request, 'app_pyrus/load_json.html', {'form': form})


def get_one_task_view(request):
    if request.method == "POST":
        form = GetOneTaskForm(request.POST)
        if form.is_valid():
            id_task = form.cleaned_data.get('task')
            task_data = one_task(id_task=id_task)
            return render(request, 'app_pyrus/get_one_task.html', {'form': form, 'data': task_data})
    else:
        form = GetOneTaskForm()
    return render(request, 'app_pyrus/get_one_task.html', {'form': form,})

