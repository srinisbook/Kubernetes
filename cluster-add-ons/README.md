<img src="https://github.com/jetstack/cert-manager/raw/master/logo/logo.png" width="200" /> 

# cert-manager

cert-manager is a Kubernetes add-on to automate TLS certificates management and issuance from various issuing sources such as Let’s Encrypt, HashiCorp Vault, Venafi, a simple signing keypair, or self signed.

It will ensure certificates are valid and up to date periodically, and attempt to renew certificates  before expiry.

Documentation for cert-manager can be found at [docs.cert-manager.io](https://docs.cert-manager.io/en/latest/ "docs.cert-manager.io")

### Install cert-manager

    git clone https://github.com/srinisbook/Kubernetes.git
    cd Kubernetes/cluster-addons/cert-manager/
    kubectl apply -f cert-manager-v0.9.1.yaml

### Helm chart

To install cert-manager with helm chart:

    helm install --name cert-manager --namespace cert-manager stable/cert-manager
Uninstalling the Chart

    helm del cert-manager --purge
    
Helm chart documentation con be found [here](https://github.com/helm/charts/tree/master/stable/cert-manager "here")

# Issuers

Issuers (and ClusterIssuers) represent a certificate authority from which signed x509 certificates can be obtained, such as Let’s Encrypt. 

You will need at least one Issuer or ClusterIssuer in order to begin issuing certificates within your cluster.

- An Issuer is a namespaced resource, you will need to create an Issuer in each namespace you wish to obtain Certificates in.

- If you want to create a single issuer that can be consumed in multiple namespaces, you should consider creating a ClusterIssuer resource.



# Let's Encrypt

<img src="https://dyltqmyl993wv.cloudfront.net/assets/stacks/cert-manager/img/cert-manager-stack-220x234.png" width="200" />

Let’s Encrypt is a free, automated, and open Certificate Authority. Documentation can be found at [letsencrypt.org]( https://letsencrypt.org/docs/)

Currently, letsencrypt providing following API endpoints:
- [Production] https://acme-v02.api.letsencrypt.org/directory
- [Staging] https://acme-staging-v02.api.letsencrypt.org/directory

It is recommend testing against staging before using production environment. This will allow you to get things right before issuing trusted certificates and reduce the chance of your running up against rate limits.

See [Rate limits](https://letsencrypt.org/docs/rate-limits/)


