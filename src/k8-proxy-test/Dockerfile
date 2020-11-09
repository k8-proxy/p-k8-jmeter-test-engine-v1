# Use a centos base image
FROM glasswallsolutions/k8-centos7:latest

# Install packages
RUN yum -y upgrade
RUN yum -y install wget
RUN yum -y install java-1.8.0-openjdk
RUN java -version
# Set variables

ENV JMETER_VERSION=5.2.1 \
    JMETER_HOME=/usr/local/apache-jmeter-${JMETER_VERSION}\
    JMETER_BIN=${JMETER_HOME}/bin \
    TEST_SCRIPT_FILE=/usr/share/jmx/Proxy_Test.jmx \
    # CERT_FILE=/Test \
    # TEST_LOG_FILE=/Test/jmeter.log \
    # TEST_RESULTS_PATH=/Test/Results/result.jtl \
    URL_SOURCE=/Test/
# Install Apache JMeter
RUN wget http://archive.apache.org/dist/jmeter/binaries/apache-jmeter-${JMETER_VERSION}.tgz && \
    tar zxvf apache-jmeter-${JMETER_VERSION}.tgz && \
    rm -f apache-jmeter-${JMETER_VERSION}.tgz && \
    mv apache-jmeter-${JMETER_VERSION} ${JMETER_HOME}

# EXPOSE 1344
# ENV PATH $PATH:${JMETER_BIN}
ENV HEAP="-Xms1g -Xmx1g -XX:MaxMetaspaceSize=256m"
COPY ./Test /usr/share/Test/
COPY Proxy_Test.jmx ${TEST_SCRIPT_FILE}
COPY allurls.csv ${URL_SOURCE}

RUN chmod -R 0777 /Test/allurls.csv
RUN chmod +x ${TEST_SCRIPT_FILE}
RUN chmod +x /usr/share/Test/launch.sh

# Copy Cert
# COPY assets-publishing-service-gov-uk.crt ${CERT_FILE}
# # Enabling the system shared CA store
# RUN update-ca-trust enable
# RUN mv ${CERT_FILE}/assets-publishing-service-gov-uk.crt /etc/pki/ca-trust/source/anchors/assets-publishing-service-gov-uk.crt
# RUN update-ca-trust extract
ENTRYPOINT ["/usr/share/Test/launch.sh"]

