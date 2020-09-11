# Securing_MS_Integrity
Securing integrity of micro-service builds on Cloud

Project Logistics:
Mentors: Shripad Nadgowda email: nadgowda@us.ibm.com; 
Will the project be open source: yes
 
Preferred Past Experience:
Docker, Kubernetes: Required
Python/Go Programming: Required (at least one team member)
Tekton: Nice to have
Software Build Process: Valuable

Project Overview:
Background: DevOps has transformed and has brought an agility to whole software development practices for micro-service application through CI/CD workflows. DevSecOps has further the cause by embedding security right into these development workflows. It is now becoming critical to ensure integrity of these CI/CD pipelines to ensure and enforce sanity of these security checks. Thus, for example, if our CI pipeline we will ensure all required checks like unit tests, security scans, etc. are performed and their results are not tempered.
 
Project Specifics: In this project, we will explore use of an open source framework "in-toto" to build an integrity solution. And we will use cloud native CI/CD pipelines of Tekton to perform these experiments. We will design and build a solution wherein every task in the Tekton pipeline (unit test, vulnerability scan, license scan, etc.) will sign their results. And we will build a verifier that could verify the output of the pipeline and ensure integrity.

We would be using in-toto framework to ensure integrity of micro-service app builds
https://github.com/in-toto/in-toto 
We will integrate in-toto signing into cloud-native build pipeline "Tekton"
https://github.com/tektoncd/pipeline 




Some Technologies you will learn/use:
Agile Method
Git Workflows
Cloud Concepts Understanding
