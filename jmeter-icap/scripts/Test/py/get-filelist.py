import os
import logging
import sys, getopt
import boto3
import requests
import time
import uuid
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
    MINIO_BUCKET = "filelist"
    file_name = 'files'

    prefix = os.getenv('POD_NAME',str(uuid.uuid4()))

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def get_filelist():
        try:
            s3 = boto3.resource('s3', endpoint_url=Main.MINIO_URL, aws_access_key_id=Main.MINIO_ACCESS_KEY,
                                aws_secret_access_key=Main.MINIO_SECRET_KEY, config=Config(signature_version='s3v4'))
            if (s3.Bucket(Main.MINIO_BUCKET) in s3.buckets.all()) == False:
                logger.error('Bucket not Found.')
                exit(1)
            logger.debug('dwonloading file from bucket {} minio {}'.format(Main.MINIO_BUCKET, Main.MINIO_URL))
            s3.Bucket(Main.MINIO_BUCKET).download_file(Main.file_name, Main.file_name)
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
            for line in search.readlines():
                linenumber += 1
                if "<stringProp name=\"Argument.name\">MINIO_URL</stringProp>" in line:
                    MINIO_URL_line = linenumber + 1
                if linenumber == MINIO_URL_line:
                    Main.MINIO_URL = line.strip().replace("<stringProp name=\"Argument.value\">","").replace("</stringProp>","")
                if "<stringProp name=\"Argument.name\">MINIO_ACCESS_KEY</stringProp>" in line:
                    MINIO_ACCESS_KEY_line = linenumber + 1
                if linenumber == MINIO_ACCESS_KEY_line:
                    Main.MINIO_ACCESS_KEY = line.strip().replace("<stringProp name=\"Argument.value\">${__P(p_minio_access_key,","").replace(")}</stringProp>","").replace('&amp;','&')
                if "<stringProp name=\"Argument.name\">MINIO_SECRET_KEY</stringProp>" in line:
                    MINIO_SECRET_KEY_line = linenumber + 1
                if linenumber == MINIO_SECRET_KEY_line:
                    Main.MINIO_SECRET_KEY = line.strip().replace("<stringProp name=\"Argument.value\">${__P(p_minio_secret_key,","").replace(")}</stringProp>","").replace('&amp;','&') 
        except Exception as e:
            logger.info(e)


    @staticmethod
    def main(argv):
        helpstring = 'pyton3 get-filelist.py -j <jmeter conf file>'
        try:
            opts, args = getopt.getopt(argv,"hj:",["help=","jmx_file_path="])
        except getopt.GetoptError:
            print (helpstring)
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print (helpstring)
                sys.exit()
            elif opt in ("-j", "--jmx_file_path"):
                Main.jmx_file_path = arg

        Main.log_level(LOG_LEVEL)
        logger.info(Main.log_file_path)
        logger.info(Main.jmx_file_path)
        Main.get_mino_credentials()
        logger.info(Main.MINIO_URL)
        #logger.info(Main.MINIO_ACCESS_KEY)
        #logger.info(Main.MINIO_SECRET_KEY)
        logger.info(Main.MINIO_BUCKET)
        Main.get_filelist()

if __name__ == "__main__":
    Main.main(sys.argv[1:])