FROM ubuntu:latest
LABEL authors="Mryan2005"
RUN apt-get update && apt-get install -y python3.11 python3-pip firefox
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
COPY ./Firefox/geckodriver /usr/bin/geckodriver
CMD python3 main.py