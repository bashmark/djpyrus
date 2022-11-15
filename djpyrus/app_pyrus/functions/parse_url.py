import re


def parse_url(url: str) -> dict:
    if re.match(r'https:', url):
        scheme = 'https'
    else:
        scheme = 'http'
    if re.search(r'\:\d{4,5}', url):
        port = re.search(r'\:\d{4,5}', url).group(0)[1:]
    else:
        port = 443
    address = re.sub(r'^https:\/\/|^http:\/\/', '', url)
    address = re.sub(r'\:\d{4,5}', '', address)

    return {'scheme': scheme, 'address': address, 'port': port}