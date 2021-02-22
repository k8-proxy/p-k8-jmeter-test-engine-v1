#!/bin/bash

echo "START Running on `date`"

rm -f /p-k8-jmeter-test-engine/jmeter-icap/scripts/config.env
cp /config/config.env /p-k8-jmeter-test-engine/jmeter-icap/scripts

exec /usr/sbin/init