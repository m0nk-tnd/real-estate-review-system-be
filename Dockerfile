FROM python:3

RUN mkdir /code
WORKDIR /code
COPY . /code/ 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN python -m pip install --upgrade pip
COPY ./requirements.txt /app
RUN python -m pip install -r requirements.txt


