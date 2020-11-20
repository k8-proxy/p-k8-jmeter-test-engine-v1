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

logger = logging.getLogger('delete_stack')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

class Main():

    prefix = 'demo'

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def stop_jmeter_jobs():
        try:
            os.system("kubectl delete --ignore-not-found jobs -l jobgroup=" + Main.prefix + "-jmeter")
            os.system("kubectl delete --ignore-not-found secret jmeterconf")
            os.system("kubectl delete --ignore-not-found secret filesconf")
        except Exception as e:
            logger.info(e)
            exit(1)

    @staticmethod
    def main(argv):
        help_string = 'python3 delete_stack.py --prefix <job prefix>'
        try:
            opts, args = getopt.getopt(argv,"hp:",["help=","prefix="])
        except getopt.GetoptError:
            print (help_string)
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h','--help'):
                print (help_string)
                sys.exit()
            elif opt in ('-p', '--prefix'):
                Main.prefix = arg

        Main.log_level(LOG_LEVEL)
        logger.info(Main.prefix)
        Main.stop_jmeter_jobs()

if __name__ == "__main__":
    Main.main(sys.argv[1:])