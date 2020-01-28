#todo SSH key work
#todo Add security
#todo Volumes

User $S
ssh-keyscan -t rsa 142.93.186.89 >> ~/.ssh/known_hosts
docker-compose -f docker-compose-prod.yml -H ssh://root@$SERVER_IP build
docker-compose -f docker-compose-prod.yml -H ssh://root@$SERVER_IP up