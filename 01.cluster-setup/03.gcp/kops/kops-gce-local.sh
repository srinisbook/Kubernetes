#!/bin/bash
set -e	# Any subsequent(*) commands which fail will cause the shell script to exit immediately

export PROJECT='<gcp_project_id>'

export KOPS_CLUSTER_NAME='<cluster_name.k8s.local>' 		# Cluster name should FQDN, example : myfirstcluster.k8s.local
export KOPS_VPC="<vpc_name>"                              		# VPC will create with given name.
export BUCKET_NAME="<bucket_name>"  	                		# Provide a name to create bucket. Bucket name should be Unique globally.

export BUCKET_REGION="us-east1"                            		# Bucket will create in the provided region.
export NODE_ZONES="us-east1-b,us-east1-c,us-east1-d"	        	# Worker nodes zones with comma separated.
export MASTER_ZONES="us-east1-b,us-east1-c,us-east1-d"			# Master nodes zones with comma separated.
# https://cloud.google.com/compute/docs/regions-zones/

export NODE_COUNT=5							# Worker nodes count.
export MASTER_COUNT=3							# Master nodes count. Provide only odd number.
export MASTER_SIZE="n1-standard-2"					# Master node machine type. Change instance type to meet your workload
export NODE_SIZE="n1-standard-4"					# Worker node machine type. Change instance type to meet your workload
# https://cloud.google.com/compute/docs/machine-types

export KOPS_FEATURE_FLAGS=AlphaAllowGCE

gcloud config set project $PROJECT

echo "Checking for dependencies ...."

if ! type kops > /dev/null; then
	echo "kops not found. Installing kops ......"
  	curl -Lo kops https://github.com/kubernetes/kops/releases/download/$(curl -s https://api.github.com/repos/kubernetes/kops/releases/latest | grep tag_name | cut -d '"' -f 4)/kops-linux-amd64
	chmod +x ./kops
	sudo mv ./kops /usr/local/bin/
fi

if ! type kubectl > /dev/null; then
	echo "kubectl not found. Installing kubectl ......"
	curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
	chmod +x ./kubectl
	sudo mv ./kubectl /usr/local/bin/
fi

if ! type helm > /dev/null; then
	echo "helm not found. Installing helm ......"
	curl -L https://git.io/get_helm.sh | bash
fi

if ! type kubectx > /dev/null; then
	echo "kubectx and kubens not found. Installing kubectx and kubens ......"
	sudo git clone https://github.com/ahmetb/kubectx /opt/kubectx
        sudo ln -s /opt/kubectx/kubectx /usr/local/bin/kubectx
        sudo ln -s /opt/kubectx/kubens /usr/local/bin/kubens
fi

case "$1" in

create)

	# Create a VPC
	check_vpc=`gcloud compute networks list --filter="name=('${KOPS_VPC}')" 2> /dev/null`

	if [ -z "$check_vpc" ]
	then
		echo "Creating VPC ....."
		gcloud compute networks 	\
		create ${KOPS_VPC} 		\
		--project=${PROJECT} 	\
		--subnet-mode=auto
	else
      		echo "VPC already available"
	fi
	
	# Create a Storage Bucket
	echo "Creating storage bucket ....."
	gsutil mb -l  ${BUCKET_REGION} gs://${BUCKET_NAME}

	# Create Kubernetes Cluster
	echo "Creating Kubenetes cluster ......"
	kops create cluster --name=${KOPS_CLUSTER_NAME}  \
		--state=gs://${BUCKET_NAME} 				 \
		--zones=${NODE_ZONES} 						 \
		--master-zones=${MASTER_ZONES}				 \
		--vpc=${KOPS_VPC}							 \
		--project=${PROJECT} 						 \
		--node-count=${NODE_COUNT}					 \
		--node-size=${NODE_SIZE}					 \
		--master-count=${MASTER_COUNT}				 \
		--master-size=${MASTER_SIZE}				 \
		--cloud gce									 \
		--yes

	echo "Cluster created successfully"
	
	while true
        do
		echo "Waiting for cluster ready ...."
   		set +e 
		kubectl get nodes > /dev/null 2>&1
		exit_status=$?
		if [ $exit_status -eq 1 ]
		then
         		sleep 30
	 		continue;
		else
			echo "Cluster is ready :)"
	 		break;
        	fi
        done
	
	set -e

	# Initialize helm
	echo "Initializing helm .........."
	helm init

	# Create service account for tiller
	echo "Creating service account and clusterrolebinding for tiller..."
	kubectl create serviceaccount --namespace kube-system tiller
	kubectl create clusterrolebinding tiller-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:tiller
	kubectl patch deploy --namespace kube-system tiller-deploy -p '{"spec":{"template":{"spec":{"serviceAccount":"tiller"}}}}'
        
	echo "Finished!"

	;;
delete)
	# Delete Kubernetes Cluster
	echo "Deleting cluster ......."
	kops delete cluster --name=${KOPS_CLUSTER_NAME} --state=gs://${BUCKET_NAME}  --yes
	exit_status=$?
        if [ $exit_status -eq 0 ]
        then
		echo "Deleting bucket ......" 
		gsutil rb gs://${BUCKET_NAME}
        fi
	;;
list)
	# Get Clusters
	kops get cluster --state=gs://${BUCKET_NAME}
	;;
validate)
	# Get Clusters
	kops validate cluster --state=gs://${BUCKET_NAME}
	;;
*)
   echo "Usage: $0 {create|delete|list|validate}"

esac
exit 0 
