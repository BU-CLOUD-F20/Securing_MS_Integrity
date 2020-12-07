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

## Demo Slides
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

* SIMS is dynamic and can work for a wide range of pipelines, assuming they are following the same guidlines. These are:
 * The users provide .yaml files
 * These .yaml files can create the tekton pipeline in kubernetes by just applying them to the cluster. We are taking care of the rest work and use in-toto.
  

## 4. Solution Concept

Assuming a software application that uses the Tekton pipeline:

* Whenever a developer pushes a new code, the new version of the application is transferred to the pipeline. 

* All tasks of the pipeline begin execution. As we mentioned before, each task can have many steps. After successful execution, each step is granted an automatic signature by in-toto. All proceeding steps will execute after that.

* At the end of the pipeline, a new final-task, created by SIMS will collect all previous signatures and decide about the integrity of the system.


![alt text](https://github.com/BU-CLOUD-F20/Securing_MS_Integrity/blob/master/Images/Flowchart.jpeg)


## 5. Project Architecture


SIMS has four main components which are operated by the _RUN.sh script. 
* The front-end interface to interact with users.
* The server which holds the data uploaded by users. 
* The tranformation function which modifies the original pipeline to the SIMS pipeline. As a reminder, when we refer to the SIMS pipeline, we mean the original pipeline combined with the in-toto signing framework.
* The final report which is visible in the Tekton dashboard. See below.

These components along with how they interact can be seen in the figure below:

image goes here------------------------


The front-end of our application shown as a blue screen is a flask application that enables interaction with the user. It runs locally in their computer and connects with our server to upload the files. 

The owner of the project only uploads the so-called "layout" file. This file is in json format and describes which developer is responsible for developing which step of the pipeline.

The developers of the project provide all the pipeline files along with another json file which describes who was the last person who modified each task.

The front-end looks like this:

image goes here --------------------------



The server component of SIMS is completely configurable and up to the user of our framework to decide. This de-centralized approach enables higher security as each user of SIMS can choose where to store the data uploaded by the users. Our implementation uses scp to transfer the files in the most secure way. (Credentials need to be given for this to work, more details in the instructions)


The transformation function is the heart of SIMS. Its job is to take the input pipeline and tranform it to the SIMS pipeline. It is true that this task has many challenges as it needs to accomondate for different pipeline designs, files, coding styles, etc. We have done our best to make this function as good as possible. See future work for more details. 

As a very simplistic explanation you can see the following two images. 

The first shows a part of a .yaml that corresponds to a task in the original pipeline.

---------------image here

The second shows the modifications made after applying the transformation function. This file will now execute the original task, but this time using in-toto. To do that we are utilizing the Tekton-CLI https://github.com/tektoncd/cli which enables running tasks from the command line. This enables the integration of in-toto and Tekton!

-------------image here

At this point, the _RUN.sh script will take the modified files, access the kubernetes cluster and tun the pipeline. This kubernetes cluster needs to be created by the user and the cresentials should be added to the pipeline-set-up folder. During our project we found that setting up a kubernetes cluster can be quite cumbersome. For this reason, along with our framework we provide a simple guide to create a kubernetes cluster! See the designated section at the end of this document.


The final report of the project can be accesed by the computer that ran the pipeline.

















## 6. Acceptance criteria

SIMS is a simple project which evaluates the pipeline steps of a CI/CD application.

The user should be able to:

* Receive the pipeline evaluation without a significant penalty in execution time for using SIMS.

* Be able to easily locate possible issues and their cause.

## 7. Release Planning

Release #1 (due by Oct.1):

- Presentation of the basic structure of our system.
- Demo the basic Tekton pipeline and In-toto tutorial.

Release #2 (due by Oct.15): 

- In-toto and Tekton running side by side as two different entities in a demo example.

Release #3 (due by Oct.29):

- First effort to combine the two tools.

Release #4 (due by Nov.12):  

- Making our project more dynamic and finalizing the design.
  [Presentation](https://docs.google.com/presentation/d/1XITpx6Z8MM1a6SjzsVAiXFB_mVtW7o8iMjSJ3zij4LI/edit?usp=sharing)

Release #5 (due by Dec.3):

- Final version.

## 8. Execution Instructions

### Kubernetes
export KUBECONFIG=<kubeconfig_file>

For all tasks:
kubectl apply -f <task-file>.yaml

For the pipeline:
kubectl apply -f <pipeline-file>.yaml

For the pipeline run:
kubectl apply -f <pipeline-run-file>.yaml

To run the dashboard:
kubectl proxy

To launch the dashboard:
http://localhost:8001/api/v1/namespaces/tekton-pipelines/services/tekton-dashboard:http/proxy/

### In-toto

- **```in-toto-run```** : It is used to execute a step in the software supply chain. This can be anything relevant to the project such as tagging a release with ```git```, running a test, or building a binary. 

- **```in-toto-record```** : It works similar to ```in-toto-run``` but can be used for multi-part software supply chain steps, i.e. steps that are not carried out by a single command. 

- **```in-toto-verify```** : Verify on the final product.

- **```in-toto-sign```** : It is a metadata signature helper tool to add, replace, and verify signatures within in-toto Link or Layout metadata.

