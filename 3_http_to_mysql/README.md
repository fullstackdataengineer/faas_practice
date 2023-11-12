
# PRACTICE: HTTP to MySQL  

This is a Function to build an HTTP API to MySQL bridge. The API endpoint supports parameters "name" and "state", which are written to a pre-configured table (event) in MySQL

## Target database schema:  


Database consists of a single table, event:  

```  
CREATE TABLE event (
    id INT  NOT NULL AUTO_INCREMENT, 
    name VARCHAR(20) , 
    state VARCHAR(20),
    datetime DATETIME NOT NULL,
    PRIMARY KEY(id)
)
```  

Records can be inserted with this command:

```  
INSERT INTO event(name, state, datetime) VALUES ('event_name','current_state',NOW())
```  

## Azure Function Environment Setup  

This is to be run on an environment with Azure Functions Core Tools available.  


```  
python3.9 -m venv .venv
source .venv/bin/activate
pip install --no-cache-dir -r requirements.txt  
```  


The contents of requirements.txt are:  

```  
azure-functions
mysql-connector-python
```  

## Create new Function App  

```  
func init HTTP2MySQL --python -m V1
cd HTTP2MySQL
func new --name HTTP2MySQL --template "HTTP trigger" --authlevel "function"
```  

Deploy Function code:  

```  
cp ../src/__init__.py HTTP2MySQL/  
cp ../requirements.txt .
```  

```  
az login --tenant 5ca2bc70-353c-4d1f-b7d7-7f2b2259df68 
az account set --subscription e0b9cada-61bc-4b5a-bd7a-52c606726b3b 

resource=IE_ST_BCSAI_DUD_STUDENT
storageaccount=iestdudbstudent0001  
```  

```  
az functionapp create --consumption-plan-location westeurope \
     --runtime python \
     --runtime-version 3.9 \
     --functions-version 4 \
     --resource-group $resource \
     --name HTTP2MySQLFunc1 \
     --os-type linux \
     --storage-account ${storageaccount}  
```  

Now, setup "New Application Setting" from Azure Portal -> Functions -> HTTP2MySQLFunc1 -> Settings -> Configuration for these variables:  

* db_username  
* db_password  
* db_host  
* db_name  

Do not forget to click the "Save" button!  

Fetch Function settings into local.settings.json:  

```  
func azure functionapp fetch-app-settings HTTP2MySQLFunc1  
```  

To make sure variables are available locally, run:  
```  
cat local.settings.json  
```  

Run function locally:  
```  
func start  
```  

Test call using curl:  

> curl "http://localhost:7071/api/HTTP2MySQL?name=Edu&state=ready"


Finally, we are ready to publish our Function code to the Azure Function App:  

```  
func azure functionapp publish HTTP2MySQLFunc1 --python  
```  

Notice that Function calls must include a code parameter for authentication. The easiest way to get the URL is to browse to the function in Azure Portal and click "Get Function Url".  

Sample call:  

```
curl "https://http2mysqlfunc1.azurewebsites.net/api/HTTP2MySQL?code=IGIE-PZX4KoS4BYidNrqU22q3yBfoF3niCPVVrjTuspQAzFuULt_Uw==&name=live&state=done"
```  

You can then connect to your target  MySQL database (using Python, for example) to ensure the new record was written to table event.  


