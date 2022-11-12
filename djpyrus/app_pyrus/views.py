import json
import os

from django.shortcuts import render
from django.conf import settings

from .pyrus_api import get_rms_servers, get_chain_servers
from .models import RmsModel, ChainModel
from .serializers import ChainSerializer, RmsSerializer
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView
import requests
import xml.etree.ElementTree as ET
from .froms import AskVersionForm, AskForAllForm, LoadJsonForm
import time


def import_rms(request):
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
                content.append([f"Server name: {line[1]}, address: {line[0]}, version: {version if version else error} imported."])

    return render(request, 'app_pyrus/import_rms.html', {'content': content})


def import_chain(request):
    lines = get_chain_servers()
    content = []
    if request.method == 'POST':
        for line in lines:
            if ChainModel.objects.filter(address=line[0]):
                pass
            else:
                version = ask_version(scheme=line[1], address=line[0], port=line[2])
                ChainModel.objects.create(address=line[0], port=line[2], scheme=line[1], login='admin', password='resto#tb', version=version)
                error = 'not available'
                content.append([f"Server address: {line[0]}, version: {version if version else error} imported."])

    return render(request, 'app_pyrus/import_chain.html', {'content': content})


class RmsList(ListModelMixin, CreateModelMixin, GenericAPIView):
    serializer_class = RmsSerializer

    def get_queryset(self):
        queryset = RmsModel.objects.all()

        # rms_name = self.queryset.query_params.get('name')
        # rms_address = self.queryset.query_params.get('address')
        # rms_port = self.queryset.query_params.get('port')
        # rms_scheme = self.queryset.query_params.get('scheme')
        # rms_version = self.queryset.query_params.get('version')
        # rms_chain = self.queryset.query_params.get('chain')

        # if rms_name:
        #     queryset = queryset.filter(name=rms_name)
        #
        # if rms_chain:
        #     chain_id = ChainModel.objects.get(chain_name=rms_chain)
        #     queryset = queryset.filter(chain=chain_id)

        return queryset

    def get(self, request):
        return self.list(request)


class ChainList(ListModelMixin, CreateModelMixin, GenericAPIView):
    serializer_class = ChainSerializer

    def get_queryset(self):
        queryset = ChainModel.objects.all()
        return queryset

    def get(self, request):
        return self.list(request)

def ask_version(scheme, address, port):

    try:
        url = f'{scheme}://{address}:{port}/resto/get_server_info.jsp?encoding=UTF-8'
        content = requests.get(url).content
        tree = ET.fromstring(content)
        server_name = tree.find("serverName").text
        version = tree.find("version").text[:-2]
        return version
    except Exception as e:
        print(e)
        return None

def ask_for_all():
    """
    RMS
    :return:
    """
    queryset = RmsModel.objects.all()
    content = []
    for item in queryset:
        #time.sleep(1)
        # print(f'{item.scheme}://{item.address}:{item.port}/resto')
        version = ask_version(item.scheme, item.address, item.port)
        version_in_base = RmsModel.objects.get(id=item.id).version
        if version != version_in_base:
            t = RmsModel.objects.filter(id=item.id).update(version=version)
            print(f'{item.address}: {t}')
            content.append([item.address, t])

    """
    Chain
    """
    queryset = ChainModel.objects.all()
    for item in queryset:
        # time.sleep(1)
        # print(f'{item.scheme}://{item.address}:{item.port}/resto')
        version = ask_version(item.scheme, item.address, item.port)
        version_in_base = ChainModel.objects.get(id=item.id).version
        if version != version_in_base:
            t = ChainModel.objects.filter(id=item.id).update(version=version)
            print(f'{item.address}: {t}')
            content.append([item.address, t])
    return content


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
            print(path)
            with open(path, 'r') as file:
                data = json.load(file)
                for item in data:
                    name = item['name']
                    rms_address = item['rms_address']
                    chain_address = item['chain_address']
                    rmss = item['rmss'] if 'rmss' in item else None
                    print(rms_address)



            return render(request, 'app_pyrus/load_json.html', {'form': form, 'data': data})

    else:
        form = LoadJsonForm()
    return render(request, 'app_pyrus/load_json.html', {'form': form})