# syntax=docker/dockerfile:1
FROM python:3.10.1

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get upgrade -y
RUN apt-get install netcat -y
RUN apt-get install postgresql gcc python3-dev musl-dev -y
RUN apt-get install gettext -y

RUN pip install --upgrade pip

WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./
