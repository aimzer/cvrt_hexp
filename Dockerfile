FROM python:3.8-alpine

MAINTAINER Aimen Zerroug <aimen.zerroug@gmail.com>

RUN apt-get update apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*


# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

