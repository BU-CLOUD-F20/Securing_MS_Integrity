# Regular Colors
Black='\033[0;30m'        # Black
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Blue='\033[0;34m'         # Blue
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan
White='\033[0;37m'        # White
NC='\033[0m'				


echo ${Purple}##############Securing Integrity of Micro-Service Builds on the Cloud - SIMS##############${NC}
#get all files from owner and developers
echo ${Purple}Downloading necessary files...${NC}
scp -r dstara@csa1.bu.edu:SIMS .
cd SIMS/owner
unzip *.zip
rm *.zip
rm -r __MACOSX/ ##if mac 
mv * ../..
cd ../developer/
unzip *.zip
rm *.zip
rm -r __MACOSX/
mv * ../..
cd ../..
rm -r SIMS

#push owner layout file to the server in order to be retrieved by the SISM pipeline 
#pending
echo ${Purple}Running the transformation...${NC}
python3 _standarize.py

echo ${Purple}Accessing the Kubernetes cluster...${NC}
export KUBECONFIG=../kubernetes_access/cluster_set_up_CONFIDENTIAL_IBM/kube-config-wdc04-gitsecure-wdc04-b3c.4x16.yml 

echo ${Purple}Applying SIMS files to the Tekton...${NC}
kubectl apply -f _task-clone-in-toto.yaml
kubectl apply -f intoto-task-verify.yaml
kubectl apply -f intoto-task-create-layout.yaml
kubectl apply -f intoto-task-clone-python-repo.yaml
kubectl apply -f intoto-task-pytest.yaml
kubectl apply -f pipeline.yaml
kubectl apply -f pipelinerun.yaml

echo ${Purple}The SIMS pipeline is now running. You can access it at: ${NC}
echo 
echo http://localhost:8001/api/v1/namespaces/tekton-pipelines/services/tekton-dashboard:http/proxy/
echo
kubectl proxy


