# Azure Functions Practice  


First, create a docker image with Azure Functions Core Tools:  


```
cd core_tools  
docker build -t func_core_tools .
```   

Then, spin up a container exposing each Practice directory as a volume:  

```
docker run -it -v ${PWD}/1_http_trigger_practice/:/1_http_trigger_practice func_core_tools bash
```    

Your practice files can be found at the volume mount point, for example:  ${PWD}/1_http_trigger_practice.  
Follow README.md and try to get the function to work.  

When you complete the deployment and testing of 1_http_trigger_practice, you may do the same with 2_queue_to_table:  

```
docker run -it -v ${PWD}/2_queue_to_table/:/2_queue_to_table func_core_tools bash
```    





