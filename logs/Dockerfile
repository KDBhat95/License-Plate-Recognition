FROM ubuntu

RUN mkdir -p /Lab8
WORKDIR /Lab8
ADD . /Lab8
RUN apt-get update
RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y python3 python3-pip python3-pillow python3-openalpr python3-redis
RUN pip3 install pika
RUN pip3 install jsonpickle
CMD ["python3","logs_file.py"]