import os
import logging
import sys, getopt
import json
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
    def initial_time(prefix):
        rs = Main.jmeter_db_client.query('SELECT FIRST("avg") FROM ' + prefix + '_jmetericap;')
        points = rs.get_points()
        for item in points:
            time = item['time']
            if time:
                return time
        print('Error getting initial time')
        exit(1)

    @staticmethod
    def final_time(prefix):
        try:
            rs = Main.jmeter_db_client.query('SELECT LAST("avg") FROM ' + prefix + '_jmetericap;')
            points = rs.get_points()
            for item in points:
                time = item['time']
                if time:
                    return time
            print('Error getting initial time')
        except Exception as e:
            print(e)
            exit(1)

    @staticmethod
    def record_count(prefix):
        try:
            rs = Main.jmeter_db_client.query('SELECT LAST("avg") FROM ' + prefix + '_jmetericap;')
            points = rs.get_points()
            for item in points:
                time = item['time']
                if time:
                    return time
            print('Error getting initial time')
        except Exception as e:
            print(e)
            exit(1)
 
    @staticmethod
    def total_reguests(prefix):
        try:
            rs = Main.jmeter_db_client.query('SELECT COUNT("avg") FROM ' + prefix + '_jmetericap WHERE transaction =~ /ICAP-Document-Process/;')
            points = rs.get_points()
            for item in points:
                count = item['count']
                if count:
                    return count
            print('Error getting total number of requests')
        except Exception as e:
            print(e)
            exit(1)

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

        print('Initial time {}'.format(Main.initial_time('demo')))
        print('Final time {}'.format(Main.final_time('demo')))
        print('Total requests {}'.format(Main.total_reguests('demo')))

if __name__ == "__main__":
    Main.main(sys.argv[1:])