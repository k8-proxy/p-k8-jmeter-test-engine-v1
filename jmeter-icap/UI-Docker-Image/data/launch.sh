#!/bin/bash
# Inspired from https://github.com/hhcordero/docker-jmeter-client
# Basically runs jmeter, assuming the PATH is set to point to JMeter bin-dir (see Dockerfile)
#
# This script expects the standdard JMeter command parameters.
#

#set -e
#freeMem=`awk '/MemFree/ { print int($2/1024) }' /proc/meminfo`

#T_DIR=/usr/share/Test
#R_DIR=${T_DIR}/report
#rm -rf ${R_DIR} > /dev/null 2>&1
#mkdir -p ${R_DIR}

echo "START Running on `date`"
#echo "JVM_ARGS=${JVM_ARGS}"

#tail -f ${R_DIR}/jmeter.log &

#python3 /usr/share/Test/py/upload-jmeter-log.py -l /usr/share/Test/report/jmeter.log -j /usr/share/jmx/jmeter-conf.jmx

while true
do
	sleep 1
done