from os import path
import yaml, json
import argparse
from kubernetes import client, config

parser = argparse.ArgumentParser(description="Numeber of Jmeter Threads")
parser.add_argument("-u", "--user", type=int, default=2, help="Enter number of users")
args = parser.parse_args()

FILE_NAME = "/home/addweb/python_script_pod_deploy/minio.yaml" #depllyment file name with path
CURRENT_CONTEXT = "jmeter-k8-eu" #Current context value can be fetched through (cat ~/.kube/config | grep current-context)
NAMESPACE = "default" #Namespace where deployment is created
DEPLOYMENT_NAME = "minio" #Deployment Name

def main():
    # Default Kube Config Location, Provide Current-Context name
    config.load_kube_config(context=CURRENT_CONTEXT)

    with open(FILE_NAME) as f:
        dep = yaml.safe_load(f)
        dep['metadata']['name'] = DEPLOYMENT_NAME
        dep['metadata']['namespace'] = NAMESPACE
        dep['spec']['replicas'] = args.user
        # print(dep)
        k8s_apps_v1 = client.AppsV1Api()

        # Create a deployment
        try:
            create_resp = k8s_apps_v1.create_namespaced_deployment(body=dep, namespace=NAMESPACE)
            print("Deployment created. status='%s'" % create_resp.metadata.name)
        # Update a deployment
        except:
            update_resp = k8s_apps_v1.patch_namespaced_deployment(body=dep, namespace=NAMESPACE, name=DEPLOYMENT_NAME)
            print("Deployment configured. status='%s'" % update_resp.metadata.name)


if __name__ == '__main__':
    main()