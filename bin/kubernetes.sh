#!/bin/bash


# ========================================
#  S E T T I N G S
# ========================================
k config set-context --current --namespace=vocabulary

k create secret docker-registry my-registry-secret \
    --docker-username=delormebenoit \
    --docker-password="Z]7Vm3XFK_Q8" \
    --docker-email=delormebenoit211@gmail.com \
    --docker-server=https://index.docker.io/v1/



# ========================================
#  D E P L O Y M E N T
# ========================================
minikube start

minikube kubectl -- apply -f data/pv.yaml
minikube kubectl -- apply -f data/pvc.yaml

minikube kubectl -- apply -f front/service.yaml
minikube kubectl -- apply -f data/service.yaml

minikube kubectl -- apply -f data/deployment.yaml
minikube kubectl -- apply -f front/deployment.yaml



# ========================================
#  T R O U B L E S H O O T I N G
# ========================================
minikube ip

minikube tunnel

k get pods <pod_name> -o yaml
k describe pods <resource_name>
k logs <pod_name> -c <container_name>
k exec -it <pod_name> -- bash

# Inside the pod
apt install curl
curl localhost



# ========================================
#  R E S O U R C E S
# ========================================
minikube addons enable metrics-server
k top node
k top pod
