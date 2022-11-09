from django.shortcuts import render
from .pyrus_api import get_rms_servers, get_chain_servers
from .models import RmsModel, ChainModel
from .serializers import ChainSerializer, RmsSerializer
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView
import requests
import xml.etree.ElementTree as ET
from .froms import AskVersionForm


def get_rms(request):
    content = get_rms_servers()
    if request.method == 'POST':
        for line in content:
            RmsModel.objects.create(name=line[1], address=line[0], port=line[3], scheme=line[2])

    return render(request, 'app_pyrus/index.html', {'content': content})


def get_chain(request):
    content = get_chain_servers()
    if request.method == 'POST':
        for line in content:
            ChainModel.objects.create(address=line[0], port=line[2], scheme=line[1])

    return render(request, 'app_pyrus/index.html', {'content': content})


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
    except requests.exceptions.ConnectionError as e:
        return None


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

