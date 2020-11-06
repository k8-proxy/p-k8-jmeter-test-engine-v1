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
    python3 create_stack.py --total_users <number of users> --users_per_instance <number of users> --duration <test duaration> --list <file list>
```
Here:
<table>
<tr>
<td width="180"> Option </td> <td> Description </td>
</tr>
<tr>
<td> --total_users, -t </td>
<td>
Total number of users for the test. If not specified, the default value of 100 will be used
</td>
</tr>
<tr>
<td> --users_per_instance, -u </td>
<td>
Users per POD. If not specified, the default value of 25 will be used
</td>
</tr>
<tr>
<td> --duration, -d </td>
<td>
Duration of the test. If not specified, the default value of 60 seconds will be used
</td>
</tr>
<tr>
<td> --list, -l </td>
<td>
The list of the files in the Minio `input` bucket to be included in the test
</td>
</tr>
</table>
### Test termination
To stop the test and release the resources run the following command
```
    python3 delete_stack.py
```