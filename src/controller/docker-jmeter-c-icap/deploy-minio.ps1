kubectl apply -f minio.yaml
Start-Sleep -Seconds 5
Start-Process -FilePath "kubectl" -ArgumentList "port-forward service/output-queue 9000:9000"
Start-Process 'http://localhost:9000/'
