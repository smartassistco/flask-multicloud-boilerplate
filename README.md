Another simple demo of a Flask web server that talks to a queue consumer.
It is deployed using Kubernetes and Docker.

# App Description
The App is a simple Crud API for 'Tasks'.
When you POST to create a task, an event is generated and pushed to the queue.
The consumer consumes this and updates the status of the task after a random delay.
Requeuing and the final status update after that is also done.

Demo API docs are at
```
{HOST}:5000/apidocs
```
# Performing Demo
### Installation
Install and run docker. You may optionally install docker-compose as well.

Install and run microk8s

`microk8s.enable dashboard dns ingress registry`
### Build the images

Git clone.

We build the images and push it to the local microk8s registry.

##### Build the server.
```
docker build -f backend/Dockerfile -t kubernetes_demo_backend .
docker tag kubernetes_demo_backend localhost:32000/kubernetes_demo_backend
docker push localhost:32000/kubernetes_demo_backend
```

##### Build the consumer
```
docker build -f consumer/Dockerfile -t kubernetes_demo_consumer .
docker tag kubernetes_demo_consumer localhost:32000/kubernetes_demo_consumer
docker push localhost:32000/kubernetes_demo_consumer
```
### Deploy
```
chmod +x deploy.sh
./deploy.sh
```
### Monitor and Interact
To access dashboard paste the Cluster IP on your browser
```
microk8s.kubectl get all --all-namespaces | grep "service/kubernetes-dashboard"
```

Get Token to Login
```
token=$(microk8s.kubectl -n kube-system get secret | grep default-token | cut -d " " -f1)
microk8s.kubectl -n kube-system describe secret $token
```
To interact and use the API you need the HOST IP
```
microk8s.kubectl get all --all-namespaces | grep "service/backend"
```
API docs are at
```
{ABOVE_CLUSTER_IP}:5000/apidocs
```

# ToDo
* Writing of Tests.
* Demo with Volumes and Secrets for Datastores.

# Testing
Writing of test cases is left to be done.

# Support Or Contact
Reach out to us at:

abhishek@smartassist.tech

stallon@smartassist.tech

# Author
Abhishek Jebaraj

abhishekjebaraj@outlook.com
