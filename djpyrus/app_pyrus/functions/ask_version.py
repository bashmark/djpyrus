import requests
import xml.etree.ElementTree as ET

from ..models import RmsModel, ChainModel


def ask_version(scheme, address, port):
    try:
        url = f'{scheme}://{address}:{port}/resto/get_server_info.jsp?encoding=UTF-8'
        content = requests.get(url).content
        tree = ET.fromstring(content)
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
    for item in queryset:
        version = ask_version(item.scheme, item.address, item.port)
        version_in_base = RmsModel.objects.get(id=item.id).version
        if version != version_in_base:
            RmsModel.objects.filter(id=item.id).update(version=version)
            print(f'{item.address}: version updated {version_in_base} -> {version}')

    """
    Chain
    """
    queryset = ChainModel.objects.all()
    for item in queryset:
        version = ask_version(item.scheme, item.address, item.port)
        version_in_base = ChainModel.objects.get(id=item.id).version
        if version != version_in_base:
            ChainModel.objects.filter(id=item.id).update(version=version)
            print(f'{item.address}: version updated {version_in_base} -> {version}')

