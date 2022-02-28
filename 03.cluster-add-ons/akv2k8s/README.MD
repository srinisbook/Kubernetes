
# Azure KeyVault to Kubernetes
### Download certificate from KeyVault and create a tls secret in AKS Cluster

https://akv2k8s.io/


## Key Vault setup

#### Step 1: Create a KeyVault to store SSL certificate if you don't have an existing Key Vault.

#### Step 2: Upload SSL certficate to the Key Vault.

#### Step 3: Go to Key Vault access policies and add new access policy with Get and List permissions on secrets and certificates to the AKS managed identities.

**Note:** There will be two managed identities for each cluster, one with "cluster-name" and the second one with "cluter-name-agentpool"

## Install Akv2k8s

### Step 1: Create a namespace

```
kubectl create ns akv2k8s
```

### Step 2: Add Helm repository

```
helm repo add spv-charts https://charts.spvapi.no
helm repo update
```

### Step 3: Install akv2k8s chart

```
helm upgrade --install akv2k8s spv-charts/akv2k8s --namespace akv2k8s
```

## Syncing the certificate

#### Step 1: Create a YAML file below content, ex: keyvault-cert-sync.yaml

```
apiVersion: spv.no/v1
kind: AzureKeyVaultSecret
metadata:
  name:  keyvault-cert-sync
spec:
  vault:
    name: <Key Vault Name>
    object:
      name: <Certificate name in the key Vault>
      type: certificate
  output:
    secret:
      name: <TLS Secret name mentioned in the Inggress>
      type: kubernetes.io/tls
```

#### Step 2: Update the above file with correct KeyVault name, certificate name and tls secret name.

#### Step 3: Apply the yaml file in the application namespace where pods and ingress is created

```
kubectl apply -f  keyvault-cert-sync.yaml -n <application namespace>
```

If the TLS secret is not created, run the below command to check status of the certificate sync process.

```
kubectl describe AzureKeyVaultSecret
```

Also, check logs of the akv2k8s pods in the akv2k8s namespace.