FROM jfloff/alpine-python:2.7-slim
RUN apk add --update python-dev libxml2-dev gcc g++ musl-dev git py-pip

#FROM noviscient/alpine-python-quickfix

VOLUME /tmp
VOLUME /application

WORKDIR /application
COPY requirements-p27.txt /application
COPY . /application

# install requirements
RUN pip install -r requirements-p27.txt

EXPOSE 3333

ENTRYPOINT python acceptor_runner.py
