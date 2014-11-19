FROM debian:wheezy

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y openjdk-7-jre-headless openjdk-7-jre-lib

EXPOSE 25565

RUN mkdir /minecraft
WORKDIR /minecraft

RUN apt-get install -y curl
RUN curl -o minecraft_server.jar https://s3.amazonaws.com/Minecraft.Download/versions/1.8/minecraft_server.1.8.jar
ADD ./data/eula.txt /minecraft/eula.txt

RUN apt-get install -y wget sudo procps vim python python-pip inotify-tools
EXPOSE 25565


RUN pip install requests==1.1.0
RUN pip install python-firebase

ADD server.py /minecraft/server.py

VOLUME ["/minecraft"]
RUN mkdir logs
# background server so we can attach to machine and do more stuff
CMD nohup python server.py
#ENTRYPOINT ["python", "server.py"]


