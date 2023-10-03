# HTTP Trigger Practice  

## Function and Environment Setup:  

### Create Python 3.9 Virtual Environment  

```
python3.9 -m venv .venv
source .venv/bin/activate
```  

### Initializa Azure Function App Environment  

We will use Python Programming Reference model V1. There is a recent model (V2) based on Python decorators that is out of the scope of this Lab.  

```func init classifyHTTP --python -m V1  ```    
```cd classifyHTTP```
### Create HTTP Trigger Function: classify  

```func new --name classify --template "HTTP trigger" --authlevel "function"```  


A function can be tested locally running:  

```func start  ```    


### Move code to function directory:  

```cp ../src/* classify  ```  
```cp ../requirements.txt .  ```  

### Install Python dependencies on virtual environment:  

```pip install --no-cache-dir -r requirements.txt  ```  

requirements.txt must be as follows:  

```
azure-functions
requests
-f https://download.pytorch.org/whl/torch_stable.html
torch==1.12.0+cpu
torchvision==0.13.0+cpu
```  

## Azure Setup  


Azure Function:


1. Create a random ID  

```export randomId=$(cat /dev/urandom | env LC_ALL=C tr -dc 'a-z0-9' | fold -w 11 | head -n 1)```  

In this run, the value was: e5u66mj92zr  

2. Log on to Azure  

```az login ```  
Follow the steps, which involve browsing too https://microsoft.com/devicelogin and inserting a code.  

```az account set --subscription e0b9cada-61bc-4b5a-bd7a-52c606726b3b ```  
3. Create Resource Group or Use an existing one  

```export resource=IE_ST_BCSAI_DUD_STUDENT```  

Run this if you want to create a new Resource Group:  
```az group create --name $resource --location eastus```  

4. Create Storage Account or Use an existing one  

```export storageaccount=lesson$randomId```  

Run this if you want to create a new Storage Account:  
```  
az storage account create \
    --name $storageaccount \
    --resource-group $resource \
    --sku Standard_LRS
```  

5. Create Function App named ClassifyHTTP$randomId. A function App may contain multiple functions  

```  
az functionapp create --consumption-plan-location eastus \
     --runtime python \
     --runtime-version 3.9 \
     --functions-version 4 \
     --resource-group $resource \
     --name ClassifyHTTP$randomId \
     --os-type linux \
     --storage-account ${storageaccount}
```  

6. Publish your Function App to Azure:  

```  
func azure functionapp publish ClassifyHTTP$randomId --python
```  

This command may take +15 minutes to complete.  
