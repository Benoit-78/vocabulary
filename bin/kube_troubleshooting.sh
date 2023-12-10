minikube ip

minikube tunnel

k config set-context --current --namespace=vocabulary

# ========================================
#  T R O U B L E S H O O T I N G
# ========================================
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