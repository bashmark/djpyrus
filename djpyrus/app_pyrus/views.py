from django.shortcuts import render
from .functions.load_kk_in_db import load_kk_in_db
from .pyrus_api import one_task, get_KK
from .froms import AskVersionForm, AskForAllForm, LoadJsonForm, GetOneTaskForm
from .functions.ask_version import ask_version, ask_for_all


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
            log = load_kk_in_db()

            return render(request, 'app_pyrus/load_json.html', {'form': form, 'log': log})

    else:
        form = LoadJsonForm()
    return render(request, 'app_pyrus/load_json.html', {'form': form})


def get_one_task_view(request):
    if request.method == "POST":
        form = GetOneTaskForm(request.POST)
        if form.is_valid():
            id_task = form.cleaned_data.get('task')
            task_data = one_task(id_task=id_task)
            return render(request, 'app_pyrus/get_one_task.html', {'form': form, 'data': task_data})
    else:
        form = GetOneTaskForm()
    return render(request, 'app_pyrus/get_one_task.html', {'form': form,})

