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

#import boto3
#import requests
#from botocore.client import Config
#from botocore.exceptions import ClientError

logger = logging.getLogger('create_stack')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()


class Main():

    total_users = '100'
    users_per_instance = '25'
    duration = '60'
    filelist = ''
    minio_url = 'http://minio.minio.svc.cluster.local:9000'
    minio_access_key = ''
    minio_secret_key = ''
    minio_input_bucket = 'input'
    minio_output_bucket = 'output'
    influxdb_url = 'http://influxdb.influxdb.svc.cluster.local:8086'
    influxHost = 'influxdb.influxdb.svc.cluster.local'
    prefix = 'demo'
    icap_server = 'icap02.glasswall-icap.com'

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def verify_minio_access():
        try:
            logger.info("verify_minio_access not implemented")
            #s3 = boto3.resource('s3', endpoint_url=Main.minio_url, aws_access_key_id=Main.minio_access_key,
            #                    aws_secret_access_key=Main.minio_secret_key, config=Config(signature_version='s3v4'))
            #if (s3.Bucket(Main.minio_input_bucket) in s3.buckets.all()) == False:
            #    logger.info('Bucket {} not Found'.format(Main.minio_input_bucket))
            #    exit(1)
        except Exception as e:
            logger.info(e)
            exit(1)


    @staticmethod
    def sanity_checks():
        try:
            subprocess.call(["kubectl", "version"])
        except OSError as e:
            if e.errno == errno.ENOENT:
                logger.error("kubectl is not installed on the system")
                exit(1)
            else:
                logger.error("failed to run kubectl")
                exit(1)
        if int(Main.total_users) <= 0:
            logger.error("Total users must be positive number")
            exit(1)
        if int(Main.users_per_instance) <= 0:
            logger.error("Users per instance must be positive number")
            exit(1)
        if int(Main.duration) <= 0:
            logger.error("Test duration must be positive number")
            exit(1)
        if not os.path.exists(Main.filelist):
            logger.error("File {} does not exist".format(Main.filelist))
            exit(1)
        Main.verify_minio_access()

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
    def replace_in_file(filename, prev_str, new_str):
        try:
            with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
                for line in file:
                    print(line.replace(prev_str, new_str), end='')
            os.remove(filename + '.bak')
        except Exception as e:
            logger.info(e)
            exit(1)

    @staticmethod
    def get_jmx_file():
        try:
            a = uuid.uuid4()
            jmeter_script_name = str(a)
            shutil.copyfile("ICAP-POC_tmpl.jmx",jmeter_script_name)
            Main.replace_in_file(jmeter_script_name,"\"ThreadGroup.num_threads\">$NO</stringProp>","\"ThreadGroup.num_threads\">"+ Main.users_per_instance +"</stringProp>")
            Main.replace_in_file(jmeter_script_name,"${__P(p_duration,$NO)}", "${__P(p_duration,"+ Main.duration +")}")
            Main.replace_in_file(jmeter_script_name,"$minio_endpoint$", Main.minio_url)
            Main.replace_in_file(jmeter_script_name,"$minio_access_key$", Main.minio_access_key)
            Main.replace_in_file(jmeter_script_name,"$minio_secret_key$", Main.minio_secret_key)
            Main.replace_in_file(jmeter_script_name,"$minio_input_bucket$", Main.minio_input_bucket)
            Main.replace_in_file(jmeter_script_name,"$minio_output_bucket$", Main.minio_output_bucket)
            Main.replace_in_file(jmeter_script_name,"$influxdb_url$", Main.influxdb_url)
            Main.replace_in_file(jmeter_script_name,"$influxHost$", Main.influxHost)
            Main.replace_in_file(jmeter_script_name,"$prefix$", Main.prefix)
            Main.replace_in_file(jmeter_script_name,"$icap_server$", Main.icap_server)
            return jmeter_script_name
        except Exception as e:
            logger.info(e)
            exit(1)

    @staticmethod
    def start_jmeter_job():
        try:
            if os.path.exists('jmeter-conf.jmx'):
                os.remove('jmeter-conf.jmx')

            jmeter_script_name = Main.get_jmx_file()
            shutil.copyfile(jmeter_script_name,'jmeter-conf.jmx')
            os.remove(jmeter_script_name)

            shutil.copyfile(Main.filelist,'files')

            os.system("kubectl create secret generic jmeterconf --from-file=jmeter-conf.jmx")
            os.system("kubectl create secret generic filesconf --from-file=files")

            if os.path.exists('job-0.yaml'):
                os.remove('job-0.yaml')

            shutil.copyfile('jmeter-job-tmpl.yaml','job-0.yaml')
            Main.replace_in_file('job-0.yaml','jmeterjob-$NO', 'jmeterjob-0')

            parallelism = math.ceil(int(Main.total_users) / int(Main.users_per_instance))
            logger.info("Number of pods to be created: {}".format(parallelism))
            Main.replace_in_file('job-0.yaml','$parallelism-number', str(parallelism))

            os.system("kubectl create -f job-0.yaml")

            os.remove('jmeter-conf.jmx')
            os.remove('files')
            os.remove('job-0.yaml')

        except Exception as e:
            logger.info(e)
            exit(1)

    @staticmethod
    def main(argv):
        help_string = 'python3 create_stack.py --total_users <number of users> --users_per_instance <number of users> --duration <test duaration> --list <file list> --minio_url <url> --minio_access_key <access key> --minio_secret_key <secret key> --minio_input_bucket <bucket name> --minio_output_bucket <bucket name> --influxdb_url <url> --prefix <prefix> --icap_server <url>'
        try:
            opts, args = getopt.getopt(argv,"htudl:ma:s:ibxpv",["total_users=","users_per_instance=","duration=","list=","minio_url=","minio_access_key=","minio_secret_key=", "minio_input_bucket=", "minio_output_bucket=","influxdb_url=","prefix=","icap_server="])
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
            elif opt in ("-l", "--list"):
                Main.filelist = arg
            elif opt in ("-m", "--minio_url"):
                Main.minio_url = arg
            elif opt in ("-a", "--minio_access_key"):
                Main.minio_access_key = arg
            elif opt in ("-s", "--minio_secret_key"):
                Main.minio_secret_key = arg
            elif opt in ("-i", "--minio_input_bucket"):
                Main.minio_input_bucket = arg
            elif opt in ("-o", "--minio_output_bucket"):
                Main.minio_output_bucket = arg
            elif opt in ("-x", "--influxdb_url"):
                Main.influxdb_url = arg
            elif opt in ("-p", "--prefix"):
                Main.prefix = arg
            elif opt in ("-v", "--icap_server"):
                Main.icap_server = arg

        Main.log_level(LOG_LEVEL)
        logger.info(Main.total_users)
        logger.info(Main.users_per_instance)
        logger.info(Main.duration)
        logger.info(Main.filelist)

        Main.minio_access_key = Main.minio_access_key.replace('&','&amp;')
        Main.minio_secret_key = Main.minio_secret_key.replace('&','&amp;')
        logger.info(Main.minio_url)
        logger.info(Main.minio_access_key)
        logger.info(Main.minio_secret_key)
        logger.info(Main.minio_input_bucket)
        logger.info(Main.minio_output_bucket)

        Main.influxHost = Main.influxdb_url.replace('http://', '')
        Main.influxHost = Main.influxHost.split(':', 1)[0]
        logger.info(Main.influxdb_url)
        logger.info(Main.influxHost)
        logger.info(Main.prefix)

        logger.info(Main.icap_server)

        Main.sanity_checks()
        Main.stop_jmeter_jobs()
        Main.start_jmeter_job()

if __name__ == "__main__":
    Main.main(sys.argv[1:])