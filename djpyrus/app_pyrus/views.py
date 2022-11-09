from django.shortcuts import render
from .pyrus_api import get_servers

def get_dict(request):
    content = get_servers()
    return render(request, 'app_pyrus/index.html', {'content': content})
