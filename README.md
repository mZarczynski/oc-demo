# Openshift Origin live demo for JUG ZG
This are my side notes from presentation introducing Openshift Origin for [Java devs comumunity](https://www.meetup.com/Zielona-Gora-JUG/) which I gave at May 2017 in Zielona Góra, Poland.


## Prerequisites
Modern Linux distro (e.g. Ubuntu 16.04) with:
* [oc](https://github.com/openshift/origin/releases) and [minishift](https://github.com/minishift/minishift/releases) cli tools in your $PATH.
* VirtualBox


## Prepare playground
##### Start minishift instance with metrics:
```
minishift start --cpus 4 --memory 8192 --vm-driver virtualbox --metrics
```

##### Login and create project dev:
```
oc login -u developer -p developer
oc new-project dev
```

##### Import python docker image whitch is base image for my example app.
```
oc import-image python:2.7 --confirm
```

##### Create new application. It will create BuildConfig, Imagestram, DeploymentConfig and will run first build.
```
oc new-app --name jug python:2.7~https://github.com/mZarczynski/oc-demo --strategy=docker
```

##### Create Service by exposing DeploymentConfig:
```
oc expose dc/jug --port=8080
```

##### Create Route by exposing Service:
```
oc expose svc/jug
```

##### Check route DNS name:
```
oc get route jug -o template --template={{.spec.host}}
```
Output will be our base url. Adjust this in next steps.
For me it was http://jug-dev.192.168.99.100.nip.io

## Playing with Openshift mechanics

##### Open in web browser http://jug-dev.192.168.99.100.nip.io
You can examine environment variables which are available out of the box.

##### On second terminal start simulating some app load with simple bash loop:
```
export BASE_URL=http://jug-dev.192.168.99.100.nip.io
while true; do curl ${BASE_URL}/cpu/50/10000; done
```
You can observe how much time computation took and where (on which Pod/hostname).


##### Scale up and down app over web console or from cli:
```
oc scale --replicas=3 dc jug
```
Observe what "load loop" returns when you change No. instances. You should see that consecutive requests are spread accross instances.


##### Apply resource limits e.g. 0.1 Core, 64Mi RAM. It will trigger new deployment.
```
oc set resources dc/jug --limits=cpu=100m,memory=64Mi
```
Observe how computation time changed. It should take ~10x more time.


##### Add ReadinessProbe and LivenessProbe:
```
oc set probe dc/jug --readiness --liveness --get-url=http://:8080/ --initial-delay-seconds=5
```


##### Add autoscaling:
```
oc autoscale dc/jug --min=1 --max=10 --cpu-percent=20
```
After a while you should observe that 4-5 pods are running.


##### Double load with with starting another "load loop" on third terminal:
```
export BASE_URL=http://jug-dev.192.168.99.100.nip.io
while true; do curl ${BASE_URL}/cpu/50/10000; done
```
Observe autoscaler reaction.


##### Chaos monkey -like test by instantly killing random app instance every 5s:
```
while true; do  oc delete `oc get pod -l app=jug -o name | shuf -n1` --now=true; sleep 5; done
```



## Cleanup
```
minishift delete
rm -rf ~/.minishift
```
