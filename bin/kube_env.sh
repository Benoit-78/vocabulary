#!/bin/bash

minikube kubectl -- apply -f data/pv.yaml
minikube kubectl -- apply -f data/pvc.yaml

minikube kubectl -- apply -f front/service.yaml
minikube kubectl -- apply -f data/service.yaml

minikube kubectl -- apply -f data/deployment.yaml
minikube kubectl -- apply -f front/deployment.yaml

