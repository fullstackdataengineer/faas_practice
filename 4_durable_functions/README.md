# Azure Durable Functions

Azure Durable Functions is an extension of Azure Functions that allows you to write stateful functions in a serverless compute environment. Durable Functions provide a way to define workflows in code, which can be composed of several functions. Unlike traditional Azure Functions, Durable Functions manage state, checkpoints, and restarts internally, enabling you to focus on your business logic without worrying about the complexities of state management.  

### Purpose:

    To simplify the development of complex, stateful, and long-running workflows.
    To provide a serverless solution for orchestrating multiple serverless functions.
    To facilitate the creation of durable, resilient, and scalable applications that require state management and coordination between functions.

### Key Features:

    Orchestration:
        Workflow Definition: Allows defining workflows in code where functions can be chained together, execute in parallel, or wait for external events.
        Orchestrator Function: A special type of function that describes the workflow using a high-level, easy-to-understand syntax.
        Chaining: Sequentially calling multiple functions in a defined order.
        Fan-Out/Fan-In: Executing multiple functions in parallel and then aggregating the results.

    Reliable State Management:
        Automatic Checkpointing: The system automatically checkpoints the progress of an orchestration function whenever the function schedules an activity or yields (waits for an external event).
        State Persistence: The state is persisted in Azure Storage, ensuring that the workflow can be reliably resumed even after a failure or restart.
        Durable Timers: Allows orchestrator functions to wait for a specified amount of time or until a specific deadline.

    Complex Workflow Handling:
        Sub-Orchestration: The ability to break down complex workflows into smaller, reusable components by calling other orchestrator functions.
        Error Handling and Retries: Built-in mechanisms to handle errors and retry operations automatically.
        Human Interaction: Workflows can pause and wait for external human input or approval, enabling human-in-the-loop scenarios.
        Monitoring and Diagnostics: Integration with Azure Monitor and Application Insights for tracking and diagnosing workflows.

References:

