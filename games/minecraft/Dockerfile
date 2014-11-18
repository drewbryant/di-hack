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

EXPOSE 25565
EXPOSE 9090

RUN echo "foo" > index.html

VOLUME ["/minecraft"]
CMD ["-Xmx1024M", "-Xms1024M"]
ENTRYPOINT ["java", "-jar", "minecraft_server.jar", "nogui"]

