#Install Node.js
sudo apt install nodejs -y
sudo apt install npm -y
sudo npm install -g @angular/cli
sudo npm install -g http-server
#Install python
sudo apt update
sudo apt -y upgrade
sudo apt install -y python3-pip
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
cd /p-k8-jmeter-test-engine/jmeter-icap/scripts
sudo pip3 install -r requirements.txt
