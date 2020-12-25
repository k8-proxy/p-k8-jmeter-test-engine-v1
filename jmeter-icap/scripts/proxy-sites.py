import os
import logging
import sys, getopt
import csv
import re
import yaml

logger = logging.getLogger('proxy-sites')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

class Main():

    file_path = ''
    yaml_file = ''
    domains = set()

    @staticmethod
    def verify_file(file):
        if not os.path.exists(file):
            print("File {} does not exist".format(file))
            exit(1)

    @staticmethod
    def get_domains():
        with open(Main.file_path, newline='') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',')
            for row in filereader:
                if Main.isValidDomain(row[0]):
                    if not row[0] in Main.domains:
                        Main.domains.add(row[0])

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
        try:
            with open(Main.yaml_file, 'r') as file:
                data = yaml.load(file, Loader=yaml.FullLoader)

                data['spec']['template']['spec']['hostAliases'][0]['hostnames'] = list(Main.domains)
                #print(data['spec']['template']['spec']['hostAliases'][0]['hostnames'])

                with open(Main.yaml_file, "w") as yaml_file:
                    yaml.dump(data, yaml_file)

        except Exception as e:
            print(e)

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def main(argv):
        help_string = 'python3 proxy-sites.py -p <csv file path> -m <yaml file>'
        try:
            opts, args = getopt.getopt(argv,"hp:m:",["help=","path=","yaml"])
        except getopt.GetoptError:
            print (help_string)
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h','--help'):
                print (help_string)
                sys.exit()
            elif opt in ('-p', '--path'):
                Main.file_path = arg
            elif opt in ('-m', '--yaml'):
                Main.yaml_file = arg

        Main.log_level(LOG_LEVEL)
        Main.verify_file(Main.file_path)
        Main.verify_file(Main.yaml_file)
        Main.get_domains()
        Main.update_yaml()

if __name__ == "__main__":
    Main.main(sys.argv[1:])