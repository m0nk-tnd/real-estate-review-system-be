FROM python:3

RUN mkdir /app
WORKDIR /app
COPY . /app 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN python -m pip install --upgrade pip
COPY ./requirements.txt /app
RUN python -m pip install -r requirements.txt


