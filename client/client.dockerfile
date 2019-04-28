FROM jfloff/alpine-python:2.7-slim

RUN apk add --update python-dev libxml2-dev gcc g++ musl-dev git py-pip

VOLUME /tmp
VOLUME /application

WORKDIR /application
COPY requirements-p27.txt /application
COPY FIX50SP2.xml /application
COPY FIXT11.xml /application
COPY client /application

# install requirements
RUN pip install -r requirements-p27.txt

ENTRYPOINT python client/initiator_app.py