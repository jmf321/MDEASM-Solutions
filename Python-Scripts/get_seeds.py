#imports
import time

import azure.core.exceptions
from azure.defender.easm import EasmClient
from azure.mgmt.defendereasm import EasmMgmtClient
from azure.identity import ClientSecretCredential
import datetime
import sys

# App Client ID
client_id = ''
# App Client secret
client_secret = ''
# Tenant ID
tenant_id = ''
# Subscription ID
sub_id = ''
# Resource Group Name Where EASM resides
resource_group = ''
# EASM Region
region = ''
# Name of EASM resource
workspace_name = ''


def authentication():
    # Get credentials and create client
    completeCredential = ClientSecretCredential(tenant_id, client_id, client_secret)
    dataEndpoint = f'{region}.easm.defender.microsoft.com'
    dataClient = EasmClient(dataEndpoint, resource_group, sub_id, workspace_name, completeCredential)
    controlClient = EasmMgmtClient(completeCredential, sub_id)
    managementClient = EasmMgmtClient(credential=completeCredential, subscription_id=sub_id)
    return dataClient, controlClient, managementClient


def get_assets_list(dataClient):
    # Get all the seeds and print out
    for asset in dataClient.discovery_groups.list():
        seed_list = asset.get('seeds', [])
        if len(seed_list) > 0:
            for each_seed in seed_list:
                assetType = each_seed['kind']
                assetName = each_seed['name']
                print(assetName + "\t" + assetType)


def main():
    dataClient, controlClient, managementClient = authentication()
    try:
        get_assets_list(dataClient)
    except azure.core.exceptions.HttpResponseError as e:
        print(e)


if __name__ == '__main__': #references the main class
    sys.exit(main()) #exits the thread