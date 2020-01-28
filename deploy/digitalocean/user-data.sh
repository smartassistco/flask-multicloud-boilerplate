#!/bin/sh
echo "MaxSessions 500" >/etc/ssh/sshd_config
service ssh restart
ufw allow 5000
apt-get update -qy
apt-get upgrade -qy
