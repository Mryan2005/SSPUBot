FROM ghcr.io/mryan2005/firefox-on-docker:latest
MAINTAINER Mryan2005
LABEL authors="Mryan2005"
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo '$TZ' > /etc/timezone
RUN apt-get install sudo
WORKDIR /app
ADD ./SSPUBot .
ADD ./requirements.txt .
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt
RUN useradd -m sspubot && echo "sspubot:sspubot" | chpasswd && adduser sspubot root
RUN chmod a+rwx ./ -R
CMD ./run.sh