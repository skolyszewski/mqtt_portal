FROM python:3.8-slim-buster

RUN pip install pipenv
COPY mqtt-device/Pipfile* /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /mqtt-device/app
COPY mqtt-device/ .

ENTRYPOINT python device.py
