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
 [demo1](https://docs.google.com/presentation/d/1_4JSYiK76KQaBABYYhgkLxFE3iWBXTWAEjPP7PzPB9g/edit?usp=sharing)
 [demo2](https://docs.google.com/presentation/d/1_4JSYiK76KQaBABYYhgkLxFE3iWBXTWAEjPP7PzPB9g/edit?usp=sharing)
 [demo3](https://docs.google.com/presentation/d/1_4JSYiK76KQaBABYYhgkLxFE3iWBXTWAEjPP7PzPB9g/edit?usp=sharing)
 

## 1. Vision and Goals Of The Project:


CI/CD pipelines are very commonly used today, especially in the industry.
Companies use them to enable their developers to write and immediately it into a testing environment. 
This environment is called a pipeline. 
Pipelines usually run on clusters, for better performance. 
Out of all pipelines, we chose to work with Tekton, first introduced by Google.
The main advantage of Tekton is that it can run on the same Kubernetes cluster as the program that is tested. 
Other pipelines need to be configured in a different Kubernetes cluster. 
A pipeline consists of tasks and each task consists of a number of tests.
A newly pushed code that passes all tasks can be immediately deployed in the main branch of the application.
However, there is no known software today that automatically verifies the integrity and the correct execution of each task.
In this project, we introduce SIMS, a verifier for all steps of a pipeline that ensures integrity. 
Each step of every task is signed by the project developer in an automated way. To do that, we use in-toto, developed by NYU.


## 2. Users/Personas Of The Project

* Our verifier will be used by company researchers and individuals who usually use cloud platforms to run tasks in CI/CD pipeline. It can be used in all major Operating Systems, including Windows, Mac, and Linux.

* This tool will be useful for clients who need to make sure that the application they are interested in has undergone sufficient testing.
We have not yet concluded how clients will have access to the result of our verifier.  

* Micro-service applications are being developed by multiple and distributed teams. SIMS provides a framework to establish trust between these teams and ensure secure collaboration.

* This project will not target the correctness of the pipeline itself. We are assuming the pipeline works perfectly. We only care about the integrity of each step.


## 3. Scope and Features Of The Project:

* Users should be able to use SIMS easily. The output should provide a detailed report. 
 
* Users will also be able to see a log of previous pipeline executions

* Users will be able to manually check the signature applied to the executed tests.

* The computational overhead of SIMS should be minimal in comparison to the pipeline cost.

## 4. Solution Concept

Assuming a software application that uses the Tekton pipeline:

* Whenever a developer pushes a new code, the new version of the application is transferred to the pipeline. 

* All tasks of the pipeline begin execution. As we mentioned before, each task can have many steps. After successful execution, each step is granted an automatic signature. All proceeding steps will execute after that. At this point, we should mention that we are going to enable users, to apply signatures both after each step or after each task, depending on their application characteristics.

* At the end of the pipeline, a new final-task, created by SIMS will collect all previous signatures and decide about the integrity of the system.

![alt text](https://github.com/BU-CLOUD-F20/Securing_MS_Integrity/blob/master/Images/Flowchart.jpeg)

## 5. Acceptance criteria

SIMS is a simple project which evaluates the pipeline steps of a CI/CD application.

The user should be able to:

* Receive the pipeline evaluation without a significant penalty in execution time for using SIMS.

* Be able to select between applying the in-toto signatures in every task or every step.

* Be able to easily locate possible issues and their cause.

## 6. Release Planning

Release #1 (due by Oct.1):

- Presentation of the basic structure of our system.
- Demo the basic Tekton pipeline and In-toto tutorial.

Release #2 (due by Oct.15): 

- In-toto and Tekton running side by side as two different entities in a demo example.

Release #3 (due by Oct.29):

- First effort to combine the two tools.

Release #4 (due by Nov.12):

- Hopefully a functional implementation of our project.

Release #5 (due by Dec.3):

- Final version.

## 7. Execution Instructions

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

