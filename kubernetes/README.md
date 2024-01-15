# How to deploy torchserve on kubernetes cluster in localhost using minikube
In this case i explane you how to create and deploy a torchserve cluster on kubernetes cluster in localhost using minikube. 
## 1) In first you must install minikube and kubectl
You can install minikube and kubectl follwing those commands. *Obbiously before this you shoulde install docker too and start it.* Anyway, you must install minikube and kubectl. You can do it with these commands:
- [minukube](https://minikube.sigs.k8s.io/docs/start/)
    ```bash
    curl -LO "https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64" && sudo install minikube-linux-amd64 /usr/local/bin/minikube
    ```
    
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
    ```bash
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    ```
## 2) Run minikube and test kubectl
You can run minikube but is needed to mount a localhost path that have all your project to be launched on torchserve. This because we use minikube that is a container and is needed bind all files situated on localhsot with minikube's container. To do this use this command:
```bash
minikube start --mount-string="$HOME/path-to-share:/where-to-mount-on-minikube-container" --mount
```
After this command terminal show you a message like this:
```bash
😄  minikube v1.32.0 on Ubuntu 22.04 (amd64)
✨  Using the docker driver based on existing profile
👍  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...
🔄  Restarting existing docker container for "minikube" ...
🐳  Preparing Kubernetes v1.28.3 on Docker 24.0.7 ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
🔎  Verifying Kubernetes components...
    ▪ Using image registry.k8s.io/metrics-server/metrics-server:v0.6.4
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
    ▪ Using image docker.io/kubernetesui/dashboard:v2.7.0
    ▪ Using image docker.io/kubernetesui/metrics-scraper:v1.0.8
💡  Some dashboard features require the metrics-server addon. To enable all features please run:

        minikube addons enable metrics-server


🌟  Enabled addons: storage-provisioner, default-storageclass, metrics-server, dashboard
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```
And you can test kubectl with this command:
```bash
kubectl cluster-info
```
This command should return something like this:
```bash
Kubernetes control plane is running at https://127.0.0.1:57064
CoreDNS is running at https://127.0.0.1:57064/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```
After that you may enable dashboard and additional metrics from minikube with this command:
```bash
minikube addons enable dashboard
minikube addons enable metrics-server
```
And you can start dashboard with this command:
```bash
minikube dashboard
```
This command should return something like this:
```bash
🤔  Verifying dashboard health ...
🚀  Launching proxy ...
🤔  Verifying proxy health ...
🎉  Opening http://127.0.0.1:45127/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/ in your default browser...
👉  http://127.0.0.1:45127/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/
```
## 3) Create all files needed to configure torchserve cluster on kubernetes
In this step you have to create all files needed to configure torchserve cluster on kubernetes. You can find all files in this repository. In particular you have to create:
- Deployments: Is the file that rappresent how your app should be wrapped in a container and deployed on kubernetes. You can find it in this repository at this path: [`kubernetes/deployment_torchserve.yaml`](deployment_torchserve.yaml). See [official documentation](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) for more details.
- Services: Is the file that rappresent how your app should be exposed to the outside world. You can find it in this repository at this path: [`kubernetes/service_torchserve.yaml`](service_loadbalancer_torchserve.yaml). See [official documentation](https://kubernetes.io/docs/concepts/services-networking/service/) for more details.
- Namespaces: Is the file that rappresent the namespace where your app should be circumscribed. You can find it in this repository at this path: [`kubernetes/name-spaces_torchserve.yaml`](name-space_torchserve.yaml). See [official documentation](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) for more details.
- Persistent Volume: Is the file that rappresent the persistent volume binded with your cluster. You can find it in this repository at this path: [`kubernetes/persistent-volume_torchserve.yaml`](pv.yaml). See [official documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) for more details.
- Persistent Volume Claim: Is the file that rappresent the specifics for a persistent volume that your pods they needed to use. You can find it in this repository at this path: [`kubernetes/pvClaim.yaml`](pvClaim.yaml). See [official documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) for more details.

In additional you can add more and more files to configure your cluster. For example you can add a file to configure a load balancer or a file to configure a ingress. Fore more about kubernetes you can read [official documentation](https://kubernetes.io/docs/home/).

## 4) Deploy torchserve cluster on kubernetes
In this step you have to deploy torchserve cluster on kubernetes. You can do it with these command to configure your cluster correctly:
```bash
kubectl apply -f kubernetes/name-spaces_torchserve.yaml
kubectl apply -f kubernetes/pv.yaml
kubectl apply -f kubernetes/pvClaim.yaml
kubectl apply -f kubernetes/deployment_torchserve.yaml
kubectl apply -f kubernetes/service_torchserve.yaml
```
After this you can see all pods and services created with this command:
```bash
kubectl get pods -n torchserve-cluster
kubectl get services -n torchserve-cluster
```
Given that we use minikube you must expose your service on localhost with bottom command that will return the endopoints to contact your cluster:
```bash
minikube service torchserve-service -n torchserve-cluster
```
Or do a port forwarding with this command:
```bash
kubectl port-forward service/torchserve-service 8080:8080 8081:8081 8082:8082 -n torchserve-cluster
```
In both case you must leave the terminal open to keep the service active. If you want stop the service you should close terminal or press `CTRL+C`.

## 5) Test torchserve cluster on kubernetes
In this step you can test torchserve cluster on kubernetes. You can do it with this command:
```bash
curl localhost:8080/ping
```
This command should return something like this:
```bash
{
  "status": "Healthy"
}
```
## 6) Now you can deploy your model on torchserve cluster on kubernetes
Now you can deploy your models on torchserve following all steps in this [README](../README.md) file. But you must be careful with the paths and the ports because you now are using cluster kubernetes runned on minikube that is a container. 

## 7) Stop minikube
In this step you can stop minikube. You can do it with this command:
```bash
minikube stop
```

## 8) Delete torchserve cluster on kubernetes
In this step you can delete torchserve cluster on kubernetes. You can do it with this command:
```bash
kubectl delete -f kubernetes/name-spaces_torchserve.yaml
kubectl delete -f kubernetes/pv.yaml
kubectl delete -f kubernetes/pvClaim.yaml
kubectl delete -f kubernetes/deployment_torchserve.yaml
kubectl delete -f kubernetes/service_torchserve.yaml
```

## 8.1) NFS server
I used an NFS server to share the models with all nodes of the cluster. To do this you must install NFS server on your machine and configure it correctly. You can do it with this command:
```bash
sudo apt install nfs-kernel-server
```
After this you must create a directory that will be shared with all nodes of the cluster. You can do it with this command:
```bash
sudo mkdir -p /media/nfs/
```
After this you must configure the NFS server to share the directory that you have created. You can do it with this command:
```bash
sudo nano /etc/exports
```
And add this line at the end of the file:
```bash
/media/nfs/ *(rw,sync,no_root_squash,no_subtree_check)
```
Where `/media/nfs/` is the path of the directory that you have created. See [this](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-20-04) for more. After this syep you must restart the NFS server with this command:
```bash
sudo systemctl restart nfs-kernel-server
```
Now you can create a persistent volume and a persistent volume claim to bind the NFS server with your cluster. You can do it with this command:
```bash
kubectl apply -f kubernetes/pv_nfs.yaml
kubectl apply -f kubernetes/pvClaim_nfs.yaml
```
Remember to copy the models in the directory that you have created. 
See the file [`kubernetes/pv_nfs.yaml`](./pv_nfs.yaml) and [`kubernetes/pvClaim_nfs.yaml`](./pvClaim_nfs.yaml) for more details of the configuration.

### CAVEAT
Make attention with the paths and if you use `minikube` you must be very careful and configure it properly. This because minikube is a container in docker. 

## 9) Delete minikube
In this step you can delete minikube and all files of him binded. You can do it with this command:
```bash
minikube delete
```

Ps. If you want you can use this repo to create a torchserve cluster on other cloud provider like AWS, GCP, Azure, etc, or on other kubernetes cluster. You should follow only the steps that isn't related to minikube. Ovbiously you must have a kubernetes cluster and configure it correctly for your needs.