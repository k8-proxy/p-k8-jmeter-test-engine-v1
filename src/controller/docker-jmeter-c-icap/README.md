# ICAP+JMeter Dockerfile

## Minio
### Deploy Minio
```
    powershell -ExecutionPolicy ByPass -File .\deploy-minio.ps1
```
This deploys Minio, opens it in the browser and starts a processor pod
To login to Minio use the following credentials
User: test
PSW: test@123
After a while the JMeter output files should appear in Minio
### Remove Minio deployement
```
    powershell -ExecutionPolicy ByPass -File .\delete-minio.ps1
```
## JMeter Jobs
### Run
On Windows 10 run the following from within the PowerShell
```
    powershell -ExecutionPolicy ByPass -File run.ps1 <jmx_file> <number_of_pods>
```
So, to start 10 JMeter jobs run:
```
    powershell -ExecutionPolicy ByPass -File run.ps1 .\icap.jmx 10
```
### Stop and remove 
```
    powershell -ExecutionPolicy ByPass -File stop.ps1
```