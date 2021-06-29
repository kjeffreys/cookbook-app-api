FROM python:3.7-alpine
LABEL noorg.image.authors="kjeffreyscs@gmail.com"

#PYTHONUNBUFFERED is recommended docker setting
# set python to not buffer outputs, but rather print them directly
# can prevent complication when docker sets up python application
# set python unbuffered variable
# the way to set environment variable in docker is ENV key=value
ENV PYTHONUNBUFFERED 1

# copy local req.txt into docker image
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# create app dir on docker image, cd, copy local app into docker image /app dir
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# create user that can run the application inside docker
# use "user" to run app for security, b/c default user would be root
RUN adduser -D user
USER user



