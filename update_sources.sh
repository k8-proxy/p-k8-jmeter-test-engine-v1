#!/bin/bash

repo_url="https://github.com/k8-proxy/p-k8-jmeter-test-engine.git"

if git remote -v | grep upstream | grep $repo_url; then
    echo "ustream remote is present"
else
    echo "ustream remote is NOT there\nAdding upstream"
    git remote remove upstream
    git remote add upstream $repo_url
fi

git checkout master
git pull upstream master

sudo python3 ./jmeter-icap/HealthCheck/pyCheck.py