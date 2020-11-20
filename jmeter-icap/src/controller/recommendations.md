# Recommendations

## Docker Image Optimization

- Publishing base docker image to glasswallsolutions docker registry.

- Reduce layers to decrease the docker image size.

- Using multi-stage docker builds.

## k8s improvements

- Hosting glasswallsolutions official helm-chart open source repository. This will host all customized k8s deployments which can simply installed via helm package to any k8s cluster.

- Creating single helm chart instead of using independent yaml files for deployment.
