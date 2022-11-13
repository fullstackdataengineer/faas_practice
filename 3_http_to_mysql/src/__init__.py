import logging
import azure.functions as func
import json


headers = {
    "Content-type": "application/json",
    "Access-Control-Allow-Origin": "*"
}

def main(req: func.HttpRequest) -> func.HttpResponse:
    '''
    This is the entry point for HTTP calls to our function
    '''

    logging.info('Python HTTP trigger function processed a request.')

    # For HTTP GET requests
    name = req.params.get('name')
    state = req.params.get('state')

    # For HTTP POST requests, when params are provided in the HTTP body:
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    if not state:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            state = req_body.get('state')

    # Event is routed to the target database and table
    try:
        insert_event(name, state)
    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
                json.dumps(dict(error="Supported paramters: name, state", exception=str(ex))),
                headers=headers,
                status_code=400
        )

    # Return the event back to the client as successful feedback
    return func.HttpResponse(
            json.dumps(dict(name=name, state=state)),
            headers=headers,
            status_code=200
    )


def insert_event(name, state):
    '''
    Insert event information into table event
    Connection details stored as Function Application settings
    '''
    import os

    # This must be set as Function application settings. https://learn.microsoft.com/en-us/azure/azure-functions/functions-app-settings
    username=os.environ['db_username']
    password=os.environ['db_password']
    host=os.environ['db_host']
    database=os.environ['db_name']

    import mysql.connector
    cnx = mysql.connector.connect(user=username, password=password,
                                host=host, database=database)

    insert_query=f"INSERT INTO event(name, state, datetime) VALUES ('{name}','{state}',NOW())"

    cursor = cnx.cursor()
    cursor.execute(insert_query)
    cnx.commit()

    cursor.close()
    cnx.close()

    return True
