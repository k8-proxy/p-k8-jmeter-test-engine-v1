# Test engine deployment with the OVA file
1. Get the latest OVA image from AWS S3 k8-jmeter-test-engine-data bucket
2. 
    - When deploying on a VMware ESXi host, create a new VM (In Virtual Machines click on 'Create / Register VM') and choose 'Deploy a virtual machine from an OVF or OVA file'. Follow the deployment wizard instructions.
    - When deploying on a VMware Workstation in select 'File/Open' menu and navigate to the OVA file location on the computer
3. Once the VM starts login with user `glasswall` and password `Gl@sswall`
4. Make sure the VM can access the network. If necessary, set static IP by following the [instructions](https://www.howtoforge.com/linux-basics-set-a-static-ip-on-ubuntu)
5. Try listing the current pods with the following command:
```
    kubectl get pods --all-namespaces
```
The output should look like
```
    NAMESPACE     NAME                                         READY   STATUS    RESTARTS   AGE
    kube-system   dashboard-metrics-scraper-6c4568dc68-4fzw6   1/1     Running   19         41h
    kube-system   metrics-server-8bbfb4bdb-f7mhl               1/1     Running   17         41h
    kube-system   kubernetes-dashboard-7ffd448895-gzfrs        1/1     Running   21         41h
    kube-system   coredns-86f78bb79c-2pbz9                     1/1     Running   19         41h
    kube-system   tiller-deploy-69c484895f-sj4tv               1/1     Running   10         16h
    kube-system   calico-kube-controllers-847c8c99d-t5gr5      1/1     Running   18         41h
    kube-system   calico-node-wn6rf                            1/1     Running   26         41h
    common        influxdb-0                                   1/1     Running   8          16h
    common        minio-774cb77ff5-r47b7                       1/1     Running   9          16h
    common        grafana-568dfdfc94-d2qrc                     1/1     Running   7          16h
```
6. In some case step 5 on the initially deployed VM might fail with the following error
```
    Unable to connect to the server: x509: certificate has expired or is not yet valid: current time 2020-05-03T23:53:06Z is after 2020-05-03T16:38:01Z
```
If this is the case run the command below
```
    sudo microk8s.refresh-cert
```
Wait until microk8s restarts and retry step 5
7. Open a new terminal tab and run the following:
```
    kubectl port-forward -n common service/minio-service 9000:80
```
In another terminal tab
```
    kubectl port-forward -n common service/grafana-service 3000:80
```
8. Open the Mozilla browser and navigate to the following pages 
Minio http://localhost:9000
Grafana http://localhost:3000
The credentials for both are admin/admin@123
9. Open a new terminal tab and run the following:
```
cd ~/p-k8-jmeter-test-engine/jmeter-icap/scripts/
```
Here make sure the parameters passed to the master script are correct
```
    cat config.env
```
Then run the master script
```
    sudo python3 create_stack_dash.py 
```
The output should look as follows:
```
    Creating Load Generators...
    INFO:create_stack:TOTAL USERS         100
    INFO:create_stack:USERS PER INSTANCE  25
    INFO:create_stack:TEST DURATION       300
    INFO:create_stack:FILE LIST           ../testdata/files01.csv
    INFO:create_stack:MINIO URL           http://minio-service.common:80
    INFO:create_stack:MINIO INPUT BUCKET  input
    INFO:create_stack:MINIO outPUT BUCKET output
    INFO:create_stack:INFLUXDB URL        http://influxdb-service.common:80
    INFO:create_stack:INFLUX HOST         influxdb-service.common
    INFO:create_stack:PREFIX              demo
    INFO:create_stack:ICAP SERVER         gw-icap02.westeurope.azurecontainer.io
    Client Version: version.Info{Major:"1", Minor:"19+", GitVersion:"v1.19.3-34+a56971609ff35a", GitCommit:"a56971609ff35ac8cc90b2aef89165208bff3fe1", GitTreeState:"clean", BuildDate:"2020-11-06T11:56:24Z", GoVersion:"go1.15.3", Compiler:"gc", Platform:"linux/amd64"}
    Server Version: version.Info{Major:"1", Minor:"19+", GitVersion:"v1.19.3-34+a56971609ff35a", GitCommit:"a56971609ff35ac8cc90b2aef89165208bff3fe1", GitTreeState:"clean", BuildDate:"2020-11-06T11:57:19Z", GoVersion:"go1.15.3", Compiler:"gc", Platform:"linux/amd64"}
    INFO:create_stack:Micro k8s           True
    No resources found
    secret/jmeterconf created
    secret/filesconf created
    INFO:create_stack:Number of pods to be created: 4
    job.batch/demo-jmeterjob created
    Creating dashboard...
    Dashboard created at: 
    http://localhost:3000/d/cfbjZi0Mz/demo-icap-live-performance-dashboard
    Stack will be deleted after 20.0 minutes
    0.0 minutes have elapsed, stack will be deleted in 20.0 minutes
```
10. At the moment Grafana is supposed to have a newly created dashboard whose name starts with the prefix passed to the master script. Open the dashboard and watch a visualization of the running test 