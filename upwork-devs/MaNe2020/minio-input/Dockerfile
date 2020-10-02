FROM openjdk:8-jre

# Install c-icap
RUN apt-get update && \
    apt-get -y install c-icap 

# Install python and pip
RUN apt install -y python3
RUN apt install -y python3-pip

# install Minio client
#RUN curl --location --silent --show-error --output /usr/bin/mc https://dl.min.io/client/mc/release/linux-amd64/mc
#RUN chmod +x /usr/bin/mc

# Set variables
ARG JMETER_VERSION="5.3"
ENV JMETER_HOME /usr/local/apache-jmeter-${JMETER_VERSION}
ENV JMETER_BIN ${JMETER_HOME}/bin

# Install Apache JMeter
RUN wget http://archive.apache.org/dist/jmeter/binaries/apache-jmeter-${JMETER_VERSION}.tgz && \
    tar zxvf apache-jmeter-${JMETER_VERSION}.tgz && \
    rm -f apache-jmeter-${JMETER_VERSION}.tgz && \
    mv apache-jmeter-${JMETER_VERSION} ${JMETER_HOME}

#Install JMeter Plugins Manager - concurrency theread group and backend listener
RUN cd ${JMETER_HOME}/lib/ext && \
    wget -cO - http://search.maven.org/remotecontent?filepath=kg/apc/jmeter-plugins-manager/1.3/jmeter-plugins-manager-1.3.jar > jmeter-plugins-manager-1.3.jar && \
    cd ${JMETER_HOME}/lib && \
    wget -cO - http://search.maven.org/remotecontent?filepath=kg/apc/cmdrunner/2.2/cmdrunner-2.2.jar > cmdrunner-2.2.jar && \
    java -cp ./ext/jmeter-plugins-manager-1.3.jar org.jmeterplugins.repository.PluginManagerCMDInstaller && \
    cd ${JMETER_BIN} && \
    ./PluginsManagerCMD.sh install jmeter.backendlistener.elasticsearch=2.7.0 && \
    ./PluginsManagerCMD.sh install jpgc-casutg=2.5
    
#In case you want to install all JMeter plugins:
# RUN cd ${JMETER_BIN} && \
#    PluginsManagerCMD.sh install-all-except jpgc-casutg


COPY requirement.txt .
RUN pip3 install -r requirement.txt --user

ENV PATH $PATH:${JMETER_BIN}
COPY ./Test /usr/share/Test/

EXPOSE 1344
#EXPOSE 9000

RUN chmod +x /usr/share
ENTRYPOINT ["/usr/share/Test/launch.sh"]
# CMD ["python3", "processor.py"]




