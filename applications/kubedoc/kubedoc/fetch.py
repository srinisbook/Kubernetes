from django.shortcuts import render, redirect
from django.http import HttpResponse
from kubernetes import client, config
from django.conf import settings
import datetime
import os
import sys

def nodes(request, node_name ):
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()
    
    v1=client.CoreV1Api()
    node_data = v1.read_node(node_name)
    context = {
        'data' : node_data,
        'title' : "Node | " + node_name
    }

    return render(request,'data.html', context )

def namespaces(request, namespace_name ):
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()
    
    v1=client.CoreV1Api()
    namespace_data = v1.read_namespace(namespace_name)
    context = {
        'data' : namespace_data,
        'title' : "Namespace | " +  namespace_name
    }

    return render(request,'data.html', context )

def pods(request, pod_name ):
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()
    
    v1=client.CoreV1Api()
    pods = v1.list_pod_for_all_namespaces(watch=False)
    pod_data = ""
    for i in pods.items:
        if ( i.metadata.name == pod_name ):
            pod_data = i
    
    context = {
        'data' : pod_data,
        'title' : "Pod | " + pod_name
    }

    return render(request,'data.html', context )

def deployments(request, deployment_name ):
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()
    
    appsv1=client.AppsV1Api()
    deployments = appsv1.list_deployment_for_all_namespaces(watch=False)
    deployment_data = ""
    for i in deployments.items:
        if ( i.metadata.name == deployment_name ):
            deployment_data = i
    
    context = {
        'data' : deployment_data,
        'title' : "Deployment | " +  deployment_name
    }

    return render(request,'data.html', context )

def daemonsets(request, daemonset_name ):
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()
    
    appsv1=client.AppsV1Api()
    daemonsets = appsv1.list_daemon_set_for_all_namespaces(watch=False)
    daemonset_data = ""
    for i in daemonsets.items:
        if ( i.metadata.name == daemonset_name ):
            daemonset_data = i
    
    context = {
        'data' : daemonset_data,
        'title' : "Daemonset | " + daemonset_name
    }

    return render(request,'data.html', context )

def statefulsets(request, statefulset_name ):
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()
    
    appsv1=client.AppsV1Api()
    statefulsets = appsv1.list_stateful_set_for_all_namespaces(watch=False)
    statefulset_data = ""
    for i in statefulsets.items:
        if ( i.metadata.name == statefulset_name ):
            statefulset_data = i
    
    context = {
        'data' : statefulset_data,
        'title' : "Statefulset | " + statefulset_name
    }

    return render(request,'data.html', context )

def services(request, service_name ):
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()
    
    v1=client.CoreV1Api()
    services = v1.list_service_for_all_namespaces(watch=False)
    service_data = ""
    for i in services.items:
        if ( i.metadata.name == service_name ):
            service_data = i
    
    context = {
        'data' : service_data,
        'title' : "Service | " + service_name
    }

    return render(request,'data.html', context )

def ingress(request, ingress_name ):
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()
    
    extv1beta=client.ExtensionsV1beta1Api()
    ingress = extv1beta.list_ingress_for_all_namespaces(watch=False)
    ingress_data = ""
    for i in ingress.items:
        if ( i.metadata.name == ingress_name ):
            ingress_data = i
    
    context = {
        'data' : ingress_data,
        'title' : "Ingress | " + ingress_name
    }

    return render(request,'data.html', context )

def volumes(request, volume_name ):
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()
    
    v1=client.CoreV1Api()
    volumes = v1.list_persistent_volume(watch=False)
    volume_data = ""
    for i in volumes.items:
        if ( i.metadata.name == volume_name ):
            volume_data = i
    
    context = {
        'data' : volume_data,
        'title' : "Voulume | " + volume_name
    }

    return render(request,'data.html', context )