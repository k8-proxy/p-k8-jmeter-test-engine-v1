import os
import logging
import sys, getopt
import boto3
import requests
import time
from botocore.client import Config
from botocore.exceptions import ClientError

logger = logging.getLogger('file processor')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

class Main():

    log_file_path = ''
    jmx_file_path = ''

    MINIO_URL = ""
    MINIO_ACCESS_KEY = ""
    MINIO_SECRET_KEY = ""
    MINIO_BUCKET = ""

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def upload_to_minio(file_path):
        logger.info('Uploading file {}.'.format(file_path))
        try:
            s3 = boto3.resource('s3', Main.MINIO_URL, Main.MINIO_ACCESS_KEY, Main.MINIO_SECRET_KEY, Config('s3v4'))
            logger.debug('Checking if the Bucket to upload files exists or not.')
            if (s3.Bucket(Main.MINIO_BUCKET) in s3.buckets.all()) == False:
                logger.info('Bucket not Found. Creating Bucket.')
                s3.create_bucket(Bucket=Main.MINIO_BUCKET)
            logger.debug('Uploading file to bucket {} minio {}'.format(Main.MINIO_BUCKET, Main.MINIO_URL))
            s3.Bucket(Main.MINIO_BUCKET).upload_file(file_path, "jmeter-logs/" + os.path.basename(file_path))
        except Exception as e:
            logger.info("Error {}".format(e))

    @staticmethod
    def get_mino_credentials():
        try:
            search = open(Main.jmx_file_path,"r")
            linenumber = 0
            MINIO_URL_line = 0
            MINIO_ACCESS_KEY_line = 0
            MINIO_SECRET_KEY_line = 0
            MINIO_BUCKET_line = 0
            for line in search.readlines():
                linenumber += 1
                if "<stringProp name=\"Argument.name\">MINIO_URL</stringProp>" in line:
                    MINIO_URL_line = linenumber + 1
                if linenumber == MINIO_URL_line:
                    Main.MINIO_URL = line.strip().replace("<stringProp name=\"Argument.value\">","").replace("</stringProp>","")
                if "<stringProp name=\"Argument.name\">MINIO_ACCESS_KEY</stringProp>" in line:
                    MINIO_ACCESS_KEY_line = linenumber + 1
                if linenumber == MINIO_ACCESS_KEY_line:
                    Main.MINIO_ACCESS_KEY = line.strip().replace("<stringProp name=\"Argument.value\">${__P(p_minio_access_key,","").replace(")}</stringProp>","")
                if "<stringProp name=\"Argument.name\">MINIO_SECRET_KEY</stringProp>" in line:
                    MINIO_SECRET_KEY_line = linenumber + 1
                if linenumber == MINIO_SECRET_KEY_line:
                    Main.MINIO_SECRET_KEY = line.strip().replace("<stringProp name=\"Argument.value\">${__P(p_minio_secret_key,","").replace(")}</stringProp>","")
                if "<stringProp name=\"Argument.name\">MINIO_BUCKET_OUTPUT</stringProp>" in line:
                    MINIO_BUCKET_line = linenumber + 1
                if linenumber == MINIO_BUCKET_line:
                    Main.MINIO_BUCKET = line.strip().replace("<stringProp name=\"Argument.value\">${__P(p_minio_bucket_output,","").replace(")}</stringProp>","")
        except Exception as e:
            logger.info(e)

    @staticmethod
    def main(argv):
        helpstring = 'test.py -l <log file path>'
        try:
            opts, args = getopt.getopt(argv,"hl:j:",["help=","log_file_path=","jmx_file_path="])
        except getopt.GetoptError:
            print (helpstring)
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print (helpstring)
                sys.exit()
            elif opt in ("-l", "--log_file_path"):
                Main.log_file_path = arg
            elif opt in ("-j", "--jmx_file_path"):
                Main.jmx_file_path = arg

        Main.log_level(LOG_LEVEL)
        logger.info(Main.log_file_path)
        logger.info(Main.jmx_file_path)
        Main.get_mino_credentials()
        logger.info(Main.MINIO_URL)
        logger.info(Main.MINIO_ACCESS_KEY)
        logger.info(Main.MINIO_SECRET_KEY)
        logger.info(Main.MINIO_BUCKET)
        Main.upload_to_minio(Main.log_file_path)

if __name__ == "__main__":
    Main.main(sys.argv[1:])