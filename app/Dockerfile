FROM python:2.7.10-slim
MAINTAINER Patrick Allen <prallen90@gmail.com>

ENV PYTHONUNBUFFERED 1
ENV APPLICATION_ROOT /app/
RUN apt-get update && apt-get install -y build-essential postgresql python-dev libpq-dev --fix-missing --no-install-recommends
RUN mkdir -p $APPLICATION_ROOT
WORKDIR $APPLICATION_ROOT
ADD requirements.txt $APPLICATION_ROOT
RUN pip install -r requirements.txt
ADD . $APPLICATION_ROOT
