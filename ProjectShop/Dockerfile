FROM python:3.9-alpine

RUN mkdir -p /usr/src/ProjectShop
WORKDIR /usr/src/ProjectShop

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY . .

RUN python manage.py collectstatic --noinput

RUN adduser -D myuser
USER myuser
