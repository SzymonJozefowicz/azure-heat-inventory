#======================================================================
# Azure-Heat Integration 
# Export data to Heat via SFTP Server
# Author:szymon@circlekeurope.com
# Date Created: 2019-08-14
#======================================================================

#For use with MIA
from msrestazure.azure_active_directory import MSIAuthentication

#For use wih SP
from azure.common.credentials import ServicePrincipalCredentials

#Imports
import os
import csv
from azure.mgmt.resource import ResourceManagementClient,SubscriptionClient
from azure.mgmt.compute import ComputeManagementClient
from msrestazure.azure_exceptions import CloudError

#==============================================================
#               Authentication credentials setup
#             Fisrt try to authenticate using MIA 
#==============================================================

sp_error=True
mia_error=True

#==============================================================
#               Authentication using MSI
#                Use MIA in production
#==============================================================

try:
    print("Azure Managed Identity is not set up for this machine.")
    credentials  = MSIAuthentication()
    mia_error=False
except:
    mia_error=True

#==============================================================
#               Authentication using SP
#==============================================================

if mia_error==True:
    try:
        credentials = ServicePrincipalCredentials(
            client_id=os.environ['AZURE_CLIENT_ID'],
            secret=os.environ['AZURE_CLIENT_SECRET'],
            tenant=os.environ['AZURE_TENANT_ID']
        )
        subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
        sp_error=False
    except:
        print("Azure Service Principal variables are not set.")
        sp_error=True

#==============================================================
#                   Quit if nothing works
#==============================================================

if sp_error==True or mia_error==True:
    print("No SP or MIA authentication possible.\nPlease check you credentials...")
    exit(1)


#Create output variables

output_name=""
output_application=""
output_environment=""
output_application=""
output_project=""
output_auto_start=""
output_auto_stop=""
output_start_time=""
output_stop_time=""
output_premium_ssd=""
output_subscription_name=""
output_resource_group=""
output_location=""
output_size=""
output_id=""
output_os=""


#Create output csv file
csv_path="/home/szymon/project/azure-start-stop/env/code/"
csv_file_name="az-heat-inventory-list.csv"
with open("az-heat-inventory-list.csv", 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    row_headers=['Name','Owner','Enviroment','Project','AutoStart','AutoStop','StartTime','StopTime','PremiumSSD','Subscription Name','ResourceGroup','Location','Size','Id','OS']
    csv_writer.writerow(row_headers)



# Create a Subscription Client
subscription_client = SubscriptionClient(credentials)
for subscriptions in subscription_client.subscriptions.list():
    print(subscriptions.display_name)
    subscription_name=subscriptions.display_name
    subscription_id=subscriptions.subscription_id
    
    
    output_subscription_name=subscription_name


# Create a Resource Management client
    resource_client = ResourceManagementClient(credentials, subscription_id)
    
# For each resource group
    for resource_group in resource_client.resource_groups.list():
        resource_group_name=resource_group.name
        print("Subscription:" + subscription_name + " Resource Group:" + resource_group_name)

    
        output_resource_group=resource_group.name
        
        compute_client = ComputeManagementClient(credentials,subscription_id)
        for vm in compute_client.virtual_machines.list(resource_group_name):
            output_name=vm.name
            output_location=vm.location
            output_size=vm.hardware_profile.vm_size
            output_id=vm.id
            output_os=vm.storage_profile.os_disk.os_type.name
            tags=vm.tags

            if tags != None:
                
                if "Application" in tags:
                    output_application=tags["Application"]
                
                if "Owner" in tags:
                    output_owner=tags["Owner"]
                
                if "Environment" in tags:
                    output_environment=tags["Environment"]
                
                if "Project" in tags:
                    output_project=tags["Project"]
                
                if "AutoStart" in tags:
                    output_auto_start=tags["AutoStart"]
                
                if "AutoStop" in tags:
                    output_auto_stop=tags["AutoStop"]
                
                if "StartTime" in tags:
                    output_start_time=tags["StartTime"]
                
                if "StopTime" in tags:
                    output_stop_time=tags["StopTime"]

                if "PremiumSSD" in tags:
                    output_premium_ssd=tags["PremiumSSD"]

            output_row = [output_name,output_application,output_environment,output_application,output_project,output_auto_start,output_auto_stop,output_start_time,output_stop_time,output_premium_ssd,output_subscription_name,output_resource_group,output_location,output_size,output_id,output_os]
            with open("az-heat-inventory-list.csv", 'a', newline='') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                csv_writer.writerow(output_row)
            



