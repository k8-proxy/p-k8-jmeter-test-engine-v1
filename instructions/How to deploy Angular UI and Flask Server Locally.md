# Angular UI Component Local Installation and Deployment

## Introduction

This document outlines how to set up and run the Angular UI front end and Flask back end on any machine. This would typically be done for testing this software during development and not recommended for production use.

## Prerequisites

The project repository should be cloned locally

Python and Node.js must be installed. On Windows systems these can be obtained from the [Python](https://www.python.org/downloads/) and [Node](https://nodejs.org/en/download/) websites respectively. On Linux systems, the following commands may be used:

Installing Node.js

```bash
sudo apt install nodejs -y
sudo apt install npm -y
sudo npm install -g @angular/cli
sudo npm install -g http-server
```
Installing python

```bash
sudo apt update
sudo apt -y upgrade
sudo apt install -y python3-pip
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
```

For back end, install Flask and dependencies. A requirements file is already set up and can be used to get the necessary packages. Navigate to folder and install:

On Windows:
```
cd Your_Github_Directory\p-k8-jmeter-test-engine\jmeter-icap\scripts
pip install -r requirements.txt
```

For Linux systems:
```
cd /opt/git/p-k8-jmeter-test-engine/jmeter-icap/scripts
sudo pip3 install -r requirements.txt
```



## Installing Front End Angular UI Component

Navigate to the UI folder and install the Angular project.

On Windows:
```
cd Your_Github_Directory\p-k8-jmeter-test-engine\UI\master-script-form
npm install
```

For Linux systems:
```
cd /opt/git/p-k8-jmeter-test-engine/UI/master-script-form
sudo npm install
```

To start up the front end server in order to run the UI, in the same directory use the following command:

```
ng serve
```
The UI can then be accessed via http://localhost:4200/.


## Running Back End Flask server

Navigate once more to the scripts folder in the repository and run the server using:

On Windows:
```
cd Your_Github_Directory\p-k8-jmeter-test-engine\jmeter-icap\scripts
python flask_server.py
```

For Linux systems:
```
cd /opt/git/p-k8-jmeter-test-engine/jmeter-icap/scripts
sudo python3 flask_server.py
```

With the back end running, the front end UI will be able to send test execution requests to it. The backend scripts will still rely on values from the config.env file, so those will need to be tweaked depending on what is required (i.e. including a Grafana API key, the URL to Grafana installation, etc).
