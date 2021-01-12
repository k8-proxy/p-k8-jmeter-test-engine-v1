import os
import logging
import sys, getopt
from influxdb import InfluxDBClient

logger = logging.getLogger('proxy-sites')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

class Main():

    hostname = ''
    hostport = ''
    jmeter_db_client = ''
    icapserver_db_client = ''
    proxysite_db_client = ''

    @staticmethod
    def verify_database(db):
        try:
            db.query('SHOW RETENTION POLICIES;')
        except Exception as e:
            print(e)
            exit(1)

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def init():
        Main.jmeter_db_client = InfluxDBClient(Main.hostname, Main.hostport, database='jmeter')
        Main.verify_database(Main.jmeter_db_client)

        Main.icapserver_db_client = InfluxDBClient(Main.hostname, Main.hostport, database='icapserver')
        Main.verify_database(Main.icapserver_db_client)

        Main.proxysite_db_client = InfluxDBClient(Main.hostname, Main.hostport, database='proxysite')
        Main.verify_database(Main.proxysite_db_client)

        print('Initialization Passed')

    @staticmethod
    def main(argv):
        help_string = 'python3 metrics.py -n <host name> -p <host port>'
        try:
            opts, args = getopt.getopt(argv,"hn:p:",["name=","port="])
        except getopt.GetoptError:
            print (help_string)
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h','--help'):
                print (help_string)
                sys.exit()
            elif opt in ('-n', '--name'):
                Main.hostname = arg
            elif opt in ('-p', '--port'):
                Main.hostport = arg

        Main.log_level(LOG_LEVEL)
        print("host name - {}".format(Main.hostname))
        print("host port - {}".format(Main.hostport))

        Main.init()

if __name__ == "__main__":
    Main.main(sys.argv[1:])