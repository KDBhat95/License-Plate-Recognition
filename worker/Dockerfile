FROM ubuntu:eoan

WORKDIR /srv
COPY worker.py /srv
COPY getALPR.py /srv
COPY getGeoTag.py /srv
RUN apt-get update
RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y openalpr
RUN (cd /usr/share/openalpr/runtime_data/ocr/; cp tessdata/lus.traineddata .)

RUN apt-get install -y python3 python3-pip python3-pika python3-pillow python3-openalpr python3-redis
RUN pip3 install jsonpickle
RUN mkdir -p /images
RUN cd /srv
CMD ["python3", "worker.py"]