[Microsoft Learn: Introduction to Durable Functions](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview?tabs=in-process%2Cnodejs-v3%2Cv1-model&pivots=python)  
[Microsoft Documentation: Durable Functions Overview](https://learn.microsoft.com/en-us/azure/azure-functions/durable/)


## Function Chaining in Azure Durable Functions  

Function chaining is a pattern where multiple functions are executed in a specific order, with each function depending on the output of the previous one. This pattern is particularly useful for workflows where steps must be performed in sequence, ensuring that each step completes successfully before moving on to the next.

In Azure Durable Functions, function chaining is implemented using an orchestrator function that defines the sequence of function calls. The orchestrator function manages the execution flow, ensuring that each function is called in order and that the results are passed correctly from one function to the next.  

Let us orchestrate a vanilla Durable Function using standard templates in the v1 model, using this [Quickstart guide](https://learn.microsoft.com/en-us/azure/azure-functions/durable/quickstart-python-vscode?tabs=linux%2Cazure-cli-set-indexing-flag&pivots=python-mode-configuration) as reference:  


## Create Python 3.10 Virtual Environment  

```
python3.10 -m venv .venv
source .venv/bin/activate
```  

## Create new Durable Function App 

The most basic Durable Functions app has three functions:

* Orchestrator function: A workflow that orchestrates other functions.
* Activity function: A function that is called by the orchestrator function, performs work, and optionally returns a value.
* Client function: A regular function in Azure that starts an orchestrator function. This example uses an HTTP-triggered function. This is the function that client applications invoke. Orchestrator and Activity functions are not directly invoked by clients.

We are going to create two activity functions: activity1 and activity2.  activity2 will send a message to a queue, which is useful to ensure the orchestration of activities is working.  

```func init VanillaDurable --python -m V1```  
```cd VanillaDurable```  
```func new --name orchestrator1 --template "Durable Functions orchestrator"```  
```func new --name activity1 --template "Durable Functions activity"```  
```func new --name activity2 --template "Durable Functions activity"``` 
```func new --name client1 --template "Durable Functions HTTP starter"```  

Ensure requirements.txt is as follows:  

```
azure-functions
azure-functions-durable
azure-storage-queue
```  
Then run:  
```pip install --no-cache-dir -r requirements.txt  ```  


You now have 3 subdirectories, named orchestrator1, activity1, and client1, each containing a Python script and a function.json file.  

We will make small changes to the default \_\_init\_\_.py files in each function to make them work together based on the chosen name and desired functionality:    


orchestrator1/\_\_init\_\_.py  
```	
# This function is not intended to be invoked directly. Instead it will be
# triggered by an HTTP starter function.
# Before running this sample, please:
# - create a Durable activity function (default name is "Hello")
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
import json

from azure.durable_functions import DurableOrchestrationContext, Orchestrator


def orchestrator_function(context: DurableOrchestrationContext):


    input_data = context.get_input()

    results = []
    result1 = yield context.call_activity('activity1', "Tokyo")
    results.append(result1)
    result2 = yield context.call_activity('activity1', "Seattle")
    results.append(result2)
    result3 = yield context.call_activity('activity1', "London")
    results.append(result3) 

    if name := input_data.get("name"):
        logging.info(f"Sending message to queue. Name: {name}")
        result4 = yield context.call_activity('activity2', name)
        results.append(result4)
    return results

main = Orchestrator.create(orchestrator_function)
```  

Notice the orchestrator called "activity1", which is the name of the activity function.  

activity1/\_\_init\_\_.py  
```
# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging


def main(name: str) -> str:
    logging.info(f"Activity 1: Say hello to {name}!")
    return f"Hello {name}!"
```

activity2/\_\_init\_\_.py  
```
# This function is not intended to be invoked directly. Instead it will be
# triggered by an orchestrator function.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable HTTP starter function
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt

import logging
from azure.storage.queue import QueueClient
import azure.functions as func

def main(name: str) -> str:

    import os
    # # Get the connection string from AzureWebJobsStorage
    # connection_string = func.config.get("AzureWebJobsStorage")
    # queue_name = func.config.get("queue_name")


    logging.info(os.environ)
    # Get the connection string from AzureWebJobsStorage
    connection_string = os.environ['AzureWebJobsStorage']
    queue_name = os.environ['queue_name']

    # Create a queue client
    queue_client = QueueClient.from_connection_string(connection_string, queue_name)

    # Send a message to the queue
    message = f"Hello {name}!"
    queue_client.send_message(message)

    return f"Message sent to Azure Queue Storage: {message}"
```


client1/\_\_init\_\_.py
```
# This function an HTTP starter function for Durable Functions.
# Before running this sample, please:
# - create a Durable orchestration function
# - create a Durable activity function (default name is "Hello")
# - add azure-functions-durable to requirements.txt
# - run pip install -r requirements.txt
 
import logging

from azure.functions import HttpRequest, HttpResponse
from azure.durable_functions import DurableOrchestrationClient


async def main(req: HttpRequest, starter: str) -> HttpResponse:

    client_input = dict(req.params)
    
    logging.info(client_input)

    client = DurableOrchestrationClient(starter)
    instance_id = await client.start_new(req.route_params["functionName"], None, client_input)

    logging.info(f"Started orchestration with ID = '{instance_id}'.")

    return client.create_check_status_response(req, instance_id)
```


Durable functions need access to a storage account, which is used to store the state of the orchestrator function. If you do not have one already, you can create a new storage account using the Azure CLI:  

```  
az storage account create \
    --name $storageaccount \
    --resource-group $resource \
    --sku Standard_LRS
``` 

The connection string for the storage account is stored in the local.settings.json file in the root of the function app project, as the value for the AzureWebJobsStorage key:    

```  
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",    
    "queue_name": "activity2",
    "AzureWebJobsStorage": "DefaultEndpointsProtocol=https;AccountName=your_storage_account_name;AccountKey=your_storage_account_key;EndpointSuffix=core.windows.net"
  }
}  
``` 


At this point, you can locally test your function:  

```func start --verbose```  

From another terminal, you can trigger the client function using curl:  

```curl -w '\n' http://localhost:7071/api/orchestrators/orchestrator1```

You should see the logging produced by the orchestrator and activity functions (e.g., *Activity 1: Say hello to Tokyo!*) in the terminal where you ran func start.  


We are ready to create our Function App in Azure:  

```
az functionapp create --consumption-plan-location eastus \
     --runtime python \
     --runtime-version 3.10 \
     --functions-version 4 \
     --resource-group $resource \
     --name VanillaDurableInstructor \
     --os-type linux \
     --storage-account ${storageaccount}
```  

And finally, we can publish it to Azure:  

```func azure functionapp publish VanillaDurableInstructor --python```  

The process provides information about invoking the durable function:  

```
Functions in VanillaDurableInstructor:
    activity1 - [activityTrigger]

    activity2 - [activityTrigger]

    client1 - [httpTrigger]
        Invoke url: https://vanilladurableinstructor.azurewebsites.net/api/orchestrators/{functionname}

    orchestrator1 - [orchestrationTrigger]
```

Notice that queue_name does not propagate to the Azure Portal from local.settings.json. You must add the setting in the Azure Portal, either manually, or by running the following command:  

```
az functionapp config appsettings set --name VanillaDurableInstructor --resource-group ie_st_bcsai_dud_student --settings queue_name=activity2
```

You can now test the function by invoking the client function using the provided URL. You must grab the right key from the Azure Portal, under "client1" -> "Get function URL"

Try calls with and without the name parameter to trigger activity2 and see the message in written in the queue:

curl "https://vanilladurableinstructor.azurewebsites.net/api/orchestrators/orchestrator1?code=KEY_FROM_PORTAL"  
curl "https://vanilladurableinstructor.azurewebsites.net/api/orchestrators/orchestrator1?code=KEY_FROM_PORTAL&name=ThisIsMe"  