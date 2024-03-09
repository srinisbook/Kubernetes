
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls import url

from django.conf.urls import handler404, handler500, url

from django.contrib.auth.views import LoginView, LogoutView

from . import main
from . import error_handler
from . import fetch
from . import pdf
from . import applications

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',main.clusteroverview,name='cluster-overview'),
    path('pdf',pdf.pdf,name='PDF Document'),
    path('node/<node_name>',fetch.nodes),
    path('namespace/<namespace_name>',fetch.namespaces),
    path('pod/<pod_name>',fetch.pods),
    path('deployment/<deployment_name>',fetch.deployments),
    path('daemonset/<daemonset_name>',fetch.daemonsets),
    path('statefulset/<statefulset_name>',fetch.statefulsets),
    path('service/<service_name>',fetch.services),
    path('ingress/<ingress_name>',fetch.ingress),
    path('volume/<volume_name>',fetch.volumes),
    #path('application',applications.application),
]

handler404 = error_handler.error_404
handler500 = error_handler.error_500
