FROM python:3.9

WORKDIR /wd

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt