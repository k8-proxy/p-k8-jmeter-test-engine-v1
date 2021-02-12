FROM glasswallsolutions/k8-centos7

RUN yum install python3 wget -y \
	&& yum clean all

ARG DATA_PATH="data"
COPY  ${DATA_PATH}/launch.sh .
COPY  ${DATA_PATH}/requirements.txt .

RUN chmod +x /launch.sh
RUN pip3 install -r requirements.txt --user
RUN curl -sL https://rpm.nodesource.com/setup_10.x | bash -
RUN yum install nodejs -y
RUN npm install -g @angular/cli -y
RUN npm install -g http-server -y


ENTRYPOINT ["/launch.sh"]