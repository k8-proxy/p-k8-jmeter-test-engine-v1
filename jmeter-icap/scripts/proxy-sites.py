import os
import logging
import sys, getopt
import csv
import re

logger = logging.getLogger('proxy-sites')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

class Main():

    file_path = ''
    domains = set()

    @staticmethod
    def verify_csv_file():
        if not os.path.exists(Main.file_path):
            print("File {} does not exist".format(Main.file_path))
            exit(1)

    @staticmethod
    def get_domains():
        with open(Main.file_path, newline='') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',')
            for row in filereader:
                if Main.isValidDomain(row[0]):
                    if not row[0] in Main.domains:
                        Main.domains.add(row[0])
                        print(row[0])

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
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def main(argv):
        help_string = 'python3 proxy-sites.py -p <csv file path>'
        try:
            opts, args = getopt.getopt(argv,"hp:",["help=","path="])
        except getopt.GetoptError:
            print (help_string)
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h','--help'):
                print (help_string)
                sys.exit()
            elif opt in ('-p', '--path'):
                Main.file_path = arg

        Main.log_level(LOG_LEVEL)
        logger.info('path    {}'.format(Main.file_path))
        Main.verify_csv_file()
        Main.get_domains()

if __name__ == "__main__":
    Main.main(sys.argv[1:])