FROM python:3.8-slim-buster

WORKDIR /usr/worker

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt && mkdir data models

COPY .env tasks.py ./
