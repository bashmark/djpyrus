# from celery import Celery
from .service import send
from djpyrus.celery import app
from celery.schedules import crontab
from .functions.load_kk_in_db import load_kk_in_db


# app.autodiscover_tasks()


@app.task
def load():
    load_kk_in_db()

@app.task
def send_spam_email(user_email):
    print(user_email)
    send(user_email)

