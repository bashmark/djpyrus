from .parse_url import parse_url
from .ask_version import ask_version
from ..models import ChainModel, RmsModel
from ..pyrus_api import get_KK


def load_kk_in_db():
    log = ''
    data = get_KK()
    for item in data:
        if item['chain_address']:
            data = parse_url(item['chain_address'])
            if not ChainModel.objects.filter(address=data['address']):
                print(f"chain {data['address']} not in db")
                log += f"chain {data['address']} not in db\n"
                ChainModel.objects.create(name=item['name'], address=data['address'], login='admin', password='',
                                          port=data['port'], scheme=data['scheme'],
                                          version=ask_version(scheme=data['scheme'], address=data['address'],
                                                              port=data['port']))
        if item['rms_address']:
            data = parse_url(item['rms_address'])
            if not RmsModel.objects.filter(address=data['address']):
                print(f"rms {data['address']} not in db")
                log += f"rms {data['address']} not in db\n"
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
                    print(f"rms {data['address']} not in db")
                    log += f"rms {data['address']} not in db\n"
                    RmsModel.objects.create(name=rms['name'], address=data['address'], login='admin', password='',
                                            port=data['port'], scheme=data['scheme'],
                                            version=ask_version(scheme=data['scheme'], address=data['address'],
                                                                port=data['port']),
                                            chain=ChainModel.objects.get(address=parse_url(item['chain_address'])['address'])
                                            if item['chain_address'] else None)
    return log