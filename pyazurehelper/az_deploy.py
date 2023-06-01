"""
Deploys Azure resources using the 
Azure Python SDK 
"""
import json
import os
from datetime import datetime

from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode

import pyazurehelper.az_login as az_login
import pyazurehelper.az_subscription as az_sub
import utils.console_helper as console_helper


class Deploy:
    """
    Main deployment class - Deploys Azure resources
    Perform the deployment of Azure resources
    """

    # ******************************************************************************** #

    def __init__(
        self, subscription_id: str, resource_group_name: str, location: str
    ) -> None:
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
            self.resource_client = ResourceManagementClient(
                self.credentials, self.subscription_id
            )
        else:
            console_helper.print_error_message("##ERROR - Invalid SubscriptionID!")

    # ******************************************************************************** #

    def deploy_resource_group(self) -> None:
        """Deploys a new Azure resource group
        Parameters
        ----------
        None - Taken from class constructor.
        """
        rg_result = self.resource_client.resource_groups.create_or_update(
            self.resource_group_name, {"location": self.location}  # type: ignore
        )

    # ******************************************************************************** #

    def deploy_resource_template(
        self, template_file: str, template_params_file: str
    ) -> None:
        """Deploys a template to the resource group
        Parameters
        ----------
        template_file - ARM or Bicep file
        template_params: - Template params file as string
        deployment_name: - Deployment Name

        Returns
        -------
        nothing
            Displays output status of the Resource group deployment.
        """

        ## ref: https://github.com/p-prakash/serverless-url-shortener-azure/blob/main/deploy.py
        ## https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/resources/azure-mgmt-resource/tests/test_mgmt_resource.py
        ## https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/deploy-python
        ## https://learn.microsoft.com/en-us/python/api/azure-core/azure.core.polling.lropoller?view=azure-python

        # generate a random deployment name
        today = datetime.now().strftime("%m-%d-%Y")
        deployment_name = f"pydeploy{today}"

        # check the file path exists
        if os.path.isfile(template_file):
            # convert the template string to json
            json_template = self.__read_file_data(template_file)

            # Load the param file as a string
            json_params = self.__read_file_data(template_params_file)

            # build properties
            deployment_params = {
                "mode": DeploymentMode.INCREMENTAL,
                "template": json_template,
                "parameters": json_params,
            }

            # Do the deployment
            deploy_result = self.resource_client.deployments.begin_create_or_update(
                self.resource_group_name,
                deployment_name,
                {"properties": deployment_params},  # type: ignore
            )

            # print the result
            print(f"Deployment result - {deploy_result.result()}")

        else:
            console_helper.print_error_message(f"##ERROR - {template_file} not found>!")

    # ******************************************************************************** #

    def __read_file_data(self, file_name: str) -> str:
        """
        Opens a given parameters file and returns a JSON string
        """
        json_data: str

        if os.path.isfile(file_name):
            with open(file_name, "r") as file:
                json_data = json.load(file)
            return json_data
        else:
            return None  # type: ignore

    # ******************************************************************************** #

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
