import logging

from .parse_url import parse_url
from .ask_version import ask_version
from ..models import ChainModel, RmsModel, RemotesModel
from ..pyrus_api import get_KK


def load_kk_in_db():

    data = get_KK()
    for item in data:
        if item['chain_address']:
            data = parse_url(item['chain_address'])  # {'scheme': scheme, 'address': address, 'port': port}
            if not ChainModel.objects.filter(address=data['address']):
                logging.debug(f"chain {data['address']} not in db")
                ChainModel.objects.create(name=item['name'], address=data['address'], login='admin', password='',
                                          port=data['port'], scheme=data['scheme'],
                                          version=ask_version(scheme=data['scheme'], address=data['address'],
                                                              port=data['port']))
        if item['rms_address']:
            data = parse_url(item['rms_address'])  # {'scheme': scheme, 'address': address, 'port': port}
            if not RmsModel.objects.filter(address=data['address']):
                logging.debug(f"rms {data['address']} not in db")
                RmsModel.objects.create(name=item['name'], address=data['address'], login='admin', password='',
                                        port=data['port'], scheme=data['scheme'],
                                        version=ask_version(scheme=data['scheme'], address=data['address'],
                                                            port=data['port']),
                                        chain=ChainModel.objects.get(address=parse_url(item['chain_address'])['address'])
                                        if item['chain_address'] else None)

        if 'rmss' in item:
            for rms in item['rmss']:
                data = parse_url(rms['address'])
                if not RmsModel.objects.filter(address=data['address']):
                    logging.debug(f"rms {data['address']} not in db")
                    RmsModel.objects.create(name=rms['name'], address=data['address'], login='admin', password='',
                                            port=data['port'], scheme=data['scheme'],
                                            version=ask_version(scheme=data['scheme'], address=data['address'],
                                                                port=data['port']),
                                            chain=ChainModel.objects.get(address=parse_url(item['chain_address'])['address'])
                                            if item['chain_address'] else None)
        if 'remotes' in item:
            for remote in item['remotes']:
                logging.debug(f"remote {remote['anydesk']} not in db")
                rms = RmsModel.objects.get(address=parse_url(item['rms_address'])['address']) if item['rms_address'] else None
                chain = ChainModel.objects.get(address=parse_url(item['chain_address'])['address']) if item['chain_address'] else None
                RemotesModel.objects.create(name=remote['name'],
                                            remote=remote['anydesk'],
                                            password=remote['password'],
                                            rms=rms if rms else None,
                                            chain=chain if chain else None)
