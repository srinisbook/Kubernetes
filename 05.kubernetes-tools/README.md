# Kubernetes Tools

## kubectl
The Kubernetes command-line tool, kubectl, allows you to run commands against Kubernetes clusters. You can use kubectl to deploy applications, inspect and manage cluster resources, and view logs.
#### Install kubectl on Linux
```
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
kubectl version
```
#### Install kubectl on macOS
```
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/darwin/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
kubectl version
```
#### Install kubectl on Windows
```
curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.15.0/bin/windows/amd64/kubectl.exe
kubectl version
```

## kops
kops helps you create, destroy, upgrade and maintain production-grade, highly available, Kubernetes clusters from the command line. AWS (Amazon Web Services) is currently officially supported, with GCE in beta support , and VMware vSphere in alpha, and other platforms planned.
#### Install kops on Linux
```
curl -LO https://github.com/kubernetes/kops/releases/download/$(curl -s https://api.github.com/repos/kubernetes/kops/releases/latest | grep tag_name | cut -d '"' -f 4)/kops-linux-amd64
chmod +x kops-linux-amd64
sudo mv kops-linux-amd64 /usr/local/bin/kops
```
#### Install kops on macOS
```
brew update && brew install kops
```
#### Install kops on Windows
* Download kops-windows-amd64 from [releases](https://github.com/kubernetes/kops/releases/latest).
* Rename kops-windows-amd64 to kops.exe and store it in a preferred path.
* Make sure the path you chose is added to your Path environment variable.

## helm
Helm is a tool for managing Kubernetes charts. Charts are packages of pre-configured Kubernetes resources.

#### Install From Binary Releases
* Download your desired version
* Unpack it (tar -zxvf helm-v2.0.0-linux-amd64.tgz)
* Find the helm binary in the unpacked directory, and move it to its desired destination (mv linux-amd64/helm /usr/local/bin/helm)

#### Install helm on Linux
```
curl -L https://git.io/get_helm.sh | bash
```
#### Install helm on macOS
```
brew install kubernetes-helm
```
#### Install From Chocolatey (Windows)
```
choco install kubernetes-helm
```
[choco installation](https://chocolatey.org/docs/installation)

After helm installed, run 'helm init' command to start work with helm.

If you get any permission denied errors while deploying applications through helm charts, run the following commands:

```
kubectl create serviceaccount --namespace kube-system tiller
kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'
```

## kubectx and kubens

kubectx is a utility to manage and switch between kubectl contexts. kubectx helps you switch between clusters back and forth.

kubens is a utility to switch between Kubernetes namespaces.

#### Installation on Linux 
```
git clone https://github.com/ahmetb/kubectx /opt/kubectx
sudo ln -s /opt/kubectx/kubectx /usr/local/bin/kubectx
sudo ln -s /opt/kubectx/kubens /usr/local/bin/kubens
```
#### Installation on macOs 
```
brew install kubectx
```
