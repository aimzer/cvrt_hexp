# taken from https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/


FROM python:3.9.5-slim-buster as builder

MAINTAINER Aimen Zerroug <aimen.zerroug@gmail.com>


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

    # gcc \

RUN git clone https://github.com/aimzer/cvrt_hexp.git


# install the dependencies and packages in the requirements file
RUN pip install --upgrade pip
RUN pip install -r cvrt_hexp/services/web/requirements.txt



# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app



# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
# WORKDIR $APP_HOME

RUN cp -r cvrt_hexp/services/web/* $APP_HOME

WORKDIR $APP_HOME


# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app
