# Webhook Router
An application that accepts incoming webhooks and forwards them to internal/external locations.

#### Run Docker container
Get your target webhook url add as environment variable.
```
$ docker run -d -p 5000:5000 \
             --env WEBHOOK_URI= < target webhook url > \
             --name webhook-router \
	     srinisbook/webhook-router:latest
```
Send a test post with curl command:
```
$ curl --header "Content-Type: application/json" \
       --request POST   --data '{"text":"Hello, This post forwarded through webhook-router"}' \ 
       http://127.0.0.1:5000/webhook
```
#### Run on Kubernetes
Deployment manifest
```
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  labels:
    app: webhook-router
  name: webhook-router
spec:
  replicas: 1
  selector:
    matchLabels:
      app: webhook-router
  template:
    metadata:
      labels:
        app: webhook-router
    spec:
      containers:
      - image: srinisbook/webhook-router:latest
        imagePullPolicy: Always
        name: webhook-router
        env:
        - name: WEBHOOK_URI
          value: "< target webhook url>"
        ports:
        - containerPort: 5000
          name: webhook-router
        resources: {}
```
Service manifest:
```
apiVersion: v1
kind: Service
metadata:
  labels:
    app: webhook-router
  name: webhook-router
spec:
  ports:
  - port: 80
    name: webhook-router
    protocol: TCP
    targetPort: 5000
  selector:
    app: webhook-router
  type: ClusterIP
```
Use http://webhook-router/webhook as endpoint in the same namespace.

If your application and webhook-router deployed in differenet namespaces, use  http://webhook-router.< namespace >.svc.cluster.local/webhook
