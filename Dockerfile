FROM ubuntu:20.04
MAINTAINER Mryan2005
LABEL authors="Mryan2005"
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo '$TZ' > /etc/timezone
RUN apt-get update && apt-get install -y python3 python3-pip wget
RUN apt install xvfb x11vnc -y
RUN wget https://download-installer.cdn.mozilla.net/pub/firefox/releases/121.0.1/linux-x86_64/zh-CN/firefox-121.0.1.tar.bz2
RUN tar xjf firefox-121.0.1.tar.bz2
RUN mv firefox /opt
RUN ln -s /opt/firefox/firefox /usr/local/bin/firefox
RUN echo 'export PATH=$PATH:/usr/bin/firefox' >> ./.bash_profile
RUN apt-get install libgtk-3-dev -y
RUN apt install libgtk2.0-0 -y
RUN apt install libasound2 -y
RUN  apt-get install firefox-locale-zh-hans -y
RUN firefox --version
WORKDIR /app
ADD ./SSPUBot .
ADD ./requirements.txt .
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt
RUN useradd -m sspubot && echo "sspubot:sspubot" | chpasswd && adduser sspubot sudo
RUN chmod a+rwx ./ -R
USER sspubot
CMD python3 main.py