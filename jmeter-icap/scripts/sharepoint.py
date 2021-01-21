import os
import logging
import sys, getopt
import csv
import re
import yaml
from config_params import Config

logger = logging.getLogger('sharepoint')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

class Sharepoint():

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
        if not Sharepoint.config_copy.sharepoint_host_names:
            return
        domain_list = Sharepoint.config_copy.sharepoint_host_names.split(' ')
        for item in domain_list:
            if Sharepoint.isValidDomain(item):
                Sharepoint.domains.add(item)

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
        if len(Sharepoint.domains) == 0:
            return

        try:
            with open(Sharepoint.yaml_file, 'r') as file:
                data = yaml.load(file, Loader=yaml.FullLoader)

                if 'hostAliases' in data['spec']['template']['spec'].keys():
                    new_entry = {'ip': Sharepoint.config_copy.sharepoint_ip, 'hostnames': list(Sharepoint.domains)}
                    data['spec']['template']['spec']['hostAliases'].append(new_entry)
                else:
                    hostAliases = {
                        'hostAliases': [{'ip': Sharepoint.config_copy.sharepoint_ip, 'hostnames': list(Sharepoint.domains)}]
                    }
                    data['spec']['template']['spec'].update(hostAliases)

                with open(Sharepoint.yaml_file, "w") as yaml_file:
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

        Sharepoint.log_level(LOG_LEVEL)
        Sharepoint.verify_file(yaml_file)
        Sharepoint.yaml_file = yaml_file
        Sharepoint.config_copy = config
        Sharepoint.get_domains()
        Sharepoint.update_yaml()

if __name__ == "__main__":
    Sharepoint.main(Config(), 'jmeter-job-tmpl copy.yaml')
    Sharepoint.main(Config(), 'jmeter-proxy-job-tmpl copy.yaml')