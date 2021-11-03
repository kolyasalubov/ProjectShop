FROM python:3.9-alpine

RUN mkdir -p /usr/src/TelegramBot
WORKDIR /usr/src/TelegramBot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add inotify-tools

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x ./bot_devel.sh
