FROM python:2.7.10-slim
MAINTAINER Patrick Allen <prallen90@gmail.com>

RUN apt-get update && apt-get install -qq -y build-essential --fix-missing --no-install-recommends

ENV INSTALL_PATH /markdraft
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

VOLUME ["$INSTALL_PATH/build/public"]

CMD python app.py
