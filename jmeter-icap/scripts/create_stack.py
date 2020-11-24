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
    requests_memory = '768'
    requests_cpu = '300'
    limits_memory = '768'
    limits_cpu = '500'
    Xms_value = '512'
    Xmx_value = '512'
    parallelism = 1
    microk8s = False

    @staticmethod
    def get_microk8s():
        try:
            subprocess.call(["microk8s", "kubectl", "version"])
            Main.microk8s = True
        except:
            Main.microk8s = False    

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def verify_url(service_name, url):
        try:
            if not (url.startswith('http://') or url.startswith('https://')):
                logger.error("{} url must srart with \'http://\' or \'https://\'".format(service_name))
                exit(1)
            port = int(url.split(':', 2)[2])
            if not (port > 0 and port < 0xffff):
                logger.error("{} url must contain a valid port number".format(service_name))
                exit(1)
        except Exception as e:
            logger.error("{} URL vertification failed {}".format(service_name, e))
            exit(1)

    @staticmethod
    def sanity_checks():
        try:
            if not Main.microk8s:
                subprocess.call(["kubectl", "version"])
        except Exception as e:
            logger.error("failed to run kubectl: {}".format(e))
            exit(1)
        if int(Main.total_users) <= 0:
            logger.error("Total users must be positive number")
            exit(1)
        if int(Main.users_per_instance) <= 0:
            logger.error("Users per instance must be positive number")
            exit(1)
        if int(Main.users_per_instance) > 200:
            logger.error("Users per instance cannot be greater than 200")
            exit(1)
        if int(Main.duration) <= 0:
            logger.error("Test duration must be positive number")
            exit(1)
        if not os.path.exists(Main.filelist):
            logger.error("File {} does not exist".format(Main.filelist))
            exit(1)
        Main.verify_url('minio', Main.minio_url)
        Main.verify_url('influxdb', Main.influxdb_url)

    @staticmethod
    def stop_jmeter_jobs():
        try:
            if Main.microk8s:
                os.system("microk8s kubectl delete --ignore-not-found jobs -l jobgroup=" + Main.prefix + "-jmeter")
                os.system("microk8s kubectl delete --ignore-not-found secret jmeterconf")
                os.system("microk8s kubectl delete --ignore-not-found secret filesconf")
            else:
                os.system("kubectl delete --ignore-not-found jobs -l jobgroup=" + Main.prefix + "-jmeter")
                os.system("kubectl delete --ignore-not-found secret jmeterconf")
                os.system("kubectl delete --ignore-not-found secret filesconf")
        except Exception as e:
            logger.error(e)
            exit(1)

    @staticmethod
    def replace_in_file(filename, prev_str, new_str):
        try:
            with fileinput.FileInput(filename, inplace=True, backup='.bak') as file:
                for line in file:
                    print(line.replace(prev_str, new_str), end='')
            os.remove(filename + '.bak')
        except Exception as e:
            logger.error(e)
            exit(1)

    @staticmethod
    def get_jmx_file():
        try:
            a = uuid.uuid4()
            jmeter_script_name = str(a)
            shutil.copyfile("ICAP_Direct_FileProcessing_k8_v1.jmx",jmeter_script_name)
            Main.replace_in_file(jmeter_script_name,"$number_of_threads$", Main.users_per_instance)
            Main.replace_in_file(jmeter_script_name,"$duration_in_seconds$", Main.duration)
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
            logger.error(e)
            exit(1)

    @staticmethod
    def apply_resource_table():
        try:
            if int(Main.users_per_instance) <= 50:
                Main.requests_memory = '768'
                Main.requests_cpu = '300'
                Main.limits_memory = '768'
                Main.limits_cpu = '500'
                Main.Xms_value = '512'
                Main.Xmx_value = '512'
                return
            if int(Main.users_per_instance) <= 100:
                Main.requests_memory = '1280'
                Main.requests_cpu = '600'
                Main.limits_memory = '1280'
                Main.limits_cpu = '1000'
                Main.Xms_value = '1024'
                Main.Xmx_value = '1024'
                return
            if int(Main.users_per_instance) <= 200:
                Main.requests_memory = '2304'
                Main.requests_cpu = '1200'
                Main.limits_memory = '2304'
                Main.limits_cpu = '2000'
                Main.Xms_value = '2048'
                Main.Xmx_value = '2048'
                return
        except Exception as e:
            logger.error(e)
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

            if Main.microk8s:
                os.system("microk8s kubectl create secret generic jmeterconf --from-file=jmeter-conf.jmx")
                os.system("microk8s kubectl create secret generic filesconf --from-file=files")
            else:
                os.system("kubectl create secret generic jmeterconf --from-file=jmeter-conf.jmx")
                os.system("kubectl create secret generic filesconf --from-file=files")

            if os.path.exists('job-0.yaml'):
                os.remove('job-0.yaml')

            shutil.copyfile('jmeter-job-tmpl.yaml','job-0.yaml')

            Main.parallelism = math.ceil(int(Main.total_users) / int(Main.users_per_instance))
            logger.info("Number of pods to be created: {}".format(Main.parallelism))
            Main.replace_in_file('job-0.yaml','$parallelism-number', str(Main.parallelism))

            Main.apply_resource_table()
            Main.replace_in_file('job-0.yaml','$requests_memory$', Main.requests_memory)
            Main.replace_in_file('job-0.yaml','$requests_cpu$', Main.requests_cpu)
            Main.replace_in_file('job-0.yaml','$limits_memory$', Main.limits_memory)
            Main.replace_in_file('job-0.yaml','$limits_cpu$', Main.limits_cpu)
            Main.replace_in_file('job-0.yaml','$Xms_value$', Main.Xms_value)
            Main.replace_in_file('job-0.yaml','$Xmx_value$', Main.Xmx_value)

            Main.replace_in_file('job-0.yaml','$prefix$', Main.prefix)

            if Main.microk8s:
                os.system("microk8s kubectl create -f job-0.yaml")
            else:
                os.system("kubectl create -f job-0.yaml")

            os.remove('jmeter-conf.jmx')
            os.remove('files')
            os.remove('job-0.yaml')

        except Exception as e:
            logger.error(e)
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
        logger.info("TOTAL USERS         {}".format(Main.total_users))
        logger.info("USERS PER INSTANCE  {}".format(Main.users_per_instance))
        logger.info("TEST DURATION       {}".format(Main.duration))
        logger.info("FILE LIST           {}".format(Main.filelist))

        Main.minio_access_key = Main.minio_access_key.replace('&','&amp;')
        Main.minio_secret_key = Main.minio_secret_key.replace('&','&amp;')
        logger.info("MINIO URL           {}".format(Main.minio_url))
        #logger.info("MINIO ACCESS KEY    {}".format(Main.minio_access_key))
        #logger.info("MINIO SECRET KEY    {}".format(Main.minio_secret_key))
        logger.info("MINIO INPUT BUCKET  {}".format(Main.minio_input_bucket))
        logger.info("MINIO outPUT BUCKET {}".format(Main.minio_output_bucket))

        Main.influxHost = Main.influxdb_url.replace('http://', '')
        Main.influxHost = Main.influxHost.split(':', 1)[0]
        logger.info("INFLUXDB URL        {}".format(Main.influxdb_url))
        logger.info("INFLUX HOST         {}".format(Main.influxHost))
        logger.info("PREFIX              {}".format(Main.prefix))

        logger.info("ICAP SERVER         {}".format(Main.icap_server))

        Main.get_microk8s()
        logger.info("Micro k8s           {}".format(Main.microk8s))

        Main.sanity_checks()
        Main.stop_jmeter_jobs()
        Main.start_jmeter_job()

if __name__ == "__main__":
    Main.main(sys.argv[1:])