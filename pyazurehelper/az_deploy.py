"""Deploys Azure resources using the Azure 
Python SDK 
"""
#import json
import os
import os.path

from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient

import pyazurehelper.az_login as az_login
import pyazurehelper.az_subscription as az_sub
import utils.console_helper as console_helper

#import sys

#from azure.mgmt.resource.resources.models import DeploymentMode



class Deploy:
    '''
    Main deployment class - Deploys Azure resources
    Perform the deployment of Azure resources
    '''

    def __init__(self, 
                 subscription_id: str, 
                 resource_group_name: str, 
                 location: str) -> None:
        """Init function."""
        # Acquire a credential object using CLI-based authentication.
        azure_cli_credential = AzureCliCredential()
        self.credentials = azure_cli_credential

        # local variables
        self.subscription_id = subscription_id
        self.resource_group_name = resource_group_name
        self.location = location

        # Check if SubscriptionID is valid
        if az_sub.check_valid_subscription_id(self.subscription_id):
            # Do login if not already
            az_login.check_azure_login(self.subscription_id)

            # Obtain the management object for resources.
            self.resource_client = ResourceManagementClient(self.credentials, 
                                                            self.subscription_id)
            # print(f"logged in")
        else:
            console_helper.print_error_message("##ERROR - Invalid SubscriptionID!")
            #sys.exit(-1)

    def deploy_resource_group(self) -> None:
        """Deploys a new Azure resource group
        Parameters
        ----------
        None - Taken from class constructor.
        """
        rg_result = self.resource_client.resource_groups.create_or_update(
            self.resource_group_name, {"location": self.location}
        )
        print(rg_result)

    def deploy_resource_template(self, 
                                 template_path: str,
                                 template_parameters: dict) -> None:
        """Deploys a template to the resource group
        Parameters
        ----------
        taken from class constructor

        Returns
        -------
        nothing
            Displays output status of the Resource group deployment.
        """

        # check the file path exists
        if os.path.isfile(template_path):
            pass
            # build properties
            # deployment_properties = {
            #     'mode': DeploymentMode.INCREMENTAL,
            #     'template': template_path,
            #     'parameters': template_parameters,
            # }

            # str_temp = json.dumps(deployment_properties)
            # print(deployment_properties)

            # Do the deployment
            # template_result = self.resource_client.deployments.begin_create_or_update(
            #     self.resource_group_name,
            #     'azure-sample',
            #     deployment_properties
            # )

            # template_result = self.resource_client.deployments.begin_create_or_update(
            #     self.resource_group_name, 
            # 'azure-sample', 
            # {'parameters': json.dumps(template_parameters)}
            # )

        else:
            console_helper.print_error_message(f"##ERROR - {template_path} not found>!")
            #sys.exit(-1)

    def destroy_resource_group(self) -> None:
        """Destroys the Azure resource group
        Parameters
        ----------
        taken from class constructor

        Returns
        -------
        nothing
            Displays output status of the Resource group deployment.
        """
        self.resource_client.resource_groups.begin_delete(self.resource_group_name)
