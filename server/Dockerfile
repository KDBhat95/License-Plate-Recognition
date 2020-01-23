FROM ubuntu

RUN mkdir -p /Lab8
WORKDIR /Lab8
ADD . /Lab8
RUN chmod 777 startup_script.sh
RUN chmod 777 server.py
CMD ["/Lab8/startup_script.sh"]
EXPOSE 5000

