FROM python:3.9

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential

COPY source /app
WORKDIR /app

RUN pip3 install hotqueue
RUN pip3 install flask
RUN pip3 install redis
RUN pip3 install pytz

ENTRYPOINT ["python3"]