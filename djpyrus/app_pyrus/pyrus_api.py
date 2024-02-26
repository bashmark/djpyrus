import logging
import re
from pyrus import client
import pyrus.models.requests
from .config import LOGIN, SECURE_KEY, ACCESS_TOKEN, set_token


def login() -> str:
    pyrus_client = client.PyrusAPI(login=LOGIN, security_key=SECURE_KEY)
    response = pyrus_client.auth()
    if response.success:
        new_token = response.access_token
        global ACCESS_TOKEN
        ACCESS_TOKEN = new_token
        set_token(new_token)
        return new_token
    else:
        raise ConnectionError


def get_KK() -> list[dict]:
    pyrus_client = client.PyrusAPI(access_token=ACCESS_TOKEN)
    forms_response = pyrus_client.get_forms()
    if forms_response.error_code == 'required_parameter_missing':
        logging.info(forms_response.error_code)
        new_token = login()
        pyrus_client = client.PyrusAPI(access_token=new_token)
        forms_response = pyrus_client.get_forms()
    forms = forms_response.forms
    out = []
    request = pyrus.models.requests.FormRegisterRequest(
        include_archived=True,
        steps=[1, 2],
        format='json',
        item_count=1000)

    form_register_response = pyrus_client.get_registry(forms[0].id, request)
    tasks = form_register_response.tasks
    for t in tasks:
        task_fields = one_task(t.id)
        if task_fields:
            out.append(task_fields)
    return out


def remove_resto_and_slash_add_https_for_iiko_it(url):
    if re.search(r'\xa0$', url):
        url = re.sub(r'\xa0$', '', url)
    if re.search(r'\r$', url):
        url = re.sub(r'\r$', '', url)
    if re.search(r'\\resto', url):
        url = re.sub(r'\\resto', '', url)
    if re.search(r'resto$', url):
        url = re.sub(r'resto$', '', url)
    if re.search(r'resto\/$', url):
        url = re.sub(r'resto\/$', '', url)
    if re.search(r'\/$', url):
        url = re.sub(r'\/$', '', url)
    if re.search(r':443$', url):
        url = re.sub(r':443$', '', url)
    if re.search(r'iiko\.it', url) and not re.match(r'https:', url):
        url = 'https://' + url
    if re.search(r'krd-host', url):
        if not re.match(r'http:', url):
            url = 'http://' + url
        if not re.search(r'38080$', url):
            url = url + ':38080'

    return url


def url_is_url(url):
    if (re.search(r'^http', url) and not re.search(r'192\.168', url)) \
            or re.search(r'iiko\.it', url) \
            or re.search(r'krd-host\.ru', url) \
            or (re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url) and not re.search(r'192\.168', url)) \
            or re.search(r'[A-Za-z0-9-_~]*\.[A-Za-z0-9-_~]*\.[A-Za-z]{1,5}$|[A-Za-z0-9-_~]*\.[A-Za-z]{1,5}$', url):
        return True
    else:
        return False


def rem_xa0(str_in: str) -> str:
    if re.search(r'\xa0$', str_in):
        str_in = re.sub(r'\xa0$', '', str_in)
    while re.search(r'\xa0', str_in):
        str_in = re.sub(r'\xa0', ' ', str_in)
    return str_in


