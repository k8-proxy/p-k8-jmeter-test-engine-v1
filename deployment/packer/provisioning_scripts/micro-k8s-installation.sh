#Installing microk8s
sudo apt update
sudo snap install microk8s --classic --channel=1.16/stable
sudo microk8s status --wait-ready
sudo microk8s start
sudo microk8s enable dns dashboard storage
sudo microk8s kubectl get all --all-namespaces
sleep 120
# alias kubectl='microk8s kubectl'
sudo snap install kubectl --classic
sudo mkdir ~/.kube
sudo bash -c 'microk8s config > ~/.kube/config'
sudo microk8s config
#Install helm
curl -LO https://git.io/get_helm.sh
chmod 700 get_helm.sh
./get_helm.sh
sudo helm init
sudo kubectl create serviceaccount --namespace kube-system tiller
sudo kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
sudo bash -c "helm init --service-account tiller --override spec.selector.matchLabels.'name'='tiller',spec.selector.matchLabels.'app'='helm' --output yaml | sed 's@apiVersion: extensions/v1beta1@apiVersion: apps/v1@' | kubectl apply -f -"
sleep 40
#helm repo add stable https://charts.helm.sh/stable
#helm repo update
cd /opt/git/p-k8-jmeter-test-engine/deployment/helm-charts/common-resources
sudo git checkout packer
sudo helm dependency update
cd ../../
sudo helm upgrade --install common ./helm-charts/common-resources/ -f ./helm-charts/common-resources/local.yaml  --namespace common