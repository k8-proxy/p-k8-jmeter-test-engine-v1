#Installing microk8s 
sudo snap install microk8s --classic
microk8s status --wait-ready
# alias kubectl='microk8s kubectl'
#Install helm
curl -LO https://git.io/get_helm.sh
chmod 700 get_helm.sh
./get_helm.sh
helm init
helm repo add stable https://charts.helm.sh/stable
helm repo update
# cd ~/p-k8-jmeter-test-engine/deployment/helm-charts/common-resources
# helm dependency update
helm upgrade --install common ./helm-charts/common-resources/ -f ./helm-charts/common-resources/local.yaml  --namespace common