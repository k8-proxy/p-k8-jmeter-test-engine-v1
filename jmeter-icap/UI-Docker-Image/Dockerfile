FROM glasswallsolutions/k8-centos7

RUN yum install python3 wget -y \
	&& yum clean all

ARG DATA_PATH="data"
COPY  ${DATA_PATH}/launch.sh .
COPY  ${DATA_PATH}/requirements.txt .
COPY  ${DATA_PATH}/wandisco-git.repo /etc/yum.repos.d
COPY  ${DATA_PATH}/kubernetes.repo /etc/yum.repos.d

RUN rpm --import http://opensource.wandisco.com/RPM-GPG-KEY-WANdisco
RUN yum install git -y
RUN git clone https://github.com/k8-proxy/p-k8-jmeter-test-engine.git

RUN yum install -y kubectl

RUN chmod +x /launch.sh
RUN pip3 install -r requirements.txt --user
RUN curl -sL https://rpm.nodesource.com/setup_10.x | bash -
RUN yum install nodejs -y
RUN npm install -g @angular/cli -y
RUN npm install -g http-server -y


ENTRYPOINT ["/launch.sh"]