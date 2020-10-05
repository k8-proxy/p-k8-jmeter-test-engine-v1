
## Elasticsearch conf. set on each node or container startup: 
``` 
sudo sysctl -w vm.max_map_count=262144
```

# EFK on docker-compose:
```
cd docker-compose-efk
docker-compose up -d
jmeter -n -t jmeter/glasswallsolutions.local.jmx -l jmeter/results/results.csv

```

# Grafana, Prometheus and InfluxDB (GPI)
```
cd docker-compose-gpi
```
### - Copy JMeter prometheus and InfluxDB modules to [JMETER_VOL]:/lib/ext/ and Set influxDB service address and port in your .jmx file
```
cp ../jmeter_modules/* [JMETER_VOL]:/lib/ext/
```

### - Replace [JMETER_SERVICE_IP] in prometheus-config/prometheus.yml 
```
# ex:
sed -i'.bak' '1,3 s/[JMETER_SERVICE_IP]/127.0.0.1/g' prometheus-config/prometheus.yml
```

### - Start Testing
```
docker-compose up -d
jmeter -n -t jmeter/glasswallsolutions.local.jmx -l ./jmeter/results/results.csv -Dprometheus.ip=0.0.0.0
```

# Grafana, Prometheus, InfluxDB, Elasticsearch, Kibana, Fluentd on k8s

- This is the final step for monitoring stack.
it contains everything we need for monitoring jmeter and other traffik generators.

___
```
cd k8s
```
- /DATA directory contains all configuration files and persistent service data like Elasticsearch and Prometheus data. you can replace it with PVC and storage classes.

### - Copy /DATA directory to PVC or shared storage betweeb k8s nodes.
```
cp -r /DATA [sharedStorage]:/
```

### - Review *-dep.yaml file and chanage mounted volumes if needed.

### - Configurable files:
```
/DATA/prometheus/conf/prometheus.yml 
/DATA/grafana/grafana-provisioning/datasources/datasource.yml
/DATA/grafana/grafana-provisioning/dashboards/dashboard.yml
/DATA/jmeter/glasswallsolutions.com.jmx
```

### - building fluentd docker image
```
cd k8s/
docker build -t fluentd-with-elasticsearch-module -f Dockerfile.fluentd.image .
```

### Apply deployments
```
kubectl apply .
```

- Services and URLs:
```
Elasticsarch:
external: NODE_IP:30858
internal: elasticsearch-service:9200

Grafana:
external: NODE_IP:30856

Influxdb:
external: NODE_IP:30854
internal: influxdb-service:8086

Kiabana:
external: NODE_IP:30857

Prometheus:
external: NODE_IP:30855
internal: prometheus-service:9090
```
