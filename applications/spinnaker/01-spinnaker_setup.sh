#!/bin/bash

sudo apt-get install --reinstall systemd -y

SPINNAKER_VERSION=1.10.14

curl -Os https://raw.githubusercontent.com/spinnaker/halyard/master/install/debian/InstallHalyard.sh

sudo bash InstallHalyard.sh --user ubuntu

#curl -fsSL get.docker.com -o get-docker.sh
#sh get-docker.sh
#sudo usermod -a -G docker $USER
#sudo docker run -p 127.0.0.1:9090:9000 -d --name minio1 -v /mnt/data:/data -v /mnt/config:/root/.minio minio/minio server /data

#sudo apt-get -y install jq

#MINIO_SECRET_KEY=`echo $(sudo docker exec minio1 cat /root/.minio/config.json) |jq -r '.credential.secretKey'`
#MINIO_ACCESS_KEY=`echo $(sudo docker exec minio1 cat /root/.minio/config.json) |jq -r '.credential.accessKey'`

AWS_S3_ACCESS_KEY=''
AWS_S3_SECRET_KEY=''
AWS_REGION=us-west-1

echo $AWS_S3_SECRET_KEY | hal config storage s3 edit  \
    --region $AWS_REGION \
    --access-key-id $AWS_S3_ACCESS_KEY \
    --secret-access-key

# --region $AWS_REGION 

hal config storage edit --type s3

# env flag that need to be set:

set -e

if [ -z "${SPINNAKER_VERSION}" ] ; then
  echo "SPINNAKER_VERSION not set"
  exit
fi

sudo hal config version edit --version $SPINNAKER_VERSION
sudo hal deploy apply

sudo echo "host: 0.0.0.0" |sudo tee \
    /home/ubuntu/.hal/default/service-settings/gate.yml \
    /home/ubuntu/.hal/default/service-settings/deck.yml

#MY_IP=`curl ifconfig.co`
#hal config security ui edit --override-base-url http://$MY_IP:9000
#hal config security api edit --override-base-url http://$MY_IP:8084

DOMAIN=''

hal config security ui edit --override-base-url https://$DOMAIN:9000
hal config security api edit --override-base-url https://$DOMAIN:8084

sudo hal deploy apply

sudo systemctl daemon-reload

sudo systemctl restart apache2
sudo systemctl restart gate
sudo systemctl restart orca
sudo systemctl restart igor
sudo systemctl restart front50
sudo systemctl restart echo
sudo systemctl restart clouddriver
sudo systemctl restart rosco
sudo systemctl restart redis-server


sudo systemctl enable apache2
sudo systemctl enable gate
sudo systemctl enable orca
sudo systemctl enable igor
sudo systemctl enable front50
sudo systemctl enable echo
sudo systemctl enable clouddriver
sudo systemctl enable rosco
sudo systemctl enable redis-server
