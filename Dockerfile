FROM ubuntu:latest
LABEL authors="Mryan2005"
RUN apt-get update && apt-get install -y python3.11 python3-pip firefox
WORKDIR /app
ADD ./SSPUBot .
RUN pip install -r requirements.txt
ADD ./Firefox/geckodriver /usr/bin/geckodriver
WORKDIR /SSPUBot
CMD python3 main.py