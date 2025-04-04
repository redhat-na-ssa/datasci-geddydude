# Pytorch distributed workload on openshift

Instructions for scheduling a pytorch distributed workload on openshift using the kubeflow training operator. 

## Prerequites
1) Openshift cluster
2) with gpu-operator, rdma enabled.
3) network-operator, in our case the network operator only loads drivers.
4) ACSCtl needs to be disabled on plx switches. Disabling virtualization via the BIOS is one way to achive this.  
5) Using a machine config, update the ulimit settings for crio runtime to allow umlimited memory locking. 
6) nmstate operator 
7) A default storage class needs to be configured.

## Create a container based on the ngc pytorch container
You can install additonal dependencies within the container ahead of time with internet connectivity.
Ex.
- clone git repos
- install python or OS dependencies 

Then ingest into the environment and load to the local conatiner registry



## Deploy the training operator
If you have an additional instanaces of training-operator you might run into a conflicts, these can be forced. 

```
wget https://github.com/kubeflow/trainer/archive/refs/tags/v1.9.0.tar.gz
tar zxvf v1.9.0.tar.gz
oc kustomize ./trainer-1.9.0/manifests/overlays/standalone/ > training-operator-standalone-manifest.yaml

# Patch image reference for local mirror
sed -i 's|kubeflow/training-operator:v1-5170a36|master.cm.cluster:5000/kubeflow/training-operator:v1-5170a36|g' training-operator-standalone-manifest.yaml

###
## please note i still dont have the apline init container patch. I haven't found where that image is referenced yet.
###

oc apply --server-side --force-conflicts -f training-operator-standalone-manifest.yaml
```

## Build the training container
docker build . -t pytorch-example:v1

## Save the pytorch, training, and alpine container
podman save pytorch-example:v1 > pytorch-example-v1.tgz
podman pull alpine:3.10
podman save alpine:3:10 > alpine-3.10.tgz
podman pull kubeflow/training-operator:v1-5170a36 
podman save kubeflow/training-operator:v1-5170a36 > kubeflow-training-operator_v1-5170a36.tgz


## Create a customer namespace/project and switch to it
oc create namespace project-a
oc project project-a

## Modify namespace with additional permissions 
# There might be an undocumented security context settings that will need to be set, especially when deploying as a user versus the cluster admin

## Apply the pvc
oc apply -n project-a pvc.yaml

# Copy data if needed 
oc rsync ./local/data pytorch-dist-nccl-master-0:/data
## Apply the pytorch job configuration
oc apply -n project-a pytorch-job.yaml

## Monitor the pods
oc get pods -n project-a

## Check logs
oc logs -n project-a pytorch-dist-nccl-master-0
  
