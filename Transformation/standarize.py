import os
from enum import Enum
import re
import json

class Type(Enum):
  Task = 1
  TaskRun = 2
  Pipeline = 3
  PipelineRun = 4
  PersistentVolumeClaim = 5
  PipelineResource = 6

fields = ['apiVersion','kind','metadata','spec','steps','stepTemplate','description','params','resources','inputs','outputs','workspaces','results','volumes','volumeMounts','stepTemplate','sidecars','name','namespace','type','default','image','args','command','volumeMounts','mountPath','emptyDir','taskRef','tasks','script','timeout','value','resources','env','targetPath','securityContext','privileged','workingDir','hostPath','configMap','valueFrom','secretKeyRef','key','runAsUser','generateName','podTemplate','runAsNonRoot','taskSpec']
workspaces = {}
# Transfer existing file to intoto version
def standarize():
  # Read users' json
  jsonfile =  open('tasks_commands.json','r')
  commands = json.loads(jsonfile.read())
  jsonfile.close()
  # Deal with all yamls
  for filename in os.listdir(os.getcwd()):
    if "yaml" not in filename:
      continue
    if "intoto-" in filename:
      continue 
    with open(os.path.join(os.getcwd(), filename),'r') as f:
      Lines = f.readlines()
      print(filename)
      
      filetype = 0
      for line in Lines:
        if line.startswith("kind"):
          if "Task" in line:
            filetype = Type.Task
            break
          elif "PipelineRun" in line:
            filetype = Type.PipelineRun
            break
          elif "Pipeline" in line:
            filetype = Type.Pipeline
            break
          elif "PersistentVolumeClaim" in line:
            filetype = Type.PersistentVolumeClaim
            break
          else:
            print(line)
      # When file type is task, modify to intoto version if need
      if filetype == Type.Task:
        modify_flag = False
        startflag_metadata = False
        origin_name =""
        startflag_workspace = False
        for idx,line in enumerate(Lines):
          if "workspace" in line:
            startflag_workspace = True
          if startflag_workspace:
              if "name:" in line:
                temp_list_workspaces = line.rstrip().split("name:")
                workspaces["name"] = temp_list_workspaces[1].strip()
              if "mountPath:" in line:
                temp_list_workspaces = line.rstrip().split("mountPath:")
                workspaces["mountPath"] = temp_list_workspaces[1].strip()
              if "name" in workspaces and "mountPath" in workspaces:
                startflag_workspace = False
          if "metadata" in line:
            startflag_metadata = True
          if startflag_metadata:
            if "name:" in line:
              temp_list = line.rstrip().split("name:")
              origin_name = temp_list[1].strip()
              startflag_metadata = False
            # TODO: Deal with situation that no name field in metadata
        if startflag_workspace:
          raise FileError("No Valid Field: Workspaces dont have name or mouthPath")
        # check if the file need to modify or not
        if origin_name == '':
          raise FileError("No Valid Field:Task file's lack of metadata-name field")
        else:
          print("origin_name: ",origin_name)
        print(commands)
        key_owner = ""
        step_name = ""
        command = ""
        for key, value in commands.items():
          # TODO: when value is empty
          for k,v in value.items():
            if k == origin_name:
              step_name = origin_name
              key_owner = key
              command = v
              modify_flag = True
        if modify_flag:
          # Create a new Task by adding intoto part
          newTaskFile = open("intoto-"+filename,'w')
          argsLines = []
          startflag_args = False
          # change matadata's name and split args part
          for idx,line in enumerate(Lines):
            if startflag_args:
              argsLines.append(line)
            if "metadata" in line:
              startflag_metadata = True
            if startflag_metadata:
              if "name:" in line:
                line = line.rstrip()+"-intoto\n"
                startflag_metadata = False
              # TODO: Deal with situation that no name field in metadata
            if not startflag_args:
              newTaskFile.write(line)
            if idx > len(Lines) -1:
              startflag_args = False
              idx_args = idx
              break
            temp_list_fields = Lines[idx+1].strip().split(":")
            if "args" in line:
              startflag_args = True
            elif temp_list_fields[0] in fields and startflag_args:
              startflag_args = False
              idx_args = idx
              break
          # deal with argsLines
          indent_spaces = ''
          print(argsLines)
          for idx,line in enumerate(argsLines):
            tmp = line.strip()
            if ":" in tmp:
              tmp_list_fields = tmp.split(":")
              if tmp_list_fields[0] in fields:
                continue
            if "pipefail" in tmp:
              temp_list = line.split("set")
              indent_spaces = temp_list[0]
              continue
            elif tmp == '\n':
              continue
            elif tmp != '' and tmp[0].isalpha():
              line = indent_spaces
              line += "- |\n"
              line += indent_spaces
              line += "set -e pipefail\n"
              line += indent_spaces
              line +="pip install in-toto\n"
              line += indent_spaces
              line +="cd in-toto/flat-directory\n"
              line += indent_spaces
              line +="echo 'installing down'\n"
              line += indent_spaces
              line +="curl -LO https://github.com/tektoncd/cli/releases/download/v0.8.0/tkn_0.8.0_Linux_x86_64.tar.gz\n"
              line += indent_spaces
              line +="su -\n"
              line += indent_spaces
              line +="tar xvzf tkn_0.8.0_Linux_x86_64.tar.gz -C /usr/local/bin/ tkn\n"
              line += indent_spaces
              line +="in-toto-run --verbose --step-name "+step_name+" --products intro-to-pytest --key "+key_owner+" -- "+command
              line +="\n"
              newTaskFile.write(line)
              break
          print(argsLines)
          # write rest of lines in output file
          for line in Lines[idx_args:]:
            newTaskFile.write(line)
          newTaskFile.close()
          
      # # Add intoto tasks
      # if filetype == Type.Pipeline:
      #   continue
      # # Add relavant params about intoto tasks
      # if filetype == Type.PipelineRun:    
      #   continue

