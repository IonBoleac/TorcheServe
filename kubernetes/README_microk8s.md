# Here i show you how to create and deploy a torchserve cluster on kubernetes cluster using microk8s
## 1) Install microk8s
In this step you can install microk8s. You can do it with this command:
```bash
sudo snap install microk8s --classic
```
That will return something like this:
```bash
microk8s (1.22/stable) v1.22.2 from Canonical✓ installed
```
## 2) Enable esentials microk8s addons
In this step you can enable microk8s addons. You can do it with this command:
```bash
microk8s enable dns dashboard storage helm helm3
```

## n) How to use Prometheus and Grafana on microk8s
In this step you can abilitate observability on microk8s. You can do it with this command:
```bash
microk8s enable observability
```
That will return something like this:
```bash
Infer repository core for addon observability
Addon core/dns is already enabled
Addon core/helm3 is already enabled
Addon core/hostpath-storage is already enabled
Enabling observability
Release "kube-prom-stack" does not exist. Installing it now.
NAME: kube-prom-stack
LAST DEPLOYED: Mon Dec 11 13:18:56 2023
NAMESPACE: observability
STATUS: deployed
REVISION: 1
NOTES:
kube-prometheus-stack has been installed. Check its status by running:
  kubectl --namespace observability get pods -l "release=kube-prom-stack"

Visit https://github.com/prometheus-operator/kube-prometheus for instructions on how to create & configure Alertmanager and Prometheus instances using the Operator.
Release "loki" does not exist. Installing it now.
NAME: loki
LAST DEPLOYED: Mon Dec 11 13:19:43 2023
NAMESPACE: observability
STATUS: deployed
REVISION: 1
NOTES:
The Loki stack has been deployed to your cluster. Loki can now be added as a datasource in Grafana.

See http://docs.grafana.org/features/datasources/loki/ for more detail.
Release "tempo" does not exist. Installing it now.
NAME: tempo
LAST DEPLOYED: Mon Dec 11 13:19:48 2023
NAMESPACE: observability
STATUS: deployed
REVISION: 1
TEST SUITE: None
[sudo] password for microk8s:

Note: the observability stack is setup to monitor only the current nodes of the MicroK8s cluster.
For any nodes joining the cluster at a later stage this addon will need to be set up again.

Observability has been enabled (user/pass: admin/prom-operator)
```
After this you can see all pods and services created with this command:
```bash
kubectl get po -A
kubectl get svc -A
```
## n) How to use Prometheus and Grafana on microk8s
In firt place you must create an ingress to access to grafana and prometheus. But before you must discovere the service name and port used by grafana and prometheus. You can do it with this command:
```bash
kubectl get svc -A | grep -E 'grafana|prometheus'
```
That will return something like this:
```bash
observability        kube-prom-stack-grafana                              ClusterIP   10.152.183.82    <none>        80/TCP
                                                                              74m
observability        kube-prom-stack-prometheus-node-exporter             ClusterIP   10.152.183.252   <none>        9100/TCP
                                                                              74m
observability        kube-prom-stack-kube-prome-prometheus                ClusterIP   10.152.183.174   <none>        9090/TCP
                                                                              74m
observability        prometheus-operated                                  ClusterIP   None             <none>        9090/TCP
                                                                              73m
```
Now you can create an ingress to access to grafana and prometheus. In this repo there is an example of ingress written in yaml and you can find this in this [path](./observability/ingress_grafana_observability.yaml). To deploy this ingress you can use this command:
```bash
kubectl apply -f observability/ingress_grafana_observability.yaml
```
After all these steps you can access to grafana and prometheus with this url:
```html
grafana.<ip>.nip.io
```
where the ip is the ip of your master kubernetes cluster and must be written correclty in the file ingres.yaml. You can find this ip with this command:
```bash
microk8s kubectl get nodes -o wide
```


