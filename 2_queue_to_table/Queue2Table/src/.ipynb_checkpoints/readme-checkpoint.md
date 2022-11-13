# QueueTrigger - Python

The `QueueTrigger` makes it incredibly easy to react to new Queues inside of Azure Queue Storage. This sample demonstrates a simple use case of processing data from a given Queue.

## How it works

For a `QueueTrigger` to work, you provide a path which dictates where the queue messages are located inside your container.

## Learn more

We will create a Python 3.9 virtual environment to install dependencies required by our Function:

apt install -y python3.9-venv
python3.9 -m venv .venv
source .venv/bin/activate
pip install --no-cache-dir -r requirements.txt  

where requirements.txt contains:

azure-functions

## Create new Function App  

func init --worker-runtime python  

Azure Table only support [Extension Bundle](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-storage-table?tabs=in-process%2Ctable-api%2Cextensionv2&pivots=programming-language-python#install-bundle) v2.x as of this writting, therefore version in host.json must be set to:  

```[2.*, 3.0.0)```  

cp src/host.json .

Reference: https://techcommunity.microsoft.com/t5/azure-storage/error-while-trying-to-write-in-azure-tables-is-not-a-valid-value/m-p/3591032  

func new --name Queue2Table --language python  

Because we did not select a Template, we are prompted for one. Azure Queue Storage trigger is chosen:  
```(.venv) root@f8df55684e67:/function# func new --name Queue2Table  --template "queueTrigger" --language python
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

cp src/\_\_init\_\_.py Queue2Table/  
cp src/function.json Queue2Table/  

Azure login

az login -u $username -p $password 
az account set --subscription e0b9cada-61bc-4b5a-bd7a-52c606726b3b

resource=IE_ST_BCSAI_DUD_STUDENT
storageaccount=iestdudbstudent0001


az functionapp create --consumption-plan-location eastus \
     --runtime python \
     --runtime-version 3.9 \
     --functions-version 4 \
     --resource-group $resource \
     --name Queue2TableInstr \
     --os-type linux \
     --storage-account ${storageaccount}

Now, we have to setup the connection to Azure Queue and Azure Table, which in functions.json appear as:

* MY_QUEUE_STORAGE_ACCT_APP_SETTING  
* MY_TABLE_STORAGE_ACCT_APP_SETTING  

Grab the Connection String from respective Azure Storage Accounts (available via Access keys).
Go to Configuration and click "New application setting".

MY_QUEUE_STORAGE_ACCT_APP_SETTING=DefaultEndpointsProtocol=https;AccountName=iestdudbstudent0001;AccountKey=0hv/Rayb4a4rMoMXHgRMP6l7N882ied5yEAJOhsB18UlaWpnF7uzprr5hHTWeOOE8bZcV/mvlDZi+AStHMTDew==;EndpointSuffix=core.windows.net

MY_TABLE_STORAGE_ACCT_APP_SETTING=DefaultEndpointsProtocol=https;AccountName=iestdudbstudent0001;AccountKey=0hv/Rayb4a4rMoMXHgRMP6l7N882ied5yEAJOhsB18UlaWpnF7uzprr5hHTWeOOE8bZcV/mvlDZi+AStHMTDew==;EndpointSuffix=core.windows.net

Now, you can test the function locally:  

1. Deploy Function settings into local.settings.json  

func azure functionapp fetch-app-settings Queue2TableInstr  
cat local.settings.json

2. Run:  

func start

3. Add a message to the target queue and make sure the content is written to the output Azure Table  


Finally, we are ready to publish our Function code to the Azure Function App:  

func azure functionapp publish Queue2TableInstr --python  