FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

CMD ["gunicorn", "ecommerce.wsgi:application", "--bind", "0.0.0.0:8969", "--worker-class", "gunicorn.workers.sync.SyncWorker"]

