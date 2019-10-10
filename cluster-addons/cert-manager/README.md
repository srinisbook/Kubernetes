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




