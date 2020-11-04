## Expose Minio Service


- Create load-balancer service for minio. Create `minio-lb.yaml` and paste below content

```shell
apiVersion: v1
kind: Service
metadata:
  name: minio-lb-svc
  namespace: common
spec:
  type: LoadBalancer
  ports:
  - port: 80
  selector:
    app: minio
  loadBalancerSourceRanges:
  - <MY_EXTERNAL_IP>
```

- `kubectl apply -f minio-lb.yaml`