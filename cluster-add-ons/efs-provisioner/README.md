# efs provisioner

By default, Kubernetes supports EBS Persistent Volumes. It also supports EFS Persistent Volumes by the external efs-provisioner.

The efs-provisioner allows you to mount EFS storage as PersistentVolumes in kubernetes. 

It consists of a container that has access to an AWS EFS resource. The container reads a configmap which contains the EFS filesystem ID, the AWS region and the name you want to use for your efs-provisioner. 

This name will be used later when you create a storage class.

### Amazon EFS

> Amazon Elastic File System (Amazon EFS) provides a simple, scalable, fully managed elastic NFS file system.  It is built to scale on demand to petabytes without disrupting applications, growing and shrinking automatically as you add and remove files, eliminating the need to provision and manage capacity to accommodate growth.

### Mount EFS filesystem

Before installing efs-provisioner, you must mount efs filesystem to an instanaces and create a directory called 'persistentvolumes'.

Edit efs-setup.yaml and add ***efs filesystem dns name*** in PersistentVolume configuaration.

    nfs:
      server: <efs_dnsname>
      path: "/"
   
Apply the efs-setup.yaml and check the efs-mount pod status.   
    
    $ kubectl apply -f efs-setup.yaml 
    persistentvolume/efs-setup created
    persistentvolumeclaim/efs-setup created
    pod/efs-setup created
    
    $ kubectl get pod efs-mount
    NAME        READY   STATUS    RESTARTS   AGE
    efs-setup   1/1     Running   0          26s

Once efs-setup pod came to running state, create a directory called 'persistentvolumes'.

    $ kubectl exec efs-setup mkdir /efs-setup/persistentvolumes

If the above command successful then you can delete the efs-setup resources.
    
    $ kubectl delete -f efs-setup.yaml
    
### Install efs provisioner

Edit efs-provisioner.yaml and update following details:

- aws_region
- efs_filesystem_id
- efs_dns_name

Now install efs provisioner:

    $ kubectl apply -f efs-setup.yaml
    namespace/efs-provisioner created
    clusterrole/efs-provisioner-runner created
    clusterrolebinding/run-efs-provisioner created
    role/leader-locking-efs-provisioner created
    rolebinding/leader-locking-efs-provisioner created
    configmap/efs-provisioner created
    serviceaccount/efs-provisioner created
    deployment/efs-provisioner created
    
    $ kubectl get pods -n efs-provisioner
    kubectl get pods
    NAME                               READY   STATUS    RESTARTS   AGE
    efs-provisioner-8mn75845c5-3hm23   1/1     Running   0          30s

Once efs provisioner deployed successfully, you can create a storage class and you can use it to create persistent volume clains for your applications.

    $ kubectl apply -f efs-storageclass.yaml
    storageclass/efs created
    
    $ kubectl get storageclass
    NAME                PROVISIONER             AGE
    default (default)   kubernetes.io/aws-ebs   2d
    gp2                 kubernetes.io/aws-ebs   2d
    efs                 efs-storage/aws-efs     20s
    
### PersistentVolumeClaim
 
Once you installed efs provisioner, application can use efs storage. Below is the PersistentVolumeClaim example:
 
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: app-efs-pvc
    spec:
      accessModes:
        - ReadWriteMany
      resources:
        requests:
          storage: 100Mi
      storageClassName: efs
