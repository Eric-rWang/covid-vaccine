FROM python:3.9

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential

COPY source /app
WORKDIR /app

RUN pip3 install hotqueue
RUN pip3 install flask
RUN pip3 install redis
RUN pip3 install pytz
RUN pip3 install matplotlib
RUN pip3 install numpy
RUN pip3 install scipy

EXPOSE 5000

ENTRYPOINT ["python3"]