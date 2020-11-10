# ICAP+JMeter Dockerfile

## Access Minio
Run below command to do port forwarding in order to access minio locally
```
kubectl port-forward -n minio svc/minio 9000
```
you can access minio using http://localhost:9000/
## Access Grafana Dashboard
To do port forwarding in order to access Grafana locally, run the command below
```
kubectl port-forward -n grafana service/grafana-service 3000
```
you can access grafana using http://localhost:3000/

Create a Minio bucket called `input` and upload your test files there

Create an influx DB database called `JMeter` on the influx DB POD

## Starting JMeter PODs
The python script will allow you to start the JMeter traffic on Linux, Windos and Mac OS,
The CLI command to start it is:
```
    python3 create_stack.py --total_users <number of users> --users_per_instance <number of users> --duration <test duaration> --list <file list> --minio_url <url> --minio_access_key <access key> --minio_secret_key <secret key> --minio_input_bucket <bucket name> --minio_output_bucket <bucket name> --influxdb_url <url> --prefix <prefix> --icap_server <url>
```
Here:
<table>
<tr>
<td width="180"> Option </td> <td> Description </td>
</tr>
<tr>
<td> --total_users </td>
<td>
Total number of users for the test. If not specified, the default value of 100 will be used
</td>
</tr>
<tr>
<td> --users_per_instance </td>
<td>
Users per POD. If not specified, the default value of 25 will be used
</td>
</tr>
<tr>
<td> --duration </td>
<td>
Duration of the test. If not specified, the default value of 60 seconds will be used
</td>
</tr>
<tr>
<td> --list </td>
<td>
The list of the files in the Minio `input` bucket to be included in the test
</td>
</tr>
<tr>
<td> --minio_url </td>
<td>
The Minio endpoint URL. The default value is 'http://minio.minio.svc.cluster.local:9000'
</td>
</tr>
<tr>
<td> --minio_access_key </td>
<td>
The Minio access key
</td>
</tr>
<tr>
<td> --minio_secret_key </td>
<td>
The Minio secret key
</td>
</tr>
<tr>
<td> --minio_input_bucket </td>
<td>
The Minio input bucket. The default value is 'input'
</td>
</tr>
<tr>
<td> --minio_output_bucket </td>
<td>
The Minio output bucket. The default value is 'output'
</td>
</tr>
<tr>
<td> --influxdb_url </td>
<td>
The InfluxDB URL. The default value is 'http://influxdb.influxdb.svc.cluster.local:8086'
</td>
</tr>
<tr>
<td> --prefix </td>
<td>
Influxdb database name prefix. The default value is 'demo'
</td>
</tr>
<tr>
<td> --icap_server </td>
<td>
ICAP server URL. The default value is 'icap02.glasswall-icap.com'
</td>
</tr>
</table>
The `--users_per_instance` parameter also defines the PODs' CPU and RAM.
The resources to be allocated are based on the following table:
<table>
<tr>
<td> Users per instance </td>
<td> RAM size </td>
<td> CPU </td>
</tr>
<tr>
<td> 0 < n <= 50 </td>
<td> 768Mi </td>
<td> 500m </td>
</tr>
<tr>
<td> 50 < n <= 100 </td>
<td> 1280Mi </td>
<td> 1000m </td>
</tr>
<tr>
<td> 100 < n <= 200 </td>
<td> 2304Mi </td>
<td> 2000m </td>
</tr>
</table>

## Test termination
To stop the test and release the resources run the following command
```
    python3 delete_stack.py
```