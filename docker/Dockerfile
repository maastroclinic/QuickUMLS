FROM jfloff/alpine-python:recent
MAINTAINER Sander Puts

#clone and install QuickUMLS from github
WORKDIR /opt
#RUN git clone https://github.com/Georgetown-IR-Lab/QuickUMLS.git
RUN git clone -b feature/docker-multilanguage https://github.com/maastroclinic/QuickUMLS

WORKDIR /opt/QuickUMLS
RUN pip install -r  requirements.txt

RUN mkdir /opt/pythonmodules
WORKDIR /opt/pythonmodules
ENV PYTHONPATH /opt/pythonmodules:/opt/QuickUMLS

RUN cp /opt/QuickUMLS/setup_simstring.sh /opt/pythonmodules/setup_simstring.sh
RUN apk add --no-cache curl
RUN /bin/bash -c "source setup_simstring.sh 3"


#install spacy model
ARG SPACYMODEL=en
ENV SPACYMODEL=$SPACYMODEL
RUN python -m spacy download $SPACYMODEL

WORKDIR /opt/QuickUMLS
CMD python /opt/QuickUMLS/app/quickumls-service.py --port=9999 --debug