def one_task(id_task) -> dict:
    """
        Form field

        Attributes:
            id (:obj:`int`): Field id
            type (:obj:`str`): Field type
            name (:obj:`str`): Field name
            info (:obj:`models.entities.FormFieldInfo`): Additional field information
            value (:obj:`object`, optional): Field value
            parent_id (:obj:`int`, optional) Parent field id (returned if field has parent)
            row_id (:obj:`int`, optional) Table row id (returned if field is in table)
    """
    pyrus_client = client.PyrusAPI(access_token=ACCESS_TOKEN)

    task = pyrus_client.get_task(id_task)
    if task.error_code == 'required_parameter_missing':
        logging.info(task.error_code)
        new_token = login()
        pyrus_client = client.PyrusAPI(access_token=new_token)
        task = pyrus_client.get_task(id_task)
    fields_d = {}
    fields_d['remotes'] = []
    # 2 - name, 6 - table of rms, 40 - rms, 42 - chain, 64 - Подключения к Точкам продаж, 17 - таблица подключений
    for field in task.task.fields:
        try:
            if field.id in [2, 6, 40, 42, 64, 17]:
                fields_d['id'] = id_task

                # start block подключения к серверам
                if field.id == 6:  # обработка таблицы подключений к rms серверам
                    if field.value:
                        l = []
                        for line in field.value:
                            d = {}
                            try:
                                for cell in line.cells:
                                    if cell.id == 7:
                                        d['name'] = rem_xa0(cell.value)
                                    if cell.id == 8:
                                        address = remove_resto_and_slash_add_https_for_iiko_it(cell.value)
                                        if url_is_url(address):
                                            d['address'] = address
                                        else:
                                            raise ValueError(f"in task_id {id_task}, in org. {fields_d['name']}, "
                                                             f"rms address '{d['address']}' is not address")

                                if not 'address' in d:
                                    raise ValueError(f'no address in row')
                                l.append(d)

                            except Exception as e:
                                logging.error(f'in task {id_task} in row {field.row_id} error: {e}')

                        if len(l):
                            fields_d['rmss'] = l
                        continue
                if field.id == 2:  # имя компании или подразделения
                    fields_d['name'] = rem_xa0(field.value)
                if field.id == 40:  # Адрес сервера rms в карточке
                    fields_d['rms_address'] = field.value
                if field.id == 42:  # Адрес сервера chain в карточке
                    fields_d['chain_address'] = field.value
                # end block подключения к серверам
                # ------------------------------------
                # start block подключения по anydesk
                if field.id == 64:  # подключения по anydesk из текстового поля
                    if field.value:
                        remotes_list = field.value.split('\n')
                        for line in remotes_list:
                            one_remotes_dict = {}
                            splitted_remotes_list = re.split(r'(\d{9}|\d{3}\ \d{3}\ \d{3})', line)[1:]

                            if not len(splitted_remotes_list) == 0:
                                one_remotes_dict['anydesk'] = splitted_remotes_list[0]
                                one_remotes_dict['name'] = rem_xa0(
                                    splitted_remotes_list[1][1:] if re.match(r'^\ ', splitted_remotes_list[1]) else
                                    splitted_remotes_list[1])
                                if 'name' not in one_remotes_dict:
                                    one_remotes_dict['name'] = 'NoName'
                                elif one_remotes_dict['name'] == '':
                                    one_remotes_dict['name'] = 'NoName'
                                if 'password' not in one_remotes_dict:
                                    one_remotes_dict['password'] = 'Tb#147852'
                                if 'anydesk' not in one_remotes_dict:
                                    one_remotes_dict['anydesk'] = '000000000'

                                fields_d['remotes'].append(one_remotes_dict)

                if field.id == 17:  # подключения по anydesk из таблицы
                    if field.value:
                        for line in field.value:
                            if line.cells:
                                d = {}
                                for cell in line.cells:
                                    # id 23 - Наименование, 20 - Anydesk, 21 - пароль Anydesk
                                    # print(f'id: {cell.id} value: {cell.value}')
                                    if cell.id == 23:
                                        d['name'] = rem_xa0(cell.value)
                                    if cell.id == 20:
                                        d['anydesk'] = cell.value
                                    if cell.id == 21:
                                        d['password'] = cell.value
                                if 'name' not in d:
                                    d['name'] = 'NoName'
                                elif d['name'] == '':
                                    d['name'] = 'NoName'
                                if 'pass' not in d:
                                    d['password'] = 'DELETED'
                                if 'anydesk' not in d:
                                    d['anydesk'] = '000000000'

                                fields_d['remotes'].append(d)

                # end block подключения по anydesk

        except Exception as e:
            logging.error(f'in task id: {id_task} unhandled error {e}')

    if fields_d['rms_address'] == fields_d['chain_address']:
        fields_d['rms_address'] = None

    if fields_d['rms_address'] and not url_is_url(fields_d['rms_address']):
        logging.info(
            f"in task_id {id_task}, in org. {fields_d['name']}, rms address '{fields_d['rms_address']}' is not address")
        fields_d['rms_address'] = None

    if fields_d['chain_address'] and not url_is_url(fields_d['chain_address']):
        logging.info(
            f"in task_id {id_task}, in org. {fields_d['name']}, chain address '{fields_d['chain_address']}' is not address")
        fields_d['chain_address'] = None

    if 'rmss' in fields_d:
        for i in fields_d['rmss']:
            if not 'name' in i:
                i['name'] = fields_d['name']

    if 'rmss' in fields_d and not fields_d['rms_address']:
        if len(fields_d['rmss']) == 1:
            fields_d['rms_address'] = fields_d['rmss'][0]['address']
            fields_d.pop('rmss')

    if not (fields_d['rms_address'] is None and fields_d['chain_address'] is None and not 'rmss' in fields_d):
        if fields_d['rms_address'] is not None:
            fields_d['rms_address'] = remove_resto_and_slash_add_https_for_iiko_it(fields_d['rms_address'])

        if fields_d['chain_address'] is not None:
            fields_d['chain_address'] = remove_resto_and_slash_add_https_for_iiko_it(fields_d['chain_address'])

        if 'rmss' in fields_d:
            if not 'address' in fields_d['rmss'][0]:
                fields_d.pop('rmss')
            else:
                if len(fields_d['rmss']) == 1 and fields_d['rmss'][0]['address'] == fields_d['rms_address']:
                    fields_d.pop('rmss')

        return fields_d
