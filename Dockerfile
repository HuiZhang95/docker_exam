FROM python:3.9-alpine 

WORKDIR /app

copy src /app/src

RUN pip install requests



