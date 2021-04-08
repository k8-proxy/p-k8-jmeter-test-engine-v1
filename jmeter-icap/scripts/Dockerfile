FROM glasswallsolutions/cloud-qa:jmeter-ubuntu

ENV PATH $PATH:${JMETER_BIN}
ARG DATA_PATH="."
COPY  ${DATA_PATH}/Test /usr/share/Test/
COPY  ${DATA_PATH}/Test/py /usr/share/Test/
COPY  ${DATA_PATH}/requirements.txt .
COPY  ${DATA_PATH}/lib/* /usr/local/apache-jmeter-5.3/lib/
COPY  ${DATA_PATH}/ca.pem /usr/local/share/ca-certificates/

RUN chmod +x /usr/share \
    && chmod +x /usr/share/Test/launch.sh \
    && pip3 install -r requirements.txt --user \
    && update-ca-certificates

RUN apt-get update && apt-get install -y curl

ENTRYPOINT ["/usr/share/Test/launch.sh"]