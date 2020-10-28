## secrets

- Default username/password for minio and grafana is `admin/admin@123`

- Secrets can be created/viewed with below commands. Update [secrets-file](https://github.com/k8-proxy/p-k8-jmeter-test-engine/blob/helm-charts/helm-charts/common-resources/templates/secrets.yaml) if required.

Creating secret
```shell
$ echo -n 'admin' | base64
YWRtaW4=
```

Decoding secret

```shell
echo 'YWRtaW4=' | base64 --decode
```

## Port Forwarding

### Grafana

```shell
$ kubectl port-forward -n common service/grafana-service 3000:80
```
### Minio

```shell
$ kubectl port-forward -n common service/minio-service 9000:80
```
### InfluxDB

```shell
kubectl port-forward -n common service/influxdb-service 8086:80
```
