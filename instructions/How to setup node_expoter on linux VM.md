## Steps

- Download `node_exporter` and extract the content to `bin` location.
  
  ```sh
  wget https://github.com/prometheus/node_exporter/releases/download/v1.0.1/node_exporter-1.0.1.linux-amd64.tar.gz
  tar -xvzf node_exporter-1.0.1.linux-amd64.tar.gz
  sudo mv node_exporter-1.0.1.linux-amd64/node_exporter /usr/local/bin/
  
  ```
 
- Add user to run it as a service and create service configuration file.

```sh
sudo useradd -rs /bin/false node_exporter
sudo cat << EOF >> /etc/prometheus/node_exporter.config
[Unit]
Description=Node Exporter
[Service]
User=node_exporter
EnvironmentFile=/etc/prometheus/node_exporter.config
ExecStart=/usr/sbin/node_exporter $OPTIONS
[Install]
WantedBy=multi-user.target
EOF

```

- Enable and start the service

```sh
sudo systemctl daemon-reload
sudo systemctl start node_exporter
sudo systemctl enable node_exporter
sudo systemctl status node_exporter
```
