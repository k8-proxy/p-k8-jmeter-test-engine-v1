#!/bin/bash

repo_url="https://github.com/k8-proxy/p-k8-jmeter-test-engine.git"

if git remote -v | grep upstream | grep $repo_url; then
    echo "ustream is there"
else
    echo "ustream is NOT there"
    exit 1
fi

git checkout master
git pull upstream master

sudo python3 ./jmeter-icap/HealthCheck/pyCheck.py