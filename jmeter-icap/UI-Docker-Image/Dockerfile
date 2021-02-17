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
RUN yum install -y openssl-devel
RUN yum install -y libffi-devel
RUN yum install -y python3-devel


RUN yum -y update; yum clean all
RUN yum -y install systemd; yum clean all; \
(cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;
VOLUME [ "/sys/fs/cgroup" ]
CMD ["/usr/sbin/init"]

RUN yum install -y httpd
RUN systemctl enable httpd

ENTRYPOINT ["/launch.sh"]