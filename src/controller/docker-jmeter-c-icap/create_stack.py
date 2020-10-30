import os
import logging
import sys, getopt
import time
import uuid
import platform
import subprocess
import shutil
import fileinput

logger = logging.getLogger('s3-to-minio')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()


class Main():

    total_users = -1
    users_per_instance = -1
    duration = -1
    filelist = ''

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

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
    def get_jmx_file():
        try:
            a = uuid.uuid4()
            jmeter_script_name = str(a)
            shutil.copyfile("ICAP-POC_tmpl.jmx",jmeter_script_name)
            with fileinput.FileInput(jmeter_script_name, inplace=True, backup='.bak0') as file:
                for line in file:
                    print(line.replace("\"ThreadGroup.num_threads\">$NO</stringProp>", "\"ThreadGroup.num_threads\">"+ Main.users_per_instance +"</stringProp>"), end='')
            with fileinput.FileInput(jmeter_script_name, inplace=True, backup='.bak1') as file:
                for line in file:
                    print(line.replace("${__P(p_duration,$NO)}", "${__P(p_duration,"+ Main.duration +")}"), end='')
            os.remove(jmeter_script_name + '.bak0')
            os.remove(jmeter_script_name + '.bak1')
            return jmeter_script_name
        except Exception as e:
            logger.info(e)
            exit(1)

    @staticmethod
    def run_it():
        try:
            jmeter_script_name = Main.get_jmx_file()
            os.system("PowerShell -ExecutionPolicy ByPass -File run.ps1 " + jmeter_script_name + " " + Main.filelist + " 1")
            os.remove(jmeter_script_name)
        except Exception as e:
            logger.info(e)

    @staticmethod
    def main(argv):
        help_string = 'python3 create_stack.py --total_users <number of users> --users_per_instance <number of users> --duration <test duaration> --list <file list>'
        try:
            opts, args = getopt.getopt(argv,"ht:u:d:l:",["total_users=","users_per_instance=","duration=","list="])
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

        Main.log_level(LOG_LEVEL)
        logger.info(Main.total_users)
        logger.info(Main.users_per_instance)
        logger.info(Main.duration)
        logger.info(Main.filelist)

        Main.sanity_checks()
        Main.stop_jmeter_jobs()
        Main.run_it()

if __name__ == "__main__":
    Main.main(sys.argv[1:])