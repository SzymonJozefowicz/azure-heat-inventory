# Azure Heat Inventory

Basic integration between Azure and Heat CI module using sftp connection.  
Heat part of integration not included in this repo.

1. Connecting to Azure using Service Principal or Managed Identity Access  

2. Scan all available subscriptions  

3. For each virtual machine collect information:  
  
  Name  
  Size  
  OS  
  Id  
  Subcription Name + Resource Group  
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
