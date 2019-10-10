# Prometheus-grafana

Fully fucntional monitoring solution for Kubernetes cluster.

***Create a single manifest file***
```
awk 'FNR==1 {print "---"}{print}' manifest/* > "prometheus_grafana_manifest.yaml"
```
***Install Promenetheus-Grafana Stack***
````
kubectl apply -f prometheus_grafana_manifest.yaml
````

***Get Grafana credentials:***
```
echo "Username: $(kubectl get secret grafana --namespace prometheus \
                 --output=jsonpath='{.data.admin-user}' | base64 --decode)"
echo "Password: $(kubectl get secret grafana --namespace prometheus \
                 --output=jsonpath='{.data.admin-password}' | base64 --decode)"
```
