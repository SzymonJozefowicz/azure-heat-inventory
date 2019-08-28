# ======================================================================
# Azure-Heat Integration
# Export data to Heat via SFTP Server
#
# 1. Connect to Azure
# 2. Get information about virtual machines
# 3. Store it in csv file
# 4. Send csv to Heat sftp
#
# Author:szymon@circlekeurope.com
# Date Created: 2019-08-14
# ======================================================================

# For use with MIA
from msrestazure.azure_active_directory import MSIAuthentication


# For use wih SP
from azure.common.credentials import ServicePrincipalCredentials


# Imports
import os
import csv
from azure.mgmt.resource import ResourceManagementClient, SubscriptionClient
from azure.mgmt.compute import ComputeManagementClient
from msrestazure.azure_exceptions import CloudError

from paramiko import SSHClient
from paramiko import AutoAddPolicy


# ==============================================================
#               Authentication credentials setup
#             Fisrt try to authenticate using MIA
# ==============================================================

sp_error = True
mia_error = True

print("Connecting to Azure.")

# ==============================================================
#               Authentication using MSI
#                Use MIA in production
# ==============================================================

try:
    credentials = MSIAuthentication()
    mia_error = False

except:
    print("Azure Managed Identity is not set up for this machine.")
    print("Trying to use Service Pricipal connection.")
    mia_error = True


# ==============================================================
#               Authentication using SP
# ==============================================================


if mia_error == True:
    try:
        credentials = ServicePrincipalCredentials(
            client_id=os.environ['AZURE_CLIENT_ID'],
            secret=os.environ['AZURE_CLIENT_SECRET'],
            tenant=os.environ['AZURE_TENANT_ID']
        )
        subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
        sp_error = False
    except:
        print("Azure Service Principal variables are not set.")
        sp_error = True

# ==============================================================
#                   Quit if nothing works
# ==============================================================


if sp_error == True and mia_error == True:
    print("No Service Principal or Managed Identity Access authentication possible.\nPlease check you credentials...")
    exit(1)

# ==============================================================
#               Check SFTP Variables
# ==============================================================

sftp_var_error=True

try:
    csv_path = os.environ['SFTP_TMP_PATH']
    sftp_hostname = os.environ['SFTP_HOSTNAME']
    sftp_username = os.environ['SFTP_USERNAME']
    sftp_password = os.environ['SFTP_PASSWORD']
    sftp_var_error=False
except:
    sftp_var_error=True


if sftp_var_error == True:
    print("SFTP variables are not set. Please check os variables.")
    print("SFTP_HOSTNAME\nSFTP_USERNAME\nSFTP_PASSWORD\nSFTP_TMP_PATH\n")
    exit(2)


# Create output variables

output_name = ""
output_application = ""
output_environment = ""
output_application = ""
output_owner_login=""
output_project = ""
output_auto_start = ""
output_auto_stop = ""
output_start_time = ""
output_stop_time = ""
output_premium_ssd = ""
output_subscription_name = ""
output_resource_group = ""
output_location = ""
output_size = ""
output_id = ""
output_os = ""


# Create output csv file
#csv_path = os.environ['SFTP_TMP_PATH']
csv_file_name = "vm-heat-inventory-list.csv"

with open(csv_path + csv_file_name, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',',quotechar='"', quoting=csv.QUOTE_ALL)
    #row_headers = ['Name', 'Login', 'Enviroment', 'Project', 'AutoStart', 'AutoStop', 'StartTime','StopTime', 'PremiumSSD', 'Subscription Name', 'ResourceGroup', 'Location', 'Size', 'Id', 'OS']
    row_headers = [
        'Name',
        'Login', 
        'Used For', 
        'Description', 
        'AutoStart', 
        'AutoStop', 
        'StartTime',
        'StopTime', 
        'OS']

    csv_writer.writerow(row_headers)


# Create a Subscription Client
subscription_client = SubscriptionClient(credentials)

for subscriptions in subscription_client.subscriptions.list():
    print(subscriptions.display_name)
    subscription_name = subscriptions.display_name
    subscription_id = subscriptions.subscription_id
    output_subscription_name = subscription_name

# Create a Resource Management client

    resource_client = ResourceManagementClient(credentials, subscription_id)

# For each resource group
    
    for resource_group in resource_client.resource_groups.list():
        resource_group_name = resource_group.name
        print("Subscription:" + subscription_name + " Resource Group:" + resource_group_name)
        output_resource_group = resource_group.name

        compute_client = ComputeManagementClient(credentials, subscription_id)

        for vm in compute_client.virtual_machines.list(resource_group_name):
            output_name = vm.name
            output_location = vm.location
            output_size = vm.hardware_profile.vm_size
            output_id = vm.id
            output_os = vm.storage_profile.os_disk.os_type.name
            tags = vm.tags

            if tags != None:
                if "Application" in tags:
                    output_application = tags["Application"]
                else:
                    output_application=""
                if "OwnerLogin" in tags:
                    output_owner_login = tags["OwnerLogin"]
                else:
                    output_owner_login=""
                #if "Owner" in tags:
                #    output_owner = tags["Owner"]
                if "Environment" in tags:
                    output_environment = tags["Environment"]
                else:
                    output_environment=""
                if "Project" in tags:
                    output_project = tags["Project"]
                else:
                    output_project=""
                if "AutoStart" in tags:
                    output_auto_start = tags["AutoStart"]
                else:
                    output_auto_start=""
                if "AutoStop" in tags:
                    output_auto_stop = tags["AutoStop"]
                else:
                    output_auto_stop=""
                if "StartTime" in tags:
                    output_start_time = tags["StartTime"]
                else:
                    output_start_time=""
                if "StopTime" in tags:
                    output_stop_time = tags["StopTime"]
                else:
                    output_stop_time=""
                if "PremiumSSD" in tags:
                    output_premium_ssd = tags["PremiumSSD"]
                else:
                    output_premium_ssd=""

                if output_application!="":
                    output_row = [
                    output_name,
                    output_owner_login,
                    output_environment, 
                    output_application + ' ' +  output_project + ' ' + output_subscription_name + ' ' + output_resource_group + ' ' + output_location + ' ' + output_size,
                    output_auto_start, 
                    output_auto_stop, 
                    output_start_time, 
                    output_stop_time, 
                    output_os]
                    
                    with open(csv_path + csv_file_name, 'a', newline='') as csv_file:
                        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                        csv_writer.writerow(output_row)

# ==============================================================

#           Verify if SFTP os variables are provided

# ==============================================================

print("Connecting to SFTP server")
sftp_working_directory = "OUT/heat/"

#try:
#    sftp_hostname = os.environ['SFTP_HOSTNAME']
#    sftp_username = os.environ['SFTP_USERNAME']
#    sftp_password = os.environ['SFTP_PASSWORD']
#
#except:
#    print("SFTP Connection variables not provided\nPlease check SFTP hostname and credentials")
#    exit(2)


try:
    client = SSHClient()
    policy = AutoAddPolicy()
    #client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
    client.set_missing_host_key_policy(policy)
    client.connect(hostname=sftp_hostname,username=sftp_username,password=sftp_password)
    sftp = client.open_sftp()
    sftp.put(csv_path + csv_file_name, sftp_working_directory + csv_file_name)
    print("Connection completed")
except:
    print("Error sending file to SFTP server")
