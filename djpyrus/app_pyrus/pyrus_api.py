import os
import re
from pprint import pprint
from pyrus import client
from .config import LOGIN, SECURE_KEY, ACCESS_TOKEN, TEST, set_test, set_token
import functools
import operator
from pandas.core.common import flatten


def login():
    pyrus_client = client.PyrusAPI(login=LOGIN, security_key=SECURE_KEY)
    response = pyrus_client.auth()
    if response.success:
        new_token = response.access_token
        print("new token: " + new_token)
        set_token(new_token)
        return new_token
    else:
        raise ConnectionError


def get_rms_servers(token=ACCESS_TOKEN):
    pyrus_client = client.PyrusAPI(access_token=token)
    server_and_names = {}
    catalog_id = 155787
    catalog_response = pyrus_client.get_catalog(catalog_id)

    if catalog_response.error_code == 'required_parameter_missing':
        return get_rms_servers(login())

    items = catalog_response.items
    for i in items:
        # print("item_id: {}, values{}, headers{}, item_ids{} rows: {}"
        #       .format(i.item_id, i.values, i.headers, i.item_ids, i.rows,))

        if re.match(r'http', i.values[1]):
            scheme = re.match(r'https|http', i.values[1]).group(0)
            address = re.sub(r':.+|\/.+', '', re.sub(r'(https|http):\/\/', '', i.values[1]))
            port = re.search(r':\d+', i.values[1]).group(0)[1:] if re.search(r':\d+', i.values[1]) else "443"
            name = i.values[0]
            if address not in server_and_names:
                line = [name, scheme, port]
                server_and_names[address] = line
    server_and_names_list = []
    for item in server_and_names:
        line = list(flatten([item, server_and_names[item]]))
        server_and_names_list.append(line)
    return server_and_names_list

def get_chain_servers(token=ACCESS_TOKEN):
    pyrus_client = client.PyrusAPI(access_token=token)
    catalog_id = 156294
    catalog_response = pyrus_client.get_catalog(catalog_id)
    out = []

    if catalog_response.error_code == 'required_parameter_missing':
        return get_rms_servers(login())

    items = catalog_response.items
    for i in items:
        # print("item_id: {}, values{}, headers{}, item_ids{} rows: {}"
        #       .format(i.item_id, i.values, i.headers, i.item_ids, i.rows,))

        if re.match(r'http', i.values[0]):
            scheme = re.match(r'https|http', i.values[0]).group(0)
            address = re.sub(r':.+|\/.+', '', re.sub(r'(https|http):\/\/', '', i.values[0]))
            port = re.search(r':\d+', i.values[1]).group(0)[1:] if re.search(r':\d+', i.values[0]) else "443"
            line = [address, scheme, port]
            out.append(line)
            print(out)
    return out
