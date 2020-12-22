cd /p-k8-jmeter-test-engine/UI/master-script-form
sudo npm install
cd /p-k8-jmeter-test-engine/UI/master-script-form
sudo ng build --prod
sudo cp -a /p-k8-jmeter-test-engine/UI/master-script-form/dist/master-script-form/. /var/www/html/
cd /p-k8-jmeter-test-engine/jmeter-icap/scripts
sudo chmod +x exec.sh
# sudo cp flask.service /etc/systemd/system/
sudo bash -c 'cat << EOF >> /etc/systemd/system/flask.service
[Unit]
Description=WSGI App for ICAP Testing UI Front End
After=network.target
[Service]
Type=simple
User=root
WorkingDirectory=/usr/glasswall/home/p-k8-jmeter-test-engine/jmeter-icap/scripts
ExecStart=/usr/glasswall/home/p-k8-jmeter-test-engine/scripts/exec.sh
Restart=always
[Install]
WantedBy=multi-user.target
EOF'
sudo systemctl daemon-reload
sudo systemctl enable flask
sudo systemctl start flask
sudo systemctl status flask

