# minikube

#### Minikube is an open source tool that makes it easy to run Kubernetes locally.

#### Minikube runs a single-node Kubernetes for users looking to try out Kubernetes or develop with it day-to-day.

#### This is ideal for development, tests and POC purposes.

#### Prerequisite
- Virtualization must be enabled

#### If you want to try out minikube on a VM Ware virtual machine, you must enable VT-x or AMD-v in your vm's setting.

## Installation

**Step 1: Update packages**

Run the following commands to update all system packages to the latest release.

    sudo apt-get update -y
    sudo apt-get install apt-transport-https -y
    sudo apt-get upgrade -y

**Step 2: Install VirtualBox Hypervisor on Ubuntu**

    sudo apt install virtualbox virtualbox-ext-pack -y


**Step 3: Download minikube**

Download minikube binary and make it executable for all users.

    wget https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    
    chmod +x minikube-linux-amd64
    
    sudo mv minikube-linux-amd64 /usr/local/bin/minikube

Check version:

    $ minikube version
    minikube version: v0.28.0

**Step 4: Start minikube**

Now, you can start minikube. VM image will be downloaded and configured for Kubernetes for you.

    $ minikube start
    Starting local Kubernetes v1.10.0 cluster...
    Starting VM...
    Downloading Minikube ISO
    150.53 MB / 150.53 MB [============================================] 100.00% 0s
    Getting VM IP address...
    Moving files into cluster...
    Downloading kubeadm v1.10.0
    Downloading kubelet v1.10.0
    Finished Downloading kubeadm v1.10.0
    Finished Downloading kubelet v1.10.0
    Setting up certs...
    Connecting to cluster...
    Setting up kubeconfig...
    Starting cluster components...
    Kubectl is now configured to use the cluster.
    Loading cached images from config file.

**Step 5: Install kubectl**

You need kubectl to deploy and manage applications on Kubernetes

    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
  
    sudo apt-get update -y
    sudo apt-get install -y kubectl

Check version:

    $ kubectl version -o json


**Check nodes:**

    $ kubectl get nodes
    NAME     STATUS ROLES  AGE  VERSION
    minikube Ready  master 6m1s v1.13.3

**Run nginx container:**

    $ kubectl run nginx --image=nginx:latest

    $ kubectl get pods
    NAME                  READY STATUS  RESTARTS AGE
    nginx-585fddf4b-xz7t6 1/1   Running 0        63s

**Access nginx application:**

Create a service by exposing the deployment.  To access the application with your private IP address, use NodePort service type.

    $ kubectl expose deployment nginx --port=80 --type=NodePort

    $ kubectl get service
    NAME       TYPE      CLUSTER-IP  EXTERNAL-IP PORT(S)      AGE
    kubernetes ClusterIP 10.96.0.1   < none >    443/TCP      9m23s
    nginx      NodePort  10.99.26.23 < none >    80:31728/TCP 10s

Now you can see the nginx page with http://your-ip.


**To stop minikube:**

    $ minikube stop

**To remove kubernetes:**

    $ minikube delete

**To list Kubernetes addons:**

    $ minikube addons list

**Enable Kubernetes Dashboard:**

Dashboard is a web-based Kubernetes user interface. You can use Dashboard to get an overview of applications running on your cluster, as well deploy containerized applications to a Kubernetes cluster, troubleshoot your containerized application, and manage the cluster resources.

    $ minikube dashboard
    Enabling dashboard ...
    Verifying dashboard health ...
    Launching proxy ...
    Verifying proxy health ...
    http://127.0.0.1:35837/api/v1/namespaces/kube-system/services/http:kubernetes-dashboard:/proxy/

It will open the dashboard in the browser.
