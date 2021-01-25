FROM glasswallsolutions/k8-centos7

RUN yum install python3 wget -y \
	&& yum clean all

ARG DATA_PATH="data"
COPY  ${DATA_PATH}/launch.sh .
COPY  ${DATA_PATH}/requirements.txt .

RUN chmod +x /launch.sh \
    && pip3 install -r requirements.txt --user

ENTRYPOINT ["/launch.sh"]