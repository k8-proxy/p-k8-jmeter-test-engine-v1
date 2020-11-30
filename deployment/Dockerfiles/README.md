# DockerImages 

## Overview

* [jmeter-base](https://github.com/k8-proxy/p-k8-jmeter-test-engine/blob/master/deployment/Dockerfiles/jmeter-base)
* [jmeter-testdata](https://github.com/k8-proxy/p-k8-jmeter-test-engine/blob/master/deployment/Dockerfiles/jmeter-testdata)

## Build and publish base image 


```shell
$ docker build . -t glasswallsolutions/cloud-qa:jmeter-ubuntu -f deployment/Dockerfiles/jmeter-base
$ docker push glasswallsolutions/cloud-qa:jmeter-ubuntu
```

## Build and publish testdata image


```shell
$ docker build . -t glasswallsolutions/cloud-qa:jmeter-engine -f deployment/Dockerfiles/jmeter-testdata 
$ docker push glasswallsolutions/cloud-qa:jmeter-engine
```
