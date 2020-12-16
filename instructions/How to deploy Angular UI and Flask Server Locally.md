# Angular UI Component Local Installation and Deployment

## Introduction

This document outlines how to set up and run the Angular UI front end and Flask back end on any machine. This would typically be done for testing this software during development and not recommended for production use.

## Prerequisites

The project repository should be cloned locally

For windows:

Python and Node.js must be installed.

[Download and install Python from here.](https://www.python.org/downloads/)

[Download and install Node.js from here.](https://nodejs.org/en/download/) Click on the Windows Installer button to begin download of the msi installer. If download does not automatically begin, choose an option (32-bit or 64-bit) depending on your operating system. If unsure, choose 32-bit.

On Linux systems:

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

With the back end running, the front end UI will be able to send test execution requests to it. The backend scripts will still rely on values from the config.env file, so those will need to be tweaked depending on what is required (i.e. including a Grafana API key, the URL to Grafana installation, etc). To read more about the Config.env file and the parameters it accepts, refer to the section titled [Using config.env to pass parameters to create_stack_dash.py](https://github.com/k8-proxy/p-k8-jmeter-test-engine/blob/master/instructions/How%20to%20use%20k8%20test%20engine%20using%20create_stack_dash.py.md)
