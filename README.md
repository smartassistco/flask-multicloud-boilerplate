An easy to use cloud demo and boilerplate of a Flask API Server and a Queue Consumer. It includes a Postgres for the backend DB and Redis for the
Cache and Queue DB

Deployment instructions are provided to deploy to various cloud providers like DigitalOcean, AWS, Heroku etc.

It includes all the typical requirements of a simple but efficient boilerplate.
They are
* Application Monitoring with NewRelic.
* Logging and Exception handling with Sentry and NewRelic.
* Request Logging and Profiling with NewRelic.
* Security with API Keys. This can be seen during the Production Deployment
* Documentation. All APIs are documented with OpenAPI Specifications.
* ORM integration with SQLAlchemy.
* ORM and DB Migration/Versioning integration.
* Worker Queue Demo.
* Flask Admin (To be done next)
* Configuration and env variable management. To separate Production and Dev deployments
* Simple Serializers and Response Wrappers.

It also includes a Production like deployment for various cloud providers. The entire deployment is very simplified using
Infrastructure as Code best practices with Terraform by Hashicorp.
* DigitalOcean
* AWS (To be done next)
* Heroku (To be done next)


# App Description
The App is a simple Crud API for 'Tasks'.
When you POST to create a task, an event is generated and pushed to the queue.
The consumer consumes this and updates the status of the task after a random delay.
Requeuing and the final status update after that is also done.

Demo API docs are at
```
{HOST}:5000/apidocs
```
# Performing Demo Locally
### Installation
Install and run docker. Docker compose needs to be installed as well.

Git Clone. Pipenv is recommended below.
```
pipenv install
pipenv install -d
```
######OR
```
pip install -r requirements.txt
pip install -r requirements-dev.txt
```
### Get New Relic APM Key.
#####(Only for DigitalOcean deployment and if you want local monitoring)
This boiler plate uses New Relic for Application Monitoring. It has a free Lite Version.

You may register without a card at https://newrelic.com/signup?trial=apm

Find 'NEWRELIC_KEY' in the docker compose files. Replace the key with the above registered key in the compose files.

### Build and Run the server.

```cp -avR envs.example/ envs/```

After this step, do check and adjust if you wish the environment variables in the envs folder. All secrets/passwords etc
can be stored here instead of Git.

```docker-compose build && docker-compose up```

### Monitor and Interact
API docs are at
```localhost:5000/apidocs```

If you are using NewRelic APM, find the monitoring dashboard at

* Visit https://rpm.newrelic.com/accounts/
* Click on your registered account.
* Click on your application where the APM has been installed. 
* View metrics on the dashboard.

# Deploy to Cloud
### DigitalOcean

#####Deployment
Install Terraform from the instructions here https://computingforgeeks.com/how-to-install-terraform-on-ubuntu-centos-7/

Add your DO API Key in the file variables.tf. You also need to have added your credit card in DO. Find/Get your API Key here
https://cloud.digitalocean.com/account/security

Then
```
cd deploy/digitalocean
terraform init
terraform plan
terraform apply
```
Wait for around 10-12 seconds after terraform has finished creating the resources.

Copy the Server IP outputted from the above run.

Then run

```
export SERVER_IP={ABOVE SERVER IP}
ssh-keyscan -t rsa $SERVER_IP >> ~/.ssh/known_hosts
docker-compose -f docker-compose-prod.yml -H ssh://root@$SERVER_IP build
docker-compose -f docker-compose-prod.yml -H ssh://root@$SERVER_IP up
```

#####Troubleshooting:
Check the public and private key paths in the variables.tf file.

If the same local SSH Key is already added in DigitalOcean you may face an error. Currently the only solution is to
copy the name of your SSH Key in DO and delete it. Terraform will recreate the Key with the same name.

You can do that here, https://cloud.digitalocean.com/account/security

After that replace the name in the file 'main.tf' under the resource
'resource "digitalocean_ssh_key"'
##### Bill:
If the above servers run for a whole month, it will cost you $11.

You may however use ```terraform destroy``` when your done and incur a much lesser hourly cost.

##### Interact on DigitalOcean
Visit http://{Above Server IP}:5000/apidocs

### AWS
Will Add Next

### Heroku
Will Add Next

### GCP
Will Add Next

# ToDo
* Writing of better tests with more coverage.
* Add SSL and HTTPS verification with ACME.
* Add more cloud providers like AWS, GCP, Heroku etc.

# Testing
Only basic smoke tests are written as of now. They test the overall functionality with the docker compose containers.

```pipenv run pytest tests/```
###### OR
```python -m pytest tests/```

# Support Or Contact
Reach out to us at:

abhishek@smartassist.tech

stallon@smartassist.tech

# Author
Abhishek Jebaraj

abhishekjebaraj@outlook.com