# create new tasks:create-layout,verify
def createTasks():
  # Get Origin task
  for filename in os.listdir(os.getcwd()):
    if "yaml" not in filename:
      continue
    if "intoto-" in filename:
      continue 
    with open(os.path.join(os.getcwd(), filename),'r') as f:
      Lines = f.readlines()
      print(filename)
      filetype = 0
      for line in Lines:
        if line.startswith("kind"):
          if "Task" in line:
            filetype = Type.Task
            break
      # When file type is task, modify to intoto version if need
      if filetype == Type.Task:
        startflag_metadata = False
        origin_name =""
        for idx,line in enumerate(Lines):
          if "metadata" in line:
            startflag_metadata = True
          if startflag_metadata:
            if "name:" in line:
              temp_list = line.rstrip().split("name:")
              origin_name = temp_list[1].strip()
              startflag_metadata = False
            # TODO: Deal with situation that no name field in metadata
        if origin_name == '':
          raise FileError("No Valid Field:Task file's lack of metadata-name field")
          continue
        # Create a new Task by adding intoto part
        TaskVerify = open("intoto-task-verify.yaml",'w')
        TaskCreateLayout = open("intoto-task-create-layout.yaml",'w')
        argsLines_TaskVerify = []
        startflag_args = False
        startflag_stepsname = False
      #TaskVerify: change name and split args part
        for idx,line in enumerate(Lines):
          if startflag_args:
            argsLines_TaskVerify.append(line)
          if "metadata" in line:
            startflag_metadata = True
          if startflag_metadata:
            if "name:" in line:
              origin_list = line.split("name:")
              line = origin_list[0]+"name: task-verify\n"
              startflag_metadata = False
            # TODO: Deal with situation that no name field in metadata
          if "steps" in line:
            startflag_stepsname = True
          if startflag_stepsname:
            if "name:" in line:
              origin_list = line.split("name:")
              line = origin_list[0]+"name: task-verify\n"
              startflag_stepsname = False
            # TODO: Deal with situation that no name field in steps
          if not startflag_args:
            TaskVerify.write(line)
          if idx > len(Lines) -1:
            startflag_args = False
            idx_args = idx
            break
          temp_list_fields = Lines[idx+1].strip().split(":")
          if "args" in line:
            startflag_args = True
          elif temp_list_fields[0] in fields and startflag_args:
            startflag_args = False
            idx_args = idx
            break
        argsLines_TaskCreateLayout = []
      # TaskCreateLayout: change names
        for idx,line in enumerate(Lines):
          if startflag_args:
            argsLines_TaskCreateLayout.append(line)
          if "metadata" in line:
            startflag_metadata = True
          if startflag_metadata:
            if "name:" in line:
              origin_list = line.split("name:")
              line = origin_list[0]+"name: task-create-layout\n"
              startflag_metadata = False
            # TODO: Deal with situation that no name field in metadata
          if "steps" in line:
            startflag_stepsname = True
          if startflag_stepsname:
            if "name:" in line:
              origin_list = line.split("name:")
              line = origin_list[0]+"name: task-create-layout\n"
              startflag_stepsname = False
            # TODO: Deal with situation that no name field in steps
          if not startflag_args:
            TaskCreateLayout.write(line)
          if idx > len(Lines) -1:
            startflag_args = False
            idx_args = idx
            break
          temp_list_fields = Lines[idx+1].strip().split(":")
          if "args" in line:
            startflag_args = True
          elif temp_list_fields[0] in fields and startflag_args:
            startflag_args = False
            idx_args = idx
            break
      # deal with argsLines
        indent_spaces = ''
        #print(argsLines_TaskVerify)
        #print(argsLines_TaskCreateLayout)
        for idx,line in enumerate(argsLines_TaskVerify):
          tmp = line.strip()
          if ":" in tmp:
            tmp_list_fields = tmp.split(":")
            if tmp_list_fields[0] in fields:
              continue
          if "pipefail" in tmp:
            temp_list = line.split("set")
            indent_spaces = temp_list[0]
            continue
          elif tmp == '\n':
            continue
          elif tmp != '' and tmp[0].isalpha():
            line = indent_spaces
            line += "- |\n"
            line += indent_spaces
            line += "set -e pipefail\n"
            line += indent_spaces
            line +="pip install in-toto\n"
            line += indent_spaces
            line +="cd in-toto/flat-directory\n"
            line += indent_spaces
            verify_line = line+"in-toto-verify --verbose --layout root.layout --layout-key alice.pub\n"
            TaskVerify.write(verify_line)
            clone_line = line+"python create_layout.py\n"
            TaskCreateLayout.write(clone_line)
            break
        #print(argsLines_TaskVerify)
        # write rest of lines in output file
        for line in Lines[idx_args:]:
          TaskVerify.write(line)
          TaskCreateLayout.write(line)
        TaskVerify.close()
        TaskCreateLayout.close()
        #print("结束"+filename)
        break
        
  # TaskCloneIntoto: append workspace (only run once)
  flag_TaskCloneIntoto = True
  TaskCloneIntotoR = open("task-clone-in-toto.yaml",'r')
  for l in TaskCloneIntotoR.readlines():
    if "workspaces:" in l:
      flag_TaskCloneIntoto = False
  if flag_TaskCloneIntoto:
    TaskCloneIntoto = open("task-clone-in-toto.yaml",'a+')
    new_workspaces = "  workspaces:\n    - name: "+workspaces["name"]+"\n      mountPath: "+workspaces["mountPath"]+"\n"
    TaskCloneIntoto.write(new_workspaces)




if __name__ == "__main__":
    # execute only if run as a script
    standarize()
    createTasks()
