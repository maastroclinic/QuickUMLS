FROM jfloff/alpine-python:recent
MAINTAINER Sander Puts

COPY requirements.txt /opt/QuickUMLS/requirements.txt
WORKDIR /opt/QuickUMLS
RUN pip install -r requirements.txt

#install spacy model
ARG SPACYMODEL=en
ENV SPACYMODEL=$SPACYMODEL
RUN python -m spacy download $SPACYMODEL

COPY setup_simstring.sh /opt/pythonmodules/setup_simstring.sh
WORKDIR /opt/pythonmodules

RUN apk add --no-cache curl
RUN /bin/bash -c "source setup_simstring.sh 3"


COPY . / /opt/QuickUMLS/

ENV PORT=9999
ENV PYTHONPATH /opt/pythonmodules:/opt/QuickUMLS


WORKDIR /opt/QuickUMLS
CMD python /opt/QuickUMLS/app/quickumls-service.py --port=$PORT $OPTIONAL_ARGS