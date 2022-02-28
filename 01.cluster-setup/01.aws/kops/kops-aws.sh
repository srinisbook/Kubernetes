#!/bin/bash
set -e	# Any subsequent(*) commands which fail will cause the shell script to exit immediately

export KOPS_CLUSTER_NAME="< clustername.hostedzone >" 		# Cluster name should FQDN, example : mycluster.your-domain.com
export KOPS_DNS_ZONE="< hostedzone >"                          	# DNS zone name. It should be created before the cluster creation
export S3_BUCKET_NAME="< bucket name >"  	                # Provide a name to create bucket. Bucket name should be Unique globally.

export S3_BUCKET_REGION="us-east-1"                             # Bucket will create in the provided region.
export NODE_ZONES="us-east-1a,us-east-1b,us-east-1c"	        # Worker nodes zones with comma separated.
export MASTER_ZONES="us-east-1a,us-east-1b,us-east-1c"		# Master nodes zones with comma separated.

# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html

export NODE_COUNT=5						# Worker nodes count.
export MASTER_COUNT=3						# Master nodes count. Provide only odd number.
export MASTER_SIZE="t2.medium"					# Master node machine type. Change instance type to meet your workload
export NODE_SIZE="t2.medium"					# Worker node machine type. Change instance type to meet your workload

# https://aws.amazon.com/ec2/instance-types/

echo "Checking for dependencies ......."

if ! type aws  > /dev/null; then
	echo "AWS CLI not installed. Installing aws cli ......"
	sudo pip install awscli --force-reinstall --upgrade
	aws --version
fi

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
	# Create S3 Bucket
	echo "Creating S3 Bucket ......."
	aws s3 mb s3://${S3_BUCKET_NAME} --region ${S3_BUCKET_REGION}

	# Create Kubernetes Cluster
	echo "Creating Kubenetes cluster ......"
	kops create cluster --name=${KOPS_CLUSTER_NAME}  			\
		--state=s3://${S3_BUCKET_NAME} 				 	\
		--zones=${NODE_ZONES} 						\
		--master-zones=${MASTER_ZONES}				 	\
		--node-count=${NODE_COUNT}					\
		--node-size=${NODE_SIZE}					\
		--master-count=${MASTER_COUNT}					\
		--master-size=${MASTER_SIZE}				 	\
	        --dns-zone=${KOPS_DNS_ZONE} 			 	 	\
		--cloud aws							\
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
	kops delete cluster --name=${KOPS_CLUSTER_NAME} --state=s3://${S3_BUCKET_NAME}  --yes
	exit_status=$?
        if [ $exit_status -eq 0 ]
        then
		echo "Deleting S3 bucket ......" 
		aws s3 rb s3://${S3_BUCKET_NAME} --force
        fi
	;;
list)
	# Get Clusters
	kops get cluster --state=s3://${S3_BUCKET_NAME}
	;;
validate)
	# Get Clusters
	kops validate cluster --state=s3://${S3_BUCKET_NAME}
	;;
*)
   echo "Usage: $0 {create|delete|list|validate}"

esac
exit 0 
