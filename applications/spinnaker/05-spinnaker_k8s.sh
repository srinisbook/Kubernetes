hal config provider kubernetes enable

CONTEXT=$(kubectl config current-context)

hal config provider kubernetes account add my-cluster-1 \
    --provider-version v2 \
    --context $CONTEXT 

# Omit Namespaces
# hal config provider kubernetes account add gke-cluster-1 \
# --omit-namespaces kube-system

# Allow only spectific namespaces

hal config provider kubernetes account edit gke-cluster-1 \
    --namespaces srinis-book

hal config features edit --artifacts true

sudo hal deploy apply

sudo systemctl daemon-reload