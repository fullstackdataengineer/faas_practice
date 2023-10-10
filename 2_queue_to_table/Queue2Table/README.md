# PRACTICE: Queue 2 Table Azure Function  


```
cd Queue2Table
```  

## Create Python 3.9 Virtual Environment  

```
python3.9 -m venv .venv
source .venv/bin/activate
```  

## Install Python dependencies on virtual environment:  

```pip install --no-cache-dir -r requirements.txt  ```  

requirements.txt must be as follows:  

```
azure-functions
```  

## Create new Function App  
 
### Initializa Azure Function App Environment  

We will use Python Programming Reference model V1. There is a recent model (V2) based on Python decorators that is out of the scope of this Lab.  

```func init Queue2Table --python -m V1  ```    
```cd Queue2Table```

Azure Table only support [Extension Bundle](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-storage-table?tabs=in-process%2Ctable-api%2Cextensionv2&pivots=programming-language-python#install-bundle) v2.x as of this writting, therefore version in host.json must be set to:  

```[2.*, 3.0.0)```  

```cp ../src/host.json .```  

Reference: https://techcommunity.microsoft.com/t5/azure-storage/error-while-trying-to-write-in-azure-tables-is-not-a-valid-value/m-p/3591032  

```func new --name Queue2Table --language python  ```  

Because we did not select a Template, we are prompted for one. Azure Queue Storage trigger is chosen:  
```(.venv) root@f8df55684e67:/function# func new --name Queue2Table  --template "Azure Queue Storage trigger" --language python
Select a number for template:queueTrigger
Can't find template "queueTrigger" in "python"
(.venv) root@f8df55684e67:/function# func new --name Queue2Table   --language python
Select a number for template:
1. Azure Blob Storage trigger
2. Azure Cosmos DB trigger
3. Durable Functions activity
4. Durable Functions entity
5. Durable Functions HTTP starter
6. Durable Functions orchestrator
7. Azure Event Grid trigger
8. Azure Event Hub trigger
9. HTTP trigger
10. Kafka output
11. Kafka trigger
12. Azure Queue Storage trigger
13. RabbitMQ trigger
14. Azure Service Bus Queue trigger
15. Azure Service Bus Topic trigger
16. Timer trigger
Choose option: 12
Azure Queue Storage trigger
Function name: [QueueTrigger] Writing /function/Queue2Table/readme.md
Writing /function/Queue2Table/__init__.py
Writing /function/Queue2Table/function.json
The function "Queue2Table" was created successfully from the "Azure Queue Storage trigger" template.
Did you know? There is a new Python programming model in public preview. For fewer files and a decorator based approach, learn how you can try it out today at https://aka.ms/pythonprogrammingmodel
```  

deploy Funcion code:  

```
cp ../src/__init__.py Queue2Table/  
cp ../src/function.json Queue2Table/   
```  

## Create a random ID  

```export randomId=$(cat /dev/urandom | env LC_ALL=C tr -dc 'a-z0-9' | fold -w 11 | head -n 1)```  
```echo $randomId```  

## Azure login  

```az login ```  
Follow the steps, which involve browsing too https://microsoft.com/devicelogin and inserting a code.  

```az account set --subscription e0b9cada-61bc-4b5a-bd7a-52c606726b3b ``` 

```export resource=IE_ST_BCSAI_DUD_STUDENT```  

Run this if you want to create a new Resource Group:  
```az group create --name $resource --location eastus```  

## Create Storage Account or Use an existing one  

```export storageaccount=lesson$randomId```  
```echo $storageaccount```  

Run this if you need to create a new Storage Account:  

```  
az storage account create \
    --name $storageaccount \
    --resource-group $resource \
    --sku Standard_LRS
```  


## Create Function App named Queue2TableInstr$randomId. A function App may contain multiple functions  

```  
az functionapp create --consumption-plan-location eastus \
     --runtime python \
     --runtime-version 3.9 \
     --functions-version 4 \
     --resource-group $resource \
     --name Queue2TableInstr$randomId \
     --os-type linux \
     --storage-account ${storageaccount}
```  

Now, we have to setup the connection to Azure Queue and Azure Table, which in functions.json appear as:  

* AzureQueueStorage  
* AzureTableStorage  

Grab the Connection String from respective Azure Storage Accounts (available via Access keys).  
Go to Configuration and click "New application setting".  

```  
AzureQueueStorage=DefaultEndpointsProtocol=https;AccountName=iestdudbstudent0001;AccountKey=0hv/Rayb4a4rMoMXHgRMP6l7N882ied5EXAMPLE;EndpointSuffix=core.windows.net

AzureTableStorage=DefaultEndpointsProtocol=https;AccountName=iestdudbstudent0001;AccountKey=0hv/Rayb4a4rMoMXHgRMP6l7N882ied5yEAJOhsB18UlaWpnEXAMPLE;EndpointSuffix=core.windows.net
```  

You should also create the relevant Queue and Table on Azure Portal. The names are in function.json:  
```  
queueName: python-queue-items    
tableName: outTable  
```  

## You can now test the function locally:  

1. Deploy Function settings into local.settings.json  

```  
func azure functionapp fetch-app-settings Queue2TableInstr$randomId  
func azure storage fetch-connection-string $storageaccount  
cat local.settings.json
```  

2. Run:  

```  
func start
```  

3. Add a message to the target queue and make sure the content is written to the output Azure Table  


Finally, we are ready to publish our Function code to the Azure Function App:  

```  
func azure functionapp publish Queue2TableInstr$randomId --python  
```  
