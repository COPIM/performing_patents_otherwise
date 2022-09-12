# syntax=docker/dockerfile:1
FROM python:3.10.7-slim-buster

RUN apt-get update -y && apt-get install -y imagemagick

WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "-m", "flask", "run"]
