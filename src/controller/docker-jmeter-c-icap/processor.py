import os
import logging
import logging.config
from pythonjsonlogger import jsonlogger
from datetime import datetime;
import boto3
import requests
import time
from botocore.client import Config
from botocore.exceptions import ClientError
from os import listdir
from os.path import isfile, join

class ElkJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(ElkJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('file processor')

TGT_URL = os.getenv('TARGET_MINIO_URL', 'http://127.0.0.1:9000')
TGT_ACCESS_KEY = os.getenv('TARGET_MINIO_ACCESS_KEY', 'test')
TGT_SECRET_KEY = os.getenv('TARGET_MINIO_SECRET_KEY', 'test@123')
TGT_BUCKET = os.getenv('TARGET_MINIO_BUCKET', 'output')

OUTPUT_PATH = os.getenv('OUTPUT_PATH', '/usr/share/Test/output/')
REPORT_PATH = os.getenv('OUTPUT_PATH', '/usr/share/Test/report/')
REPORT_BUCKET = os.getenv('REPORTS_MINIO_BUCKET', 'reports')

POD_NAME = os.getenv('POD_NAME', 'file-processor-pod')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

SHELL_ACCESS = True

class Main():

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def upload_to_minio(bucket, file_path, filename):
        try:
            logger.info('Uploading file {}.'.format(filename))

            s3 = boto3.resource('s3', endpoint_url=TGT_URL, aws_access_key_id=TGT_ACCESS_KEY,
                                aws_secret_access_key=TGT_SECRET_KEY, config=Config(signature_version='s3v4'))
            logger.debug('Checking if the Bucket to upload files exists or not.')
            if (s3.Bucket(bucket) in s3.buckets.all()) == False:
                logger.info('Bucket not Found. Creating Bucket.')
                s3.create_bucket(Bucket=bucket)
            logger.debug('Uploading file to bucket {} minio {}'.format(bucket, TGT_URL))
            file_to_upload = file_path + filename
            s3.Bucket(bucket).upload_file(file_to_upload, filename)
        except ClientError as e:
            logger.error("Cannot connect to the minio {}. Please vefify the Credentials.".format(bucket))
        except Exception as e:
            logger.info(e)

    @staticmethod
    def application():
        #if os.name == 'nt':
        #    file_path = 'C:/GW/files/'
        try:
            for f in listdir(OUTPUT_PATH):
                if isfile(join(OUTPUT_PATH, f)):
                    logger.info(f)
                    Main.upload_to_minio(TGT_BUCKET, OUTPUT_PATH, f)

            report_file = POD_NAME + '.tar.gz'
            os.system('tar -zcvf ' + report_file + ' /usr/share/Test/report/')
            Main.upload_to_minio(REPORT_BUCKET, '/', report_file)
            exit(0)
            
        except Exception as e:
            logger.error(e)

    @staticmethod
    def main():
        Main.log_level(LOG_LEVEL)
        #if os.name == 'nt':
        #    file_path = 'C:/GW/files/'
        #else:
        os.system('/usr/share/Test/launch.sh')
        # os.system('service filebeat start')

        while True:
            Main.application()
            time.sleep(5)

if __name__ == "__main__":
    Main.main()
