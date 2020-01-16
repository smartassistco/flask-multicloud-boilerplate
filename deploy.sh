#!/bin/bash

echo "Creating the Datastores deployment and service..."
microk8s.kubectl create -f ./kubernetes/rabbit/deployment.yml
microk8s.kubectl create -f ./kubernetes/rabbit/service.yml

microk8s.kubectl create -f ./kubernetes/mongo/deployment.yml
microk8s.kubectl create -f ./kubernetes/mongo/service.yml

echo "Creating the Backend deployment and service and the Consumer deployment..."

microk8s.kubectl create -f ./kubernetes/backend/deployment.yml
microk8s.kubectl create -f ./kubernetes/backend/service.yml

microk8s.kubectl create -f ./kubernetes/consumer/deployment.yml
