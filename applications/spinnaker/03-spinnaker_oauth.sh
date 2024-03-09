#!/bin/bash

# env flags that need to be set:

#MY_IP=`curl -s ifconfig.co`

DOMAIN='< your domain >'

CLIENT_ID=Iv1.b0d9d7ee93941f78
CLIENT_SECRET=effc154abcf4767c92db4a9abcd8df4222f9594a
PROVIDER=github
REDIRECT_URI=https://$DOMAIN:8084/login

set -e

if [ -z "${CLIENT_ID}" ] ; then
  echo "CLIENT_ID not set"
  exit
fi
if [ -z "${CLIENT_SECRET}" ] ; then
  echo "CLIENT_SECRET not set"
  exit
fi
if [ -z "${PROVIDER}" ] ; then
  echo "PROVIDER not set"
  exit
fi
if [ -z "${REDIRECT_URI}" ] ; then
  echo "REDIRECT_URI not set"
  exit
fi

hal config security authn oauth2 edit \
  --client-id $CLIENT_ID \
  --client-secret $CLIENT_SECRET \
  --provider $PROVIDER

hal config security authn oauth2 enable

hal config security authn oauth2 edit --pre-established-redirect-uri $REDIRECT_URI

sudo hal deploy apply