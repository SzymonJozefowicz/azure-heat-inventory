# Azure Heat Inventory

Basic integration between Azure and Heat CI module using sftp connection.  
Heat part of integration not included in this repo.

1. Connecting to Azure using Service Principal or Managed Identity Access  
  To use Service Principal you need to provide information as os variables:
     
   export AZURE_CLIENT_ID=<your sp client id>  
   export AZURE_CLIENT_SECRET=<your sp client password>  
   export AZURE_TENANT_ID=<your tenant id>  
     
   optional export AZURE_SUBSCRIPTION_ID'=<your subscription>  

2. Scan all available by rbac subscriptions  

3. For each virtual machine collect information:  
  
  Name  
  Size  
  OS  
  Id  
  Subcription Name
  Resource Group  
  Location  
    
  Using tags:  
  Owner  
  Environment  
  Project  
  Application  
  AutoStart  
  AutoStop  
  StartTime  
  StopTime  
  PremiumSSD  
  
4. Store information in csv file
5. Send file to sftp server.
