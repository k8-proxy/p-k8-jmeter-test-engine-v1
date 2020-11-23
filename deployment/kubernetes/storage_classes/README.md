## This folder contains the storage classes of persistent volumes

## Azure Kubernetes Service

`azure-file` storage class supports read/write from multiple pods. This means all pods of a deployment can use the same volume even though the pods are scheduled on different nodes in the cluster.

If this storage class is not the default storage class in the kubernetes cluster, we need to explicitly mention the storage class name in persistent volume claims.

Run the below one time command in the cluster to create the storage class:

`kubectl apply -f azure-file-storage.yaml`


## Elastic Kubernetes Service (AWS)

create an EFS in the same region where EKS is deployed.

Run below command to after updating the EFS id and region in below command to create the provisioner for EFS.

```
helm install --name efs-provisioner \
    --namespace default \
    --set  efsProvisioner.efsFileSystemId=fs-xxxxxx \
    --set efsProvisioner.awsRegion=us-east-1
    stable/efs-provisioner
```
Once the efs provisioner is deployed, the storage class `efs` can be used in persistent volume claims

