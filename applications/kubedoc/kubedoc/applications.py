from django.shortcuts import render, redirect
from django.http import HttpResponse
from kubernetes import client, config
from django.conf import settings
from .render import Render
from .k8s import K8s
import os

def application(request):


    context = {
        'title' : "Application Flow Diagram"
    }
    return render(request,'application.html',context )