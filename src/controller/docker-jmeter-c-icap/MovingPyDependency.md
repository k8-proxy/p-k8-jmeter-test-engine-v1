# ICAP+JMeter Dockerfile

## Using MinIO
Script ICAP_POC_Minio.jmx is removing python script (upload.py and download.py) dependency from ICAP_POC_s3_k8.jmx script.
It uses minio-7.1.4.jar that should be imported from Maven into JMeter lib folder.
It executes upload and download based on MinIO API directly as part of JSR232Sampler.