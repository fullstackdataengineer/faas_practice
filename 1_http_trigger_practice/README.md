# HTTP Trigger Practice  

## Function and Environment Setup:  

### Create Python 3.10 Virtual Environment  

```
python3.10 -m venv .venv
source .venv/bin/activate
```  

### Initializa Azure Function App Environment  

We will use Python Programming Reference model V2, which is the most recent one based on Python decorators.  

```func init SimpleHTTP --worker-runtime python --model V2```    
```cd SimpleHTTP```  

### Create HTTP Trigger Function: simple  

```func new --name simple --template "HTTP trigger"```  

For Auth Level, choose ANONYMOUS.

### Install Python dependencies on virtual environment:  

```pip install --no-cache-dir -r requirements.txt  ```  

## Test Function Locally

A function can be tested locally running:  

```func start  ```    

On a different Terminal, you may use curl to call the function and get responses.  

## Azure Setup  

Azure Function:


1. Create a random ID  

```export randomId=$(cat /dev/urandom | env LC_ALL=C tr -dc 'a-z0-9' | fold -w 11 | head -n 1)```  

In this run, the value was: e5u66mj92zr  

2. Log on to Azure  

```az login --use-device-code ```  
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
     --runtime-version 3.11 \
     --functions-version 4 \
     --resource-group $resource \
     --name SimpleHTTP$randomId \
     --os-type linux \
     --storage-account ${storageaccount}
```  

6. Publish your Function App to Azure:  

```  
func azure functionapp publish SimpleHTTP$randomId
```  

This command may take +15 minutes to complete. When it is done, information about the Function App from your browser using the supplied "Invoke url". This should work without any authentication as we set the Auth Level to ANONYMOUS.  

Now, log on to the Azure Portal and check your Function App. Test it using the browser from the Azure Portal.  
