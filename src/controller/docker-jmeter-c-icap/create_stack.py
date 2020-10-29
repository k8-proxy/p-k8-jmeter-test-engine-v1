import os
import logging
import sys, getopt
import time
import uuid
import platform
import subprocess

logger = logging.getLogger('s3-to-minio')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()


class Main():

    total_users = 0
    users_per_instance = 0
    duration  = 0

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def sanity_checks():
        try:
            subprocess.call(["kubectl", "get", "pods"])
        except OSError as e:
            if e.errno == errno.ENOENT:
                logger.error("kubectl is not installed on the system")
                exit(1)
            else:
                logger.error("failed to run kubectl")
                exit(1)

    @staticmethod
    def run_it():
        try:
            os.system("PowerShell -ExecutionPolicy ByPass -File run.ps1 ICAP-POC_s3.jmx files.txt 1")
        except Exception as e:
            logger.info(e)

    @staticmethod
    def main(argv):
        help_string = 'create_stack.py --total_users <number of users> --users_per_instance <number of users> --duration <test duaration>'
        try:
            opts, args = getopt.getopt(argv,"ht:u:d:",["total_users=","users_per_instance=","duration="])
        except getopt.GetoptError:
            print (help_string)
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print (help_string)
                sys.exit()
            elif opt in ("-t", "--total_users"):
                Main.total_users = arg
            elif opt in ("-u", "--users_per_instance"):
                Main.users_per_instance = arg
            elif opt in ("-d", "--duration"):
                Main.duration = arg

        Main.log_level(LOG_LEVEL)
        logger.info(Main.total_users)
        logger.info(Main.users_per_instance)
        logger.info(Main.duration)

        Main.sanity_checks()
        Main.run_it()

if __name__ == "__main__":
    Main.main(sys.argv[1:])