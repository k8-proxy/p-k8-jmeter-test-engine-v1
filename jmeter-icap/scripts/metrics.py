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

        print('Metrics module initialization PASSED')

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
    def count_query(prefix, start, finish, condition):
        try:
            str_query = 'SELECT COUNT("avg") FROM '\
                    + prefix + '_jmetericap WHERE '\
                    + ' time >= \'' + start + '\' AND ' \
                    + ' time <= \'' + finish + '\' AND '\
                    + condition \
                    + ';'
            #print (str_query)
            rs = Main.jmeter_db_client.query(str_query)
            points = rs.get_points()
            for item in points:
                count = item['count']
                if count:
                    return count
            return 0
        except Exception as e:
            print(e)
            exit(1)

    @staticmethod
    def total_reguests(prefix, start, finish):
        return Main.count_query(prefix, start, finish, ' transaction =~ /ICAP-Document-Process/')

    @staticmethod
    def failed_reguests(prefix, start, finish):
        return Main.count_query(prefix, start, finish, ' transaction =~ /ICAP-Document-Process/ AND statut=\'ko\'')

    @staticmethod
    def successful_reguests(prefix, start, finish):
        return Main.count_query(prefix, start, finish, ' transaction =~ /ICAP-Document-Process/ AND statut=\'ok\'')

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
        #print("host name - {}".format(Main.hostname))
        #print("host port - {}".format(Main.hostport))

        Main.init()

        prefix = 'demo'
        start_time = Main.initial_time(prefix)
        finish_time = Main.final_time(prefix)
        print('Initial time {}'.format(start_time))
        print('Final time {}'.format(finish_time))
        print('Total requests {}'.format(Main.total_reguests(prefix, start_time, finish_time)))
        print('Failed requests {}'.format(Main.failed_reguests(prefix, start_time, finish_time)))
        print('Successfull requests {}'.format(Main.successful_reguests(prefix, start_time, finish_time)))

if __name__ == "__main__":
    Main.main(sys.argv[1:])