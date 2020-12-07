** **

## Securing Integrity of Micro-Service Builds on Cloud (SIMS) Project Proposal

## Team Members:
Role | Name | Email
-----|------|------
Mentor/Client | Shripad J Nadgowda | nadgowda@us.ibm.com
Developer | Yanyu Zhang | zhangya@bu.edu
Developer | Ningrong Chen | noracnr@bu.edu
Developer | Tony Mark | marktony@bu.edu
Developer | Staratzis Dimitrios | dstara@bu.edu
Developer | Zhou Fang | fzx2666@bu.edu

## Demo Slides and videos
 **[[demo1]](https://docs.google.com/presentation/d/1_4JSYiK76KQaBABYYhgkLxFE3iWBXTWAEjPP7PzPB9g/edit?usp=sharing)
 [[demo2]](https://docs.google.com/presentation/d/1_4JSYiK76KQaBABYYhgkLxFE3iWBXTWAEjPP7PzPB9g/edit?usp=sharing)
 [[demo3]](https://docs.google.com/presentation/d/1_4JSYiK76KQaBABYYhgkLxFE3iWBXTWAEjPP7PzPB9g/edit?usp=sharing)
 [[demo4]](https://docs.google.com/presentation/d/1XITpx6Z8MM1a6SjzsVAiXFB_mVtW7o8iMjSJ3zij4LI/edit?usp=sharing)
 [[demo5]](https://docs.google.com/presentation/d/1n7f7zduryj3oxcrVPGeozEaQvAI089k6zvjfVk8Ep6s/edit?usp=sharing)
 [[demo5-video]](https://drive.google.com/file/d/1i4RSvhSm19UudXlbIGmSfWDnXf8baxEi/view?usp=sharing)**
 

## 1. Vision and Goals Of The Project:


CI/CD pipelines are very commonly used today, especially in the industry.
Companies use them to enable their developers to write and immediately it into a testing environment. 
This environment is called a pipeline. 
Pipelines usually run on clusters, for better performance. 
Out of all pipelines, we chose to work with Tekton, first introduced by Google.
The main advantage of Tekton is that it can run on the same Kubernetes cluster as the program that is tested. 
Other pipelines need to be configured in a different Kubernetes cluster. 
A pipeline consists of tasks and each task consists of a number of steps.
A newly pushed code that passes all tasks can be immediately deployed in the main branch of the application.
However, there is no known software today that automatically verifies the integrity and the correct execution of each task.
In this project, we introduce SIMS, a verifier for all steps of a pipeline that ensures integrity. 
Each step of every task is signed after execution. After executing all tasks, we use in-toto, developed by NYU, to verify whether these tasks where the ones that were supposed to be executed. To make this verification we also use a file provided by the owner of the project.


## 2. Users/Personas Of The Project

* Our verifier will be used by company researchers and individuals who usually use cloud platforms to run tasks in CI/CD pipelines. It can be used in all major Operating Systems, including Windows, Mac, and Linux.
  

* Micro-service applications are being developed by multiple and distributed teams. SIMS provides a framework to establish trust between these teams and ensure secure collaboration.

* This project will not target the correctness of the pipeline itself. We are assuming the pipeline works perfectly. We only care about the integrity of each step.


## 3. Features Of The Project:

* Users are able to use SIMS easily. The output should provide a detailed report. 
 
* Users are able to see a log of previous pipeline executions

* The computational overhead of SIMS is minimal.

* SIMS is dynamic and can work for a wide range of pipelines, assuming they are following the same guidelines. These are:
 * The users provide .yaml files
 * These .yaml files can create the Tekton pipeline in Kubernetes by just applying them to the cluster. We are taking care of the rest work and use in-toto.
  

## 4. Solution Concept

Assuming a software application that uses the Tekton pipeline:

* Whenever a developer pushes a new code, the new version of the application is transferred to the pipeline. 

* All tasks of the pipeline begin execution. As we mentioned before, each task can have many steps. After successful execution, each step is granted an automatic signature by in-toto. All proceeding steps will execute after that.

* At the end of the pipeline, a new final-task, created by SIMS will collect all previous signatures and decide about the integrity of the system.

As you can see in the figure below, the success of the final verification task is completely unrelated to the success of the previously executed tasks. It is certainly possible to have a pipeline where all tasks are executed successfully, but the final verification fails.


![alt text](https://github.com/BU-CLOUD-F20/Securing_MS_Integrity/blob/master/Images/SIMS.png)


## 5. Project Architecture


SIMS has four main components which are operated by the _RUN.sh script. 
* The front-end interface to interact with users.
* The server which holds the data uploaded by users. 
* The transformation function which modifies the original pipeline to the SIMS pipeline. As a reminder, when we refer to the SIMS pipeline, we mean the original pipeline combined with the in-toto signing framework.
* The final report which is visible in the Tekton dashboard. See below.

These components along with how they interact can be seen in the figure below:


![alt text](https://github.com/BU-CLOUD-F20/Securing_MS_Integrity/blob/master/Images/design.png)


The front-end of our application shown as a blue screen is a flask application that enables interaction with the user. It runs locally in their computer and connects with our server to upload the files. 

The owner of the project only uploads the so-called "layout" file. This file is in json format and describes which developer is responsible for developing which step of the pipeline.

The developers of the project provide all the pipeline files along with another json file which describes who was the last person who modified each task.

The front-end looks like this:


![alt text](https://github.com/BU-CLOUD-F20/Securing_MS_Integrity/blob/master/Images/frontEnd.png)


The server component of SIMS is completely configurable and up to the user of our framework to decide. This de-centralized approach enables higher security as each user of SIMS can choose where to store the data uploaded by the users. Our implementation uses scp to transfer the files in the most secure way. (Credentials need to be given for this to work, more details in the instructions)


The transformation function is the heart of SIMS. Its job is to take the input pipeline and transform it to the SIMS pipeline. It is true that this task has many challenges as it needs to accommodate for different pipeline designs, files, coding styles, etc. We have done our best to make this function as good as possible. See future work for more details. 

The transformation is based on the fact that we can execute the original task utilizing the Tekton-CLI https://github.com/tektoncd/cli which enables running tasks from the command line. This enables the integration of in-toto and Tekton since in-toto is also a command line tool.

At this point, the _RUN.sh script will take the modified files, access the Kubernetes cluster and tun the pipeline. This Kubernetes cluster needs to be created by the user and the cresentials should be added to the kubernetes-set-up folder. During our project we found that setting up a Kubernetes cluster can be quite cumbersome. For this reason, along with our framework we provide a simple guide to create a Kubernetes cluster! See the designated section at the end of this document.


The final report of the project can be accessed by the computer that ran the pipeline. Instructions will be shown in the terminal to access the dashboard. It will look like this. 



![alt text](https://github.com/BU-CLOUD-F20/Securing_MS_Integrity/blob/master/Images/dashboard2.png)


You also have the ability to loo past pipeline executions.



![alt text](https://github.com/BU-CLOUD-F20/Securing_MS_Integrity/blob/master/Images/dashboard1.png)


## 6. Acceptance criteria

SIMS is a simple project which evaluates the pipeline steps of a CI/CD application.

The user should be able to:

* Receive the pipeline evaluation without a significant penalty in execution time for using SIMS.

* Be able to easily locate possible issues and their cause.


## 7. Execution Instructions

* First you need to clone our repo in your local machine

* Before you continue to the next steps, make sure you have a Kubernetes cluster up and running and you can access it with a pem key. This means that you need to have two files. One which will be the configuration of the cluster as a .yaml file and the pem key. To make your life easier we have provided some template files in the Kubernetes folder. You only need to modify these files to point to your cluster. 

* Then make sure that you have access to a Linux server. This server will be the SIMS server which is responsible for keeping the files that the users will upload. 

* Then you will need to open the upload.py file which is located inside the service folder. This file is responsible for the front-end that you need to send to your users. Before that you need to edit it and add the credentials for the server that you will be using. (We know that this part of the framework needs improvement. Of course, we do not want to give the server credentials to the people that will be using the framework. See future work for more details)

* When using the front-end make sure that you only upload zip files. For the developers upload a zip file named developer.zip. For the owner upload a file named owner.zip.

* Next, you should be able to go in the transformation folder and simply run the .RUN.sh. This script will download the data from the server, transform the files to be able to run the SIMS pipeline, configure the Kubernetes cluster, and finally provide instructions to access the dashboard which will contain the final report.

## 8. Bonus, Kubernetes cluster set-up

* Spin up some VMs in cluster. You can use MOC for that. 
	See instructions here on how to create a cluster: https://docs.massopen.cloud/en/latest/openstack/OpenStack-Tutorial-Index.html?fbclid=IwAR2a5ROUvW39n9jfbD3SNtbqmmGcAkS9HDCY3m3nEMjl0uwH3CqNWd0ZHpk

* Install docker on all VMs
	curl -sSL https://get.docker.com | sh -
 
* Setup passwordless ssh between machines as described in the tutorial above.

* Install kubeadm on all your nodes

	apt-get update && apt-get install -y apt-transport-https curl
	curl -s https://packages.cloud.google.com/apt/doc/	apt-key.gpg | apt-key add -
	cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
	deb https://apt.kubernetes.io/ kubernetes-xenial main
	EOF
	apt-get update
	apt-get install -y kubelet kubeadm kubectl
	apt-mark hold kubelet kubeadm kubectl
 
* Restart kubelet

	systemctl daemon-reload
	systemctl restart kubelet

* Disable swapp (Do not skip this step)
 	swapoff -a 

* Run kubeadm init on master node with correct network policy

 	kubeadm init —pod-network-cidr=192.168.0.0/16
	
* To start using your cluster, you need to run the following as a regular user:
	
	mkdir -p $HOME/.kube
	sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config 
	sudo chown $(id -u):$(id -g) $HOME/.kube/config
	
* From the worker nodes, join the master
	
	kubeadm join 10.144.101.177:6443 --token 5zwx6w.q8c2vyn7cpu0e5um --discovery-token-ca-cert-hash sha256:fc24fc1c641cc9758f01415063562b0392eff5d5ddf11ad3e7f046badb06ff8a
	
* Label the worker nodes

	kubectl label node mowgli2.sl.cloud9.ibm.com node-role.kubernetes.io/worker=worker
	kubectl label node mowgli3.sl.cloud9.ibm.com node-role.kubernetes.io/worker=worker

* Make sure all nodes are ready

	root@mowgli1:~# kubectl get nodes
	NAME                        STATUS   ROLES    AGE   VERSION
	mowgli1.sl.cloud9.ibm.com   Ready    master   78m   v1.13.2
	mowgli2.sl.cloud9.ibm.com   Ready    worker   75m   v1.13.2
	mowgli3.sl.cloud9.ibm.com   Ready    worker   34s   v1.13.2

* if you observe nodes are not ready, apply network controller
 	kubectl apply -f https://docs.projectcalico.org/v3.7/manifests/calico.yaml
 
## 9.Future work
 
 
