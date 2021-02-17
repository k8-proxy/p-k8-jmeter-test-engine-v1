image-name="ggrig/ui-k8s-jmeter:0.01"

build:
	sudo docker build -t $(image-name) .

run:
	sudo docker run -d --name engine_ui --privileged $(image-name)

run1:
	sudo docker run --name engine_ui --privileged -ti -e container=docker  -v /sys/fs/cgroup:/sys/fs/cgroup  $(image-name) /usr/sbin/init

bash:
	sudo docker exec -it engine_ui /bin/bash

push:
	sudo docker push $(image-name)

imgs:
	sudo docker images

cont:
	sudo docker ps -aq

clean:
	sudo docker stop $$(sudo docker ps -aq)
	sudo docker rm $$(sudo docker ps -aq)

