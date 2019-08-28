# Azure Heat Inventory

Basic integration between Azure and Heat CI module using sftp connection.  
Heat part of integration not included in this repo.

Requirements:
- Python3  
- pip3 install msrestazure
- pip3 install azure-mgmt
- pip3 install paramiko


1. Connecting to Azure using Service Principal or Managed Identity Access  
  To use Service Principal you need to provide information as os variables:
     
   export AZURE_CLIENT_ID=<your sp client id>  
   export AZURE_CLIENT_SECRET=<your sp client password>  
   export AZURE_TENANT_ID=<your tenant id>  
     
   optional export AZURE_SUBSCRIPTION_ID'=<your subscription>  
   os variables should be taken from azure key vault using command like this:
   export AZ_SECRET=$(az keyvault secret show  --vault-name "<your vault name> --name "<name of secret>" --query value --output tsv)
  
  
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
  OwnerLogin  
  Environment  
  Project  
  Application  
  AutoStart  
  AutoStop  
  StartTime  
  StopTime  
  PremiumSSD  
  
4. Store information in csv file
5. Send file to sftp server using ssh client from paramiko
  You need to provide sftp server scredentials as os variables
  SFTP_HOSTNAME - sftp server name or IP  
  SFTP_USERNAME - sftp user  
  SFTP_PASSWORD - sftp password    
  SFTP_TMP_PATH - local path to store sftp temporary files
  SFTP_OUT_PATH - remote output path on sftp server
    
  
