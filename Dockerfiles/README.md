# DockerImages 

## Overview

* [jmeter-base](https://github.com/k8-proxy/p-k8-jmeter-test-engine/blob/docker-images/Dockerfiles/jmeter-base)
* [jmeter-testdata](https://github.com/k8-proxy/p-k8-jmeter-test-engine/blob/docker-images/Dockerfiles/jmeter-testdata)

## Build and publish base image 


```shell
$ docker build . -t glasswallsolutions/jmeter:5.3 -f Dockerfiles/jmeter-base
$ docker push glasswallsolutions/jmeter:5.3
```

## Build and publish testdata image


```shell
$ docker build . -t glasswallsolutions/jmeter:testdata -f Dockerfiles/jmeter-testdata 
$ docker push glasswallsolutions/jmeter:testdata
```
