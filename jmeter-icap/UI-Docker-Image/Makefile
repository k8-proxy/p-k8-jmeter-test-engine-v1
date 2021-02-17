image-name="ggrig/ui-k8s-jmeter:0.01"

build:
	sudo docker build -t $(image-name) .

run:
	sudo docker run -d --name engine_ui --privileged $(image-name)

bash:
	sudo docker exec -it engine_ui /bin/bash

push:
	sudo docker push $(image-name)

listcont:
	sudo docker ps -aq

cleancont:
	sudo docker stop $$(sudo docker ps -aq)
	sudo docker rm $$(sudo docker ps -aq)

