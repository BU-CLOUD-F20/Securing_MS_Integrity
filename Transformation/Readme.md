# Transformation

### origin files
* task-pytest.yaml
* task-clone.yaml
* pytest-pipeline.yaml
* pvc-claim.yaml (don't need to change)
* pipelinerun.yaml
* owner.json

### new files
1. modified from original ones

- intoto-task-pytest.yaml  <--task-pytest.yaml
- intoto-task-clone.yaml   <--task-clone.yaml
- intoto-pytest-pipeline.yaml  <- pytest-pipeline.yaml
- intoto-pipelinerun.yaml   <-- pipelinerun.yaml

2. create new files for intoto

- task-clone-in-toto.yaml   for  cloning intoto things
- intoto-task-create-layout.yaml for creating intoto layout depending on owner.json
- intoto-task-verify.yaml  for verifying whole project.