FROM python:3.9

RUN mkdir -p flask-server
COPY flask-server/requirements.txt /flask-server
RUN pip install -r /flask-server/requirements.txt
COPY flask-server/server.py /flask-server
RUN mkdir -p /flask-server/uploads

RUN mkdir -p react-client

COPY react-client/build /react-client/build/

WORKDIR /flask-server
CMD ["python3", "server.py"]
