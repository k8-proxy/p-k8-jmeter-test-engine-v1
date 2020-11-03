import os
import logging
import sys, getopt
import time
import uuid
import platform
import subprocess
import shutil
import fileinput
import math

logger = logging.getLogger('s3-to-minio')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

class Main():

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def stop_jmeter_jobs():
        try:
            os.system("kubectl delete --ignore-not-found jobs -l jobgroup=jmeter")
            os.system("kubectl delete --ignore-not-found secret jmeterconf")
            os.system("kubectl delete --ignore-not-found secret filesconf")
        except Exception as e:
            logger.info(e)
            exit(1)

    @staticmethod
    def main(argv):
        Main.log_level(LOG_LEVEL)
        Main.stop_jmeter_jobs()

if __name__ == "__main__":
    Main.main(sys.argv[1:])