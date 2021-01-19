import os
import logging
import sys, getopt
import csv
import re
import yaml
from config_params import Config

logger = logging.getLogger('sharepoint')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

class Main():

    yaml_file = ''
    domains = set()
    config_copy = Config()

    @staticmethod
    def verify_file(file):
        if not os.path.exists(file):
            print("File {} does not exist".format(file))
            exit(1)

    @staticmethod
    def get_domains():
        if not Main.config_copy.sharepoint_host_names:
            return
        domain_list = Main.config_copy.sharepoint_host_names.split(' ')
        for item in domain_list:
            if Main.isValidDomain(item):
                Main.domains.add(item)

    @staticmethod
    def isValidDomain(str):
    
        # Regex to check valid 
        # domain name.  
        regex = "^((?!-)[A-Za-z0-9-]" + \
                "{1,63}(?<!-)\\.)" + \
                "+[A-Za-z]{2,6}"
        
        # Compile the ReGex
        p = re.compile(regex)
    
        # If the string is empty 
        # return false
        if (str == None):
            return False
    
        # Return if the string 
        # matched the ReGex
        if(re.search(p, str)):
            return True
        else:
            return False

    @staticmethod
    def update_yaml():
        # check if there are valid domains in the set
        if len(Main.domains) == 0:
            return

        try:
            with open(Main.yaml_file, 'r') as file:
                data = yaml.load(file, Loader=yaml.FullLoader)

                hostAliases = {
                    'hostAliases': [{'ip': Main.config_copy.sharepoint_ip, 'hostnames': list(Main.domains)}]
                }

                #print(data['spec']['template']['spec'])
                #print('\n\n')
                data['spec']['template']['spec'].update(hostAliases)
                #print(data['spec']['template']['spec'])

                with open(Main.yaml_file, "w") as yaml_file:
                    yaml.dump(data, yaml_file)

        except Exception as e:
            print(e)

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def main(config, yaml_file):

        if not config.sharepoint_ip:
            return

        if not config.sharepoint_host_names:
            return

        Main.log_level(LOG_LEVEL)
        #print("{}".format(config.sharepoint_ip))        
        #print("{}".format(config.sharepoint_host_names))    
        Main.verify_file(yaml_file)
        Main.yaml_file = yaml_file
        Main.config_copy = config
        Main.get_domains()
        Main.update_yaml()

if __name__ == "__main__":
    Main.main(Config(), 'job-0.yaml')
    #Main.main(Config(), 'jmeter-proxy-job-tmpl.yaml')