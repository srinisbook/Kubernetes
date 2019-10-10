# efs provisioner

By default, Kubernetes supports EBS Persistent Volumes. It also supports EFS Persistent Volumes by the external efs-provisioner.

The efs-provisioner allows you to mount EFS storage as PersistentVolumes in kubernetes. 

It consists of a container that has access to an AWS EFS resource. The container reads a configmap which contains the EFS filesystem ID, the AWS region and the name you want to use for your efs-provisioner. 

This name will be used later when you create a storage class.

### Amazon EFS

> Amazon Elastic File System (Amazon EFS) provides a simple, scalable, fully managed elastic NFS file system.  It is built to scale on demand to petabytes without disrupting applications, growing and shrinking automatically as you add and remove files, eliminating the need to provision and manage capacity to accommodate growth.
