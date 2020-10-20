FROM openjdk:8-jre

# Install c-icap
RUN apt-get update && \
    apt-get -y install c-icap

# Set variables
ARG JMETER_VERSION="5.3"
ENV JMETER_HOME /usr/local/apache-jmeter-${JMETER_VERSION}
ENV JMETER_BIN ${JMETER_HOME}/bin

# Install Apache JMeter
RUN wget http://archive.apache.org/dist/jmeter/binaries/apache-jmeter-${JMETER_VERSION}.tgz && \
    tar zxvf apache-jmeter-${JMETER_VERSION}.tgz && \
    rm -f apache-jmeter-${JMETER_VERSION}.tgz && \
    mv apache-jmeter-${JMETER_VERSION} ${JMETER_HOME}

EXPOSE 1344

ENV PATH $PATH:${JMETER_BIN}
RUN mkdir -p /usr/share/config
COPY ./Test /usr/share/Test/

RUN chmod +x /usr/share
RUN chmod +x /usr/share/Test/launch.sh

ENTRYPOINT ["/usr/share/Test/launch.sh"]
