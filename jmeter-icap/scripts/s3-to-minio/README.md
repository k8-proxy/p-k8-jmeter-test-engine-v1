# Download files from S3 and upload to Minio

Specify AWS credentials by running:
```
    aws configure
```
or by creating `~/.aws/credentials` and `~/.aws/config` files with the following content:

```
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

```
[default]
region = YOUR_PREFERRED_REGION
```

Run the script with the following command line:
```
    python3 's3-to-minio.py -b <bucket name> -c <cvs file path> -m <minio URL> -a <minio access ket> -s <minio secret key>'
```
