from kubernetes import client, config

CURRENT_CONTEXT = "jmeter-k8-eu" #Current context value can be fetched through (cat ~/.kube/config | grep current-context)
NAMESPACE = "default" #Namespace where deployment is created
DEPLOYMENT_NAME = "minio" #Deployment Name

def main():
    config.load_kube_config(context=CURRENT_CONTEXT)
    k8s_apps_v1 = client.AppsV1Api()

    try:
        delete_resp = k8s_apps_v1.delete_namespaced_deployment(
            name=DEPLOYMENT_NAME,
            namespace=NAMESPACE,
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=5))
        print("Deployment deleted. status='%s'" % str(delete_resp.status))
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()
