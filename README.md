** **

## Securing Integrity of Micro-Service Builds on Cloud(SIMS) Project Proposal

## 1. Vision and Goals Of The Project:

SIMS will be the verifier to ensure the integrity of these [CI/CD](https://en.wikipedia.org/wiki/CI/CD) pipelines to ensure and enforce the sanity of these security checks. High-Level Goals of the pipeline include:

* Exploring the use of an open-source framework ["in-toto"](https://github.com/in-toto/in-toto) to build an integrity solution, which provides a framework to protect the integrity of the software supply chain. It does so by verifying that each task in the chain is carried out as planned, by authorized personnel only, and that the product is not tampered with in transit.

* Designing and building a solution wherein every task in the [Tekton](https://github.com/tektoncd/pipeline) pipeline (unit test, vulnerability scan, license scan, etc.) will sign their results. The Tekton Pipelines project provides k8s-style resources for declaring CI/CD-style pipelines.

* Building a verifier that could verify the output of the pipeline and ensure the integrity

## 2. Users/Personas Of The Project

* The securing verifier will be used by the researchers for companies and individuals who usually use cloud platforms to run tasks in CI/CD pipeline. It can be used in multiple systems, including Windows, Mac, and Linux.

* This project will not target the correctness of the pipeline itself. We are assuming that all the pipeline works perfectly and only cares about the integrity of them.

## 3. Scope and Features Of The Project:

SIMS

* find a solution to combine a framework “in-toto” and Tekton. 

## 4. Solution Concept

“In-toto” is used for giving each step of the pipeline a signature we used to validate it. 

* Each step of the pipeline will be signed. Before the next step being executed, it should verify the previous signature.

* If the previous signature doesn’t match its own, the system should stop the pipeline and report this issue to the user.

“Tekton” is used as a basic platform for running tests. It supports various programming languages and this project will not care about the test languages.

## 5. Acceptance criteria

Minimum acceptance criteria is a simple solution wherein every task in the Tekton pipeline will sign their results and a verifier to verify output of pipeline and ensure integrity. Stretch goals are:

* Get the signature from in-toto automatically and apply it to Tekton.

* Apply in-toto signature in every pipeline.

* A method to validate the signature and report the issues.

## 6. Release Planning

Release #1 (due by Oct.1):

In-toto and Tekton implementation.

Release #2 (due by Oct.15): 

Addition/modification/deletion of a VM into/in/from a Project:

Release #3 (due by Oct.29):

Addition/modification/deletion of a VM into/in/from a Project:

…
Release #4 (due by Nov.12):

…

Release #5 (due by Dec.3):

A final version of this release.

