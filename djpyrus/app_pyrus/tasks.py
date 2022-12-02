# from celery import Celery
from djpyrus.celery import app
from celery.schedules import crontab
from .functions.load_kk_in_db import load_kk_in_db
from .functions.ask_version import ask_for_all

# app.autodiscover_tasks()

@app.task
def load():
    load_kk_in_db()

@app.task
def update_versions():
    ask_for_all()
