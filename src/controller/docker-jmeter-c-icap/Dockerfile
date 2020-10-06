FROM openjdk:8-jre

# Install c-icap
RUN apt-get update && \
    apt-get -y install c-icap

RUN apt install -y python3
RUN apt install -y python3-pip

# Set variables
ARG JMETER_VERSION="5.3"
ENV JMETER_HOME /usr/local/apache-jmeter-${JMETER_VERSION}
ENV JMETER_BIN ${JMETER_HOME}/bin

# install Minio client
RUN curl --location --silent --show-error --output /usr/bin/mc https://dl.min.io/client/mc/release/linux-amd64/mc
RUN chmod +x /usr/bin/mc

# Install Apache JMeter
RUN wget http://archive.apache.org/dist/jmeter/binaries/apache-jmeter-${JMETER_VERSION}.tgz && \
    tar zxvf apache-jmeter-${JMETER_VERSION}.tgz && \
    rm -f apache-jmeter-${JMETER_VERSION}.tgz && \
    mv apache-jmeter-${JMETER_VERSION} ${JMETER_HOME}

EXPOSE 1344

ENV PATH $PATH:${JMETER_BIN}
COPY ./Test /usr/share/Test/
COPY ./jmeter-conf.jmx /etc/conf/

RUN chmod +x /usr/share
#ENTRYPOINT ["/usr/share/Test/launch.sh"]

COPY requirement.txt .

RUN pip3 install -r requirement.txt --user

COPY processor.py .

COPY logging.conf .

CMD ["python3", "processor.py"]
