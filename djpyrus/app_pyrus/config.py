import os
import sys
from dotenv import load_dotenv, find_dotenv, set_key

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

APP_PATH = os.path.dirname(sys.modules['__main__'].__file__)
LOGIN = os.getenv('LOGIN')
SECURE_KEY = os.getenv('SECURE_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
TEST = os.getenv('TEST')


def set_token(value):
    set_key(dotenv_path='.env', key_to_set='ACCESS_TOKEN', value_to_set=value)
    load_dotenv()
    global ACCESS_TOKEN
    ACCESS_TOKEN = value


def set_test(value):
    set_key(dotenv_path='.env', key_to_set='TEST', value_to_set=value)
    load_dotenv()
    global TEST
    TEST = value


