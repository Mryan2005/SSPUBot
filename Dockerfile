FROM selenium/standalone-firefox:latest
LABEL authors="Mryan2005"
WORKDIR /app
ADD ./ .
ADD ./requirements.txt .
RUN sudo apt-get update && sudo apt install libopencv-dev python3-opencv -y && sudo apt-get install -y python3-pip
RUN sudo pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN sudo pip install -r requirements.txt
RUN sudo useradd -ms /bin/bash SSPUBot
RUN sudo chown -R SSPUBot SSPUBot/
WORKDIR /app/SSPUBot
USER SSPUBot
CMD sudo python3 main.py

EXPOSE 4444