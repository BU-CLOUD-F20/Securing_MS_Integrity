** **

## Securing_MS_Integrity Project Proposal

## 1. Vision and Goals Of The Project:

Securing_MS_Integrity will be the verifier to ensure integrity of these [CI/CD](https://en.wikipedia.org/wiki/CI/CD) pipelines to ensure and enforce sanity of these security checks. High-Level Goals of pipeline include:

* Designing and building a solution wherein every task in the Tekton pipeline (unit test, vulnerability scan, license scan, etc.) will sign their results

* Building a verifier that could verify the output of the pipeline and ensure integrity

## 2. Users/Personas Of The Project

Securing virifier will be used by the researchers for companies and individuals who usually use cloud platforms to run tasks in CI/CD pipeline. It can be used in multiple systems, including Windows, Mac and Linux.

This project will not target the correctness of the pipeline itself. We are assuming that all the pipeline works perfectly and only cares about the integrity of them.

## 3. Scope and Features Of The Project:

Securing_MS_Integrity

find a solution to combine a framework “in-toto” and Tekton. 

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

Detailed user stories and plans are on the Trello board: https://trello.com/b/4EbylOXI/example-trello-board-for-moc-ui

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

