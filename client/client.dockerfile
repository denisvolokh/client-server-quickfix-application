#FROM jfloff/alpine-python:2.7-slim

FROM frolvlad/alpine-python3

RUN apk add --update python-dev libxml2-dev gcc g++ musl-dev git py-pip bash python3-dev

#FROM noviscient/alpine-python-quickfix

VOLUME /tmp
VOLUME /application

WORKDIR /application
COPY requirements-p27.txt /application
COPY . /application

# install requirements
RUN pip3 install -r requirements-p27.txt

#EXPOSE 3333

#ENTRYPOINT python initiator_runner.py

ENTRYPOINT bash

#CMD ["true"]