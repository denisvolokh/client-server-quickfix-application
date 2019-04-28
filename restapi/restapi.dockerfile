FROM jfloff/alpine-python:2.7-slim

RUN apk add --update python-dev libxml2-dev gcc g++ musl-dev git py-pip

VOLUME /tmp
VOLUME /application

WORKDIR /application
COPY requirements-p27.txt /application
COPY . /application

EXPOSE 5555

# install requirements
RUN pip install -r requirements-p27.txt

ENTRYPOINT python main.py