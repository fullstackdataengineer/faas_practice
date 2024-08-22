# Azure Functions Practice  

First, create a docker image with Azure Functions Core Tools:  


```
cd core_tools  
docker build -t func_core_tools .
```   

Go back to the faas_practice directory:  

```   
cd ..
pwd
```   

Then, spin up a container exposing faas_practice as a volume. Try to understand each flag in the docker run command:  



```
CONTAINER_NAME=$(whoami)_faas_$(date +%Y%m%d%H%M%S)
docker run -d --rm \
  --name $CONTAINER_NAME \
  -v /etc/passwd:/etc/passwd:ro \
  -v /etc/group:/etc/group:ro \
  -v ${PWD}:/home/$(whoami) \
  --workdir=/home/$(whoami) \
  --user $(id -u):$(id -g) \
  func_core_tools tail -f /dev/null
```    

The recommended way to work on your container it is use [Visual Studio Code Development Containers](https://microsoft.github.io/code-with-engineering-playbook/developer-experience/devcontainers/).  


Your practice files are scattered across different directories, for example :  /faas_practice/1_http_trigger_practice.  
Follow README.md on each practice directory and try to get the function to work on the Azure portal.  