# Integrating Azure Event Hub and Azure Functions with Python

In this lab, you will learn how to integrate Azure Event Hub and Azure Functions using the Python SDK and Core Tools. Azure Event Hub is a highly scalable and event-driven data streaming platform that allows you to ingest and process large volumes of data in real-time. Azure Functions, on the other hand, is a serverless compute service that enables you to run your code in response to events and triggers. Event Hub messages can be processed by Azure Functions using the Event Hub trigger template.

## Create Python 3.10 Virtual Environment  

```
python3.10 -m venv .venv
source .venv/bin/activate
```  

Using the Python Programming Reference model v1, create a new function app:  

```func init EventHub --python -m V1```   
```cd EventHub```  


To enable local development, modify local.settings.json file to include the Azure Event Hub connection string:  

```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "STORAGE_ACCOUNT_CONNECTION_STRING",
    "eventHubConnectionAppSetting": "EVENT_HUB_CONNECTION_STRING",
  }
```

Then, create a function based on the Azure Event Hub trigger template:  

```func new --name processor1 --template "Azure Event Hub trigger" --python```


Ensure function.json file is updated with the correct Event Hub connection string:  

```json
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "type": "eventHubTrigger",
      "name": "events",
      "direction": "in",
      "eventHubName": "feed1",
      "connection": "eventHubConnectionAppSetting",
      "cardinality": "many",
      "consumerGroup": "$Default"
    }
  ]
}
```
Notice the value of connection is the same as the key in the local.settings.json file (eventHubConnectionAppSetting). Once the function is published to Azure, the connection string will be stored in the Azure Function App settings (remember to check!).

"cardinality": "many" indicates that the function will process multiple events from the Event Hub:

```python
def main(events: List[EventHubEvent]):
    for event in events:
      logging.info(f'Function triggered to process a message: {event.get_body().decode()}')
      logging.info(f'  EnqueuedTimeUtc = {event.enqueued_time}')
      logging.info(f'  SequenceNumber = {event.sequence_number}')
      logging.info(f'  Offset = {event.offset}')
```

When set to "one", the function will process a single event at a time:

```python
import logging
import azure.functions as func


def main(event: func.EventHubEvent):
    logging.info(f'Function triggered to process a message: {event.get_body().decode()}')
    logging.info(f'  EnqueuedTimeUtc = {event.enqueued_time}')
    logging.info(f'  SequenceNumber = {event.sequence_number}')
    logging.info(f'  Offset = {event.offset}')

    # Metadata
    for key in event.metadata:
        logging.info(f'Metadata: {key} = {event.metadata[key]}')
```

Note: if using the above function defition, set "name" to "event" in the function.json file, as required by the function signature.  

```json
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "type": "eventHubTrigger",
      "name": "event",
      "direction": "in",
      "eventHubName": "feed1",
      "connection": "eventHubConnectionAppSetting",
      "cardinality": "one",
      "consumerGroup": "$Default"
    }
  ]
}
```


Test the function locally:  

```func start --verbose```  

After the function is running, send a message to the Event Hub using the Azure portal or the Azure CLI:  

```az eventhubs eventhub eventhub create --resource-group $resource --namespace-name $namespace --name feed1```  
```az eventhubs eventhub eventhub send --resource-group $resource --namespace-name $namespace --eventhub-name feed1 --messages "{'name': 'John'}"```  

Inspect the function log to find the messages processed by the function.

## Publish to Azure

Log on to your Azure account:  

```az login```  

Create your function app (you need to specific the resource group ($resource) and storage account ($storageaccount) you want to use):

```
az functionapp create --consumption-plan-location eastus \
     --runtime python \
     --runtime-version 3.10 \
     --functions-version 4 \
     --resource-group $resource \
     --name eventprocessorie1 \
     --os-type linux \
     --storage-account ${storageaccount}
```  

Publish the function to Azure:

```func azure functionapp publish eventprocessorie1 --python```  

Once the function is published, you can send messages to the Event Hub and inspect the function log in the Azure portal.  