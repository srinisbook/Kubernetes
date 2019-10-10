# Contour

Contour is an Ingress controller for Kubernetes that works by deploying the Envoy proxy as a reverse proxy and load balancer.

### Add Contour to your cluster
#### Prerequisites
- RBAC must be enabled on your cluster
- Kubernetes clusters running version 1.10 and later

Run:

    $ kubectl apply -f contour.yaml
    
    $ kubectl get all -n heptio-contour
    NAME                           READY     STATUS    RESTARTS   AGE
    pod/contour-84fc7556f5-4whfn   2/2       Running   0          2m
    pod/contour-84fc7556f5-xsqb6   2/2       Running   0          2m

    NAME              TYPE           CLUSTER-IP    EXTERNAL-IP   PORT(S)                      AGE
    service/contour   LoadBalancer   10.7.253.78   35.188.17.0   80:30260/TCP,443:31803/TCP   1m

    NAME                      DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
    deployment.apps/contour   2         2         2            2           2m

    NAME                                 DESIRED   CURRENT   READY     AGE
    replicaset.apps/contour-84fc7556f5   2         2         2         2m

#### Ingress class annotation

You must specify `kubernetes.io/ingress.class: contour ` to serve the Ingress only by the Contour.

### IngressRoute

Contour also introduces a new ingress API (IngressRoute) which is implemented via a Custom Resource Definition (CRD).

Its goal of the IngressRoute to expand upon the functionality of the Ingress API to allow for richer user experience as well as solve shortcomings in the original design.

IngressRoute example:

    apiVersion: contour.heptio.com/v1beta1
    kind: IngressRoute
    metadata:
      name: my-ingress-route
    spec:
      virtualhost:
        fqdn: subdomain.your-domain.com
      routes:
        - match: /
          services:
            - name: my-service
              port: 80
#### TLS
Like Ingress, The IngressRoute can be configured to use this secret using tls.secretName property:

    apiVersion: contour.heptio.com/v1beta1
    kind: IngressRoute
    metadata:
      name: ingress-route-example
    spec:
      virtualhost:
        fqdn: blog.domain.com
        tls:
          secretName: testsecret
      routes:
        - match: /
          services:
            - name: blog-service
              port: 80

#### Routing
Like Ingress, IngressRoute also supports multiple routes.

    apiVersion: contour.heptio.com/v1beta1
    kind: IngressRoute
    metadata:
      name: domain-routes
    spec:
      virtualhost:
        fqdn: domain.com
      routes:
        - match: /
          services:
            - name: main-srv
              port: 80
        - match: /shop
          services:
            - name: shop-srv
              port: 80
        - match: /music
          services:
            - name: music-srv
              port: 80

One of the key IngressRoute features is the ability to support multiple services for a given path:

    apiVersion: contour.heptio.com/v1beta1
    kind: IngressRoute
    metadata:
      name: multiple-upstreams
      namespace: default
    spec:
      virtualhost:
        fqdn: domaincom
      routes:
        - match: /music
          services:
            - name: music-1-srv
              port: 80
            - name: music-2-srv
              port: 80

We can also define relative weights for the Services.

    apiVersion: contour.heptio.com/v1beta1
    kind: IngressRoute
    metadata:
      name: multiple-upstreams
      namespace: default
    spec:
      virtualhost:
        fqdn: domain.com
      routes:
        - match: /music
          services:
            - name: music-1-srv
              port: 80
              weight: 30
            - name: music-2-srv
              port: 80
              weight: 70
In the above example, we are sending 30% of the traffic to Service music-1-srv, while Service music-2-srv receives the other 70% of traffic.

#### Load Balancing Strategy

IngressRoute has the feature providing load balancing to the services.
Following are the options available:
- RoundRobin
- WeightedLeastRequest
- RingHash
- Maglev
- Random

      apiVersion: contour.heptio.com/v1beta1
      kind: IngressRoute
      metadata:
        name: domain.com-lb
      spec:
        virtualhost:
          fqdn: domain.com
        strategy: WeightedLeastRequest
        routes:
          - match: /music
            services:
              - name: music-1-srv
                port: 80
              - name: music-2-srv
                port: 80
              - name: music-3-srv
                port: 80

The default load balancing strategy can be overridden by specifying to the individual service.

     - name: music-3-srv
       port: 80
       strategy: Random

#### Health Checking

Contour supports HTTP health checking and can be configured with various settings to tune the behavior.

    apiVersion: contour.heptio.com/v1beta1
    kind: IngressRoute
    metadata:
      name: music.domain.com-lb
    spec:
      virtualhost:
        fqdn: domain.com
      strategy: WeightedLeastRequest
      healthCheck:
        path: /music
        intervalSeconds: 5
        timeoutSeconds: 2
        unhealthyThresholdCount: 3
        healthyThresholdCount: 5
      routes:
        - match: /music
          services:
            - name: music-1-srv
              port: 80
            - name: music-2-srv
              port: 80
            - name: music-3-srv
              port: 80

You may still override this default on a per-Service basis.
