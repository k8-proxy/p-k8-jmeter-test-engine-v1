import os
import logging
import sys, getopt
import boto3
import requests
import time
import csv
import threading
import uuid
from botocore.client import Config
from botocore.exceptions import ClientError

logger = logging.getLogger('s3-to-minio')
s3_client = boto3.client('s3')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()


class Main():

    bucketname = ''
    cvs_file = ''
    minio_URL = ''
    minio_access_key = ''
    minio_secret_key = ''

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def create_minio_bucket(bucket_name):
        s3 = boto3.resource('s3', endpoint_url=Main.minio_URL, aws_access_key_id=Main.minio_access_key,
                            aws_secret_access_key=Main.minio_secret_key, config=Config(signature_version='s3v4'))
        logger.debug('Checking if the Bucket to upload files exists or not.')
        if (s3.Bucket(bucket_name) in s3.buckets.all()) == False:
            logger.info('Bucket not Found. Creating Bucket.')
            s3.create_bucket(Bucket=bucket_name)

    @staticmethod
    def upload_to_minio(bucket_name, s3_file, basename):
        logger.info('Uploading file {}.'.format(os.path.basename(s3_file)))
        i = 0
        wait_time = 1
        while i < 10:
            try:
                s3 = boto3.resource('s3', endpoint_url=Main.minio_URL, aws_access_key_id=Main.minio_access_key,
                                    aws_secret_access_key=Main.minio_secret_key, config=Config(signature_version='s3v4'))
                logger.debug('Uploading file to bucket {} minio {}'.format(bucket_name, Main.minio_URL))
                s3.Bucket(bucket_name).upload_file(basename, s3_file)
                break
            except Exception as e:
                logger.info(e)
            i += 1
            logger.info('Waiting {} seconds.'.format(wait_time))
            time.sleep(wait_time)
            wait_time *= 2

    @staticmethod
    def process_s3_file(bucketname, s3_file):
        try:
            s3 = boto3.resource('s3')
            a = uuid.uuid4()
            basename = str(a)#os.path.basename(s3_file)
            s3.Bucket(bucketname).download_file(s3_file, basename)
            Main.upload_to_minio(bucketname, s3_file, basename)
            os.remove(basename)
        except Exception as e:
            logger.info(e)

    @staticmethod
    def process_the_csv_file(csv_file_path):
        Main.create_minio_bucket(Main.bucketname)
        filename_idx = 1
        path_idx = 2
        with open(csv_file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            threads = list()
            for row in csv_reader:
                line_count += 1
                if line_count == 1:
                    # Skip the first (header) line
                    continue
                basename = row[filename_idx]
                path = row[path_idx]
                if path.startswith('/'):
                    path = path[1:]
                if not path.endswith('/'):
                    path += '/'
                s3_file = path + basename
                x = threading.Thread(target=Main.process_s3_file, args=(Main.bucketname, s3_file,))
                threads.append(x)
                x.start()
                # limit the number of parallel threads
                if line_count % 100 == 0:
                    # Clean up the threads
                    logging.info ('Lines processed so far {}'.format(line_count))
                    for index, thread in enumerate(threads):
                        thread.join()
                        if index >= line_count:
                            logging.info("Main    : thread %d done", index)


            for index, thread in enumerate(threads):
                thread.join()
                logging.info("Main    : thread %d done", index)

    @staticmethod
    def main(argv):
        help_string = 's3-to-minio.py -b <bucketname> -c <cvs file path> -m <minio URL> -a <minio access ket> -s <minio secret key>'
        try:
            opts, args = getopt.getopt(argv,"hb:c:m:a:s:",["bucket=","cvs=","minio=","access=","secret="])
        except getopt.GetoptError:
            print (help_string)
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print (help_string)
                sys.exit()
            elif opt in ("-b", "--bucket"):
                Main.bucketname = arg
            elif opt in ("-c", "--cvs"):
                Main.cvs_file = arg
            elif opt in ("-m", "--minio"):
                Main.minio_URL = arg
            elif opt in ("-a", "--access"):
                Main.minio_access_key = arg
            elif opt in ("-s", "--secret"):
                Main.minio_secret_key = arg

        Main.log_level(LOG_LEVEL)
        logger.info(Main.bucketname)
        logger.info(Main.cvs_file)
        logger.info(Main.minio_URL)
        logger.info(Main.minio_access_key)
        logger.info(Main.minio_secret_key)

        Main.process_the_csv_file(Main.cvs_file)

if __name__ == "__main__":
    Main.main(sys.argv[1:])