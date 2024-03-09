hal config ci jenkins enable

BASEURL='http://jenkins.gcloud.s3labs.com:8080/'
USERNAME='admin'
PASSWORD='Sree12#$'

echo $PASSWORD | hal config ci jenkins master add my-jenkins-master \
    --address $BASEURL \
    --username $USERNAME \
    --password

hal config ci jenkins master edit my-jenkins-master --csrf true

sudo hal deploy apply

sudo systemctl daemon-reload
