# Transformation
    
    Change all files from developers to intoto version: modification and creation.

## General files (code and necessary files)
* standarize.py
* task_clone_in_toto.yaml
* developers' files for their project (like tasks, pipeline, pipelinerun)
* a owner.json file for assign keys and missions.

## A simple example

##### origin files(in tranformation-before)
* task-pytest.yaml
* task-clone.yaml
* pytest-pipeline.yaml
* pvc-claim.yaml
* pipelinerun.yaml
* owner.json

##### After run `python3 standarize.py`

##### new files
1. modified from original ones

- intoto-task-pytest.yaml  <--task-pytest.yaml
- intoto-task-clone.yaml   <--task-clone.yaml
- intoto-pytest-pipeline.yaml  <- pytest-pipeline.yaml
- intoto-pipelinerun.yaml   <-- pipelinerun.yaml

2. create new files for intoto

- task-clone-in-toto.yaml   
    - for  cloning intoto things 
    - only add workspace dynamically by origin task.
- intoto-task-create-layout.yaml 
    - for creating intoto layout depending on owner.json
- intoto-task-verify.yaml  
    - for verifying whole project.