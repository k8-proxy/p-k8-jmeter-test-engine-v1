#!/bin/bash

echo "START Running on `date`"

rm -f /p-k8-jmeter-test-engine/jmeter-icap/scripts/config.env
cp /config/config.env /p-k8-jmeter-test-engine/jmeter-icap/scripts

export KUBECONFIG=/config/kube-config

exec /usr/sbin/init