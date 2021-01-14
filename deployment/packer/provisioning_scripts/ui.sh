#Install Node.js
sudo apt update
sudo apt install jq nodejs npm -y
sudo npm install -g @angular/cli
sudo npm install -g http-server
#Install python
sudo apt install -y python3-pip
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
sudo apt update
sudo apt install apache2 -y
sudo systemctl status apache2
sudo systemctl enable apache2
sudo mkdir /opt/git
cd /opt/git
sudo git clone https://github.com/k8-proxy/p-k8-jmeter-test-engine.git
cd p-k8-jmeter-test-engine/jmeter-icap/scripts
sudo pip3 install -r requirements.txt
cd /opt/git/p-k8-jmeter-test-engine/UI/master-script-form
sudo npm install
sudo ng build --prod
cd /opt/git
sudo cp -a p-k8-jmeter-test-engine/UI/master-script-form/dist/master-script-form/. /var/www/html/
cd /opt/git/p-k8-jmeter-test-engine/jmeter-icap/scripts
sudo chmod +x exec.sh
#sudo cp flask.service /etc/systemd/system/
sudo bash -c 'cat << EOF >> /etc/systemd/system/flask.service
[Unit]
Description=WSGI App for ICAP Testing UI Front End
After=network.target
[Service]
Type=simple
User=root
WorkingDirectory=/opt/git/p-k8-jmeter-test-engine/jmeter-icap/scripts
ExecStart=/opt/git/p-k8-jmeter-test-engine/jmeter-icap/scripts/exec.sh
Restart=always
[Install]
WantedBy=multi-user.target
EOF'
sudo cat /etc/systemd/system/flask.service
sudo systemctl daemon-reload
sudo systemctl enable flask
sudo systemctl start flask
sleep 10
sudo systemctl status flask