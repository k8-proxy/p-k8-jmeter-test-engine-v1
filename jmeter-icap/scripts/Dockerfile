FROM glasswallsolutions/cloud-qa:jmeter-ubuntu

ENV PATH $PATH:${JMETER_BIN}
ARG DATA_PATH="."
COPY  ${DATA_PATH}/Test /usr/share/Test/
COPY  ${DATA_PATH}/Test/py /usr/share/Test/
COPY  ${DATA_PATH}/requirement.txt .
COPY  ${DATA_PATH}/lib/* /usr/local/apache-jmeter-5.3/lib/

RUN chmod +x /usr/share \
    && chmod +x /usr/share/Test/launch.sh \
    && pip3 install -r requirement.txt --user

ENTRYPOINT ["/usr/share/Test/launch.sh"]