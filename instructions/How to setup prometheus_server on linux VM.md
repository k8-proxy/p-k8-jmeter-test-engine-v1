## Steps

- Create user `prometheus` and relevant folder structure.
  
  ```sh
  sudo useradd --no-create-home --shell /bin/false prometheus
  sudo mkdir /etc/prometheus
  sudo mkdir /var/lib/prometheus
  sudo chown prometheus:prometheus /etc/prometheus
  sudo chown prometheus:prometheus /var/lib/prometheus
  ```
- Download `prometheus` and extract
  
  ```sh
  wget wget https://github.com/prometheus/prometheus/releases/download/v2.23.0/prometheus-2.23.0.linux-amd64.tar.gz
  tar -xvzf prometheus-2.23.0.linux-amd64.tar.gz
  cd prometheus-2.23.0.linux-amd64/
  sudo cp prometheus /usr/local/bin/
  sudo cp promtool /usr/local/bin/
  sudo chown prometheus:prometheus /usr/local/bin/prometheus
  sudo chown prometheus:prometheus /usr/local/bin/promtool
  sudo cp -r consoles /etc/prometheus/
  sudo cp -r console_libraries/ /etc/prometheus/
  sudo cp prometheus.yml /etc/prometheus/prometheus.yml
  sudo chown -R prometheus:prometheus /etc/prometheus/

  
  ```
- Reference `prometheus.yaml` config file.

```sh
global:
  scrape_interval: 10s

scrape_configs:
  - job_name: 'prometheus'
    scrape_interval: 5s
    static_configs:
      - targets: ['localhost:9090']
  - job_name: 'prometheus_metrics'
    scrape_interval: 5s
    static_configs:
      - targets: ['localhost:9100']
  - job_name: 'icap_metrics'
    scrape_interval: 5s
    static_configs:
      - targets: ['91.109.25.70:9100', '91.109.25.76:9100', '91.109.25.78:9100']
  - job_name: 'ICAP-01'
    scrape_interval: 5s
    static_configs:
      - targets: ['91.109.25.76:32045']
        labels:
          clusterID: ICAP-01
  - job_name: 'ICAP-03'
    scrape_interval: 5s
    static_configs:
      - targets: ['91.109.25.70:32045']
        labels:
          clusterID: ICAP-03
```

- Add user to run it as a service and create service configuration file.

```sh

sudo cat << EOF >> /etc/systemd/system/prometheus.service
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
    --config.file /etc/prometheus/prometheus.yml \
    --storage.tsdb.path /var/lib/prometheus/ \
    --web.console.templates=/etc/prometheus/consoles \
    --web.console.libraries=/etc/prometheus/console_libraries

[Install]
WantedBy=multi-user.target
EOF

```

- Enable and start the service

```sh
  sudo systemctl start prometheus
  sudo systemctl enable prometheus
  sudo systemctl status prometheus
```
