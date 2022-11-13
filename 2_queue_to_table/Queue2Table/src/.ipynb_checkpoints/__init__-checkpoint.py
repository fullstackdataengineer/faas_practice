import logging
import uuid
import json

import azure.functions as func

# https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-storage-table-output?tabs=in-process%2Cstorage-extension&pivots=programming-language-python

# https://stackoverflow.com/questions/62780962/update-azure-table-using-azure-function-app-with-python

# /usr/lib/azure-functions-core-tools-4/workers/python/3.8/LINUX/X64/azure_functions_worker/dispatcher.py
def main(msg: func.QueueMessage, entity: func.Out[str]):
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))

    rowKey = str(uuid.uuid4())

    data = {
        "message": msg.get_body().decode('utf-8'),
        "PartitionKey": "message",
        "RowKey": rowKey
    }

    entity.set(json.dumps(data))
    logging.info(vars(entity))

    # return func.HttpResponse(body=f"Message created with the rowKey: {rowKey}") # HTTPResponse not supported
