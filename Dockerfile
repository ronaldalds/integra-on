FROM python:3.12-alpine

USER root

ENV TZ=America/Fortaleza


WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD gunicorn core.wsgi:application --bind 0.0.0.0:5000