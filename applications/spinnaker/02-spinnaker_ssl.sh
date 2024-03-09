#!/bin/bash
# Install certbot
sudo apt-get update -y
sudo apt-get install software-properties-common -y
sudo add-apt-repository universe -y
sudo add-apt-repository ppa:certbot/certbot -y
sudo apt-get update -y
sudo apt-get install certbot python-certbot-apache -y

# Generate certificates
export DOMAIN= < your-domain >

sudo certbot certonly -d \*.$DOMAIN \
  --manual --server https://acme-v02.api.letsencrypt.org/directory \
  --preferred-challenges dns


sudo cp -R /etc/letsencrypt/archive/$DOMAIN/ /home/ubuntu/

sudo mv $DOMAIN certs

sudo chown -R ubuntu:ubuntu certs/

cd certs


# Gate Java TrustStore/KeyStore setup

cat fullchain1.pem privkey1.pem > wildcard.pem

openssl pkcs12 -export -out wildcard.pkcs12 \
  -in wildcard.pem -name spinnaker \
  -password pass:nosecrets

keytool -v -importkeystore -srckeystore wildcard.pkcs12 \
  -destkeystore wildcard.jks -deststoretype JKS \
  -srcstorepass nosecrets \
  -deststorepass nosecrets

keytool -trustcacerts -keystore wildcard.jks \
  -importcert -file chain1.pem \
  -storepass nosecrets
  
KEYSTORE_PATH=~/certs/wildcard.jks


# Deck SSL Setup

cp privkey1.pem wildcard.key

cp fullchain1.pem wildcard.crt

SERVER_CERT=wildcard.crt

SERVER_KEY=wildcard.key


hal config security api ssl edit --key-alias spinnaker \
  --keystore $KEYSTORE_PATH --keystore-password  \
  --keystore-type jks --truststore $KEYSTORE_PATH \
  --truststore-password \
  --truststore-type jks

hal config security api ssl enable

hal config security ui ssl edit --ssl-certificate-file $SERVER_CERT --ssl-certificate-key-file $SERVER_KEY

hal config security ui ssl enable

sudo hal deploy apply

sudo systemctl daemon-reload