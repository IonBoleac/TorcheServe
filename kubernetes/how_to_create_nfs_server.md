# In this file we will create a NFS server
We use this NFS server to store our data for kubernetes cluster. 
## Install NFS server
```bash
sudo apt-get install nfs-kernel-server
```
## Create a directory for NFS server
```bash
sudo mkdir -p /media/nfs # create a directory for NFS server that will be shared with all clients
```
## Configure exports file
```bash
sudo nano /etc/exports
```
Add the following line to the file and save it. See [this](https://linuxconfig.org/how-to-configure-nfs-on-linux) for more and to understand the significate of each option.
```bash
/media/nfs *(rw,sync,no_subtree_check)
```
Load the new configuration
```bash
sudo exportfs -arv
```
## Finish
Now we have a NFS server that can be used by all clients. In this repo we are using it for kubernetes cluster like a persistent volume. See [this](pv_nfs.yaml).