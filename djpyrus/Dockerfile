FROM python:3.10.1-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/djpyrus

COPY ./requirements.txt /usr/src/requirements.txt

COPY . /usr/src/djpyrus

RUN pip install -r /usr/src/requirements.txt

RUN pip install -U "celery[redis]"

# ENTRYPOINT ["sh", "/entrypoint.sh"]

# EXPOSE 8000

#CMD ["python", "manage.py", "makemigrations"]
#
#CMD ["python", "manage.py", "migrate"]
#
#CMD ["python", "manage.py", "init"]
#
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]