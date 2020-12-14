# Introduction
OVA image encapsulates the JMeter engine test environment within a single virtual machine<br/>
![traffic](pngs/jmeter-test-ova.png)<br/>
The environment does not have to scale up capabilities (like in EKS or AKS). However, it allows us to demonstrate the whole workflow along with results visualization in a Grafana dashboard.
# Test engine deployment with OVA
1. Get the latest OVA image from Glasswall AWS S3 icap-performance-test-data-bucket bucket<br/>
![bucket](pngs/aws-bucket.png)
2. 
    - When deploying on a VMware ESXi host, create a new VM (In Virtual Machines click on 'Create / Register VM') and choose 'Deploy a virtual machine from an OVF or OVA file'. Follow the deployment wizard instructions.
    ![ova_esxi](pngs/ova_esxi.png)
    - When deploying on a VMware Workstation in select 'File/Open' menu and navigate to the OVA file location on the computer<br/>
    ![ova_workstation](pngs/ova_workstation.png)
3. Once the VM starts login with user `glasswall`
4. Steps to setup static IP. <br/>
The VM has a preset static IP address to run on Glasswall VMware ESXi host.<br/>

- Identify available network interface
  
  ```sh
   ip link show
  ```
  Result:
  
   1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00</br>
    
   2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000 link/ether 00:0c:29:00:22:80 brd ff:ff:ff:ff:ff:ff
 
- Enable the network interface

```sh
sudo ifconfig ens33 up
```

```sh
sudo nano /etc/netplan/01-network-manager-all.yaml
```

- Add below content to `/etc/netplan/01-network-manager-all.yaml`. Mention network interface name and other network details accordingly.

Sample:
```yaml
network:
    ethernets:
        ens33:
            addresses: [91.109.26.22/27]
            gateway4: 91.109.26.30
            nameservers:
              addresses: [8.8.4.4,8.8.8.8]
    version: 2
```

- Once done run below commands to apply network changes

```sh
sudo netplan apply
reboot
```

5. In a terminal window try listing the current pods with the following command:
```
    kubectl get pods -A
```
The output should look like
```
    NAMESPACE     NAME                                         READY   STATUS
    common        loki-promtail-fm5j6                          1/1     Running
    common        promtail-5wkxz                               1/1     Running
    kube-system   metrics-server-8bbfb4bdb-f7mhl               1/1     Running
    kube-system   calico-node-wn6rf                            1/1     Running
    kube-system   calico-kube-controllers-847c8c99d-t5gr5      1/1     Running
    common        influxdb-0                                   1/1     Running
    common        grafana-568dfdfc94-lzfmf                     0/1     Pending
    kube-system   kubernetes-dashboard-7ffd448895-gzfrs        1/1     Running
    common        minio-774cb77ff5-r47b7                       1/1     Running
    kube-system   dashboard-metrics-scraper-6c4568dc68-4fzw6   1/1     Running
    kube-system   coredns-86f78bb79c-2pbz9                     0/1     Running
    common        loki-0                                       0/1     Running
    kube-system   tiller-deploy-69c484895f-sj4tv               0/1     Running
```
wait until all the PODs are `READY` and `Running`<br/>
6. In some cases step 5 on the initially deployed VM might fail with the following error
```
    Unable to connect to the server: x509: certificate has expired or is not yet valid: current time 2020-05-03T23:53:06Z is after 2020-05-03T16:38:01Z
```
or 
```
The connection to the server 127.0.0.1:16443 was refused - did you specify the right host or port?
```
If this is the case run the command below
```
    sudo microk8s.refresh-cert
```
Wait until microk8s restarts and retry step 5

Generate Load using Command Line - https://github.com/k8-proxy/p-k8-jmeter-test-engine/blob/master/instructions/How%20to%20generate%20load%20with%20OVA%20utilizing%20command%20line.md
