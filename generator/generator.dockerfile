FROM frolvlad/alpine-python3

RUN apk add --update python-dev py-pip bash python3-dev

VOLUME /tmp
VOLUME /application

WORKDIR /application
COPY requirements.txt /application
COPY . /application

RUN pip install --upgrade pip

# install requirements
RUN pip3 install -r requirements.txt

ENTRYPOINT python3 main.py