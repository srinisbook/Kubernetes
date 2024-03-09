from django.shortcuts import render, redirect
from django.http import HttpResponse
from kubernetes import client, config
from django.conf import settings
from .render import Render
from .k8s import K8s
import os

def pdf(request):

    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()
    
    v1=client.CoreV1Api()
    appsv1=client.AppsV1Api()
    extv1beta=client.ExtensionsV1beta1Api()
    
    nodes = v1.list_node(watch=False)

    namespaces = v1.list_namespace(watch=False)

    pods =  v1.list_pod_for_all_namespaces(watch=False)
    
    ingress = extv1beta.list_ingress_for_all_namespaces(watch=False)
    services = v1.list_service_for_all_namespaces(watch=False)
    
    deployments = appsv1.list_deployment_for_all_namespaces(watch=False)
    daemonsets = appsv1.list_daemon_set_for_all_namespaces(watch=False)
    statefulsets = appsv1.list_stateful_set_for_all_namespaces(watch=False)
    
    pv = v1.list_persistent_volume(watch=False)
    
    nodes_data = K8s.nodes(nodes)
    namespace_data = K8s.namespaces(namespaces)
    pods_data = K8s.pods(pods)
    workloads_data = K8s.workloads(deployments,daemonsets,statefulsets)
    ingress_data = K8s.ingress(ingress)
    service_data = K8s.services(services)
    pv_data = K8s.volumes(pv)

    provider = nodes_data['provider']
    running_since = nodes_data['running_since']
    capacity = nodes_data['capacity']
    master_machine_type = nodes_data['master_machine_type']
    worker_machine_type = nodes_data['worker_machine_type']
    worker_machine_size = nodes_data['worker_machine_size']
    master_machine_size = nodes_data['master_machine_size']
    total_nodes = nodes_data['total_nodes']
    masters = nodes_data['masters']
    workers = nodes_data['workers']
    node_pdf_data = nodes_data['nodes_pdf_data']
    
    namespace_pdf_data = namespace_data['namespace_pdf_data']
    namespace_count = namespace_data['namespace_count']
    pod_pdf_data = pods_data['pod_pdf_data']
    pod_count = pods_data['pod_count']
    workloads_pdf_data = workloads_data['workload_pdf_data']
    deployments_count = workloads_data['deployments_count']
    statefulsets_count = workloads_data['statefulsets_count']
    daemonsets_count = workloads_data['daemonsets_count']
    ingress_pdf_data = ingress_data['ingress_pdf_data']
    ingresses_count = ingress_data['ingress_count']
    service_pdf_data  = service_data['service_pdf_data']
    services_count = service_data['service_count']
    pv_pdf_data = pv_data['pv_pdf_data']
    pv_count = pv_data['pv_count']

    cluster_name = os.getenv('CLUSTER_NAME', 'Kubernetes Cluster')
    environments = os.getenv('ENVIRONMENTS','Test')
    org = os.getenv('ORGANIZATION','My Organization')

    context = {
            'cluster_name' : cluster_name,
            'environments' : environments,
            'org' : org,
            'provider' : provider,
            'running_since' : running_since,
            'capacity' : capacity,
            'master_machine_type' : master_machine_type,
            'worker_machine_type' : worker_machine_type,
            'master_machine_size' : master_machine_size,
            'worker_machine_size' : worker_machine_size,
            'total_nodes' : total_nodes,
            'masters' : masters,
            'workers' : workers,
            'node_data' : node_pdf_data,
            'namespace_data' : namespace_pdf_data,
            'namespace_count' : namespace_count,
            'pods_data' : pod_pdf_data,
            'pod_count' : pod_count,
            'workloads_data' : workloads_pdf_data,
            'deployments_count' : deployments_count,
            'statefulsets_count' : statefulsets_count,
            'daemonsets_count' : daemonsets_count,
            'service_data' : service_pdf_data,
            'services_count' : services_count,
            'ingress_data' : ingress_pdf_data,
            'ingresses_count' :   ingresses_count,     
            'pv_table_data' : pv_pdf_data,
            'pv_count' : pv_count
        }

    return Render.render('pdf.html', context )