# KUBERNETES (K8S)

Kubernetes automates the deployment, scaling, and management of containerized applications.

say we have 4 pods, k8s will make sure that all 4 pods are running and if one of them dies, it will create a new one, eliminating the need of creating a new one manually.

say you have a load balancer and you receive high traffic and hence want to add an extra pod, just run `kubectl scale deployment --replicas=6 service` to scale and conffigure the load balancer to route traffic to the new pod.