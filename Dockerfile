# taken from https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/


FROM python:3.9.5-slim-buster as builder

MAINTAINER Aimen Zerroug <aimen.zerroug@gmail.com>


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

    # gcc \

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
# RUN mkdir $APP_HOME

WORKDIR $HOME

RUN git clone https://github.com/aimzer/cvrt_hexp.git



RUN cp -r cvrt_hexp/services/* $HOME

# install the dependencies and packages in the requirements file
RUN pip install --upgrade pip
RUN pip install -r cvrt_hexp/requirements.txt

WORKDIR $APP_HOME
