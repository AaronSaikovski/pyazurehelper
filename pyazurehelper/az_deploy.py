"""
Deploys Azure resources using the 
Azure Python SDK 
"""
import json
import os
import time
from datetime import datetime

from azure.core.polling import LROPoller
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

        # Do login
        self.__do_login()
        # # Check if SubscriptionID is valid
        # if az_sub.check_valid_subscription_id(self.subscription_id):
        #     # Do login if not already
        #     az_login.check_azure_login(self.subscription_id)

        #     # Obtain the management object for resources.
        #     self.resource_client = ResourceManagementClient(
        #         self.credentials, self.subscription_id
        #     )
        # else:
        #     console_helper.print_error_message("##ERROR - Invalid SubscriptionID!")

    # ******************************************************************************** #

    def __do_login(self) -> None:
        """Logs in using the CLI
        Parameters
        ----------
        None - Taken from class constructor.
        """
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

    def __deployment_params(self, template_data: dict, parameter_data: str) -> dict:
        """creates a new deployment params dict
        Parameters
        ----------
        template_data: template payload
        parameter_data: template parameters
        """
        return {
            "mode": DeploymentMode.INCREMENTAL,
            "template": template_data,
            "parameters": parameter_data,
        }

    # ******************************************************************************** #

    def __deploy_resources(
        self, resource_group_name: str, deployment_name: str, deployment_params: dict
    ) -> LROPoller:
        """do the deployment and return a status message
        Parameters
        ----------
        template_data: template payload
        parameter_data: template parameters
        """
        deploy_result: LROPoller
        deploy_result = self.resource_client.deployments.begin_create_or_update(
            self.resource_group_name,
            deployment_name,
            {"properties": deployment_params},  # type: ignore
        )

        return deploy_result

    # ******************************************************************************** #

    def __do_resource_deployment(
        self, deployment_name: str, deployment_params: dict
    ) -> None:
        """do the deployment and print a status message
        Parameters
        ----------
        template_data: template payload
        parameter_data: template parameters
        """
        # # Do the deployment
        # deploy_result = self.resource_client.deployments.begin_create_or_update(
        #     self.resource_group_name,
        #     deployment_name,
        #     {"properties": deployment_params},  # type: ignore
        # )

        # Do the deployment and get a result
        deploy_result = self.__deploy_resources(
            self.resource_group_name, deployment_name, deployment_params
        )

        # get the status for the deployment
        console_helper.print_command_message("**Deployment started **")
        deployment_status = deploy_result.status()
        while deployment_status == "InProgress":
            console_helper.print_command_message("Deployment in progress..")
            deployment_status = deploy_result.status()
            time.sleep(3)

        # print the result
        print(f"Deployment result - {deploy_result.result()}")

    # ******************************************************************************** #

    def deploy_resource_template(
        self,
        template_file: str,
        template_params_file: str,
        deploy_prefix: str = "pydeploy",
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

        # generate a random deployment name - YY-MM-DD
        today = datetime.now().strftime("%Y-%m-%d")
        deployment_name = f"{deploy_prefix}{today}"

        # check the file path exists
        if os.path.isfile(template_file):
            console_helper.print_command_message("**Deploying template **")

            # convert the template string to json
            json_template = self.__read_file_data(template_file)

            # Load the param file as a string
            json_params = self.__read_file_data(template_params_file)

            # Get the params from the dict using a get()
            extracted_params: str = str(json_params.get("parameters"))

            # build properties
            deployment_params = self.__deployment_params(
                json_template, extracted_params
            )

            # do the deployment
            self.__do_resource_deployment(deployment_name, deployment_params)

            # # Do the deployment
            # deploy_result = self.resource_client.deployments.begin_create_or_update(
            #     self.resource_group_name,
            #     deployment_name,
            #     {"properties": deployment_params},  # type: ignore
            # )

            # # get the status for the deployment
            # console_helper.print_command_message("**Deployment started **")
            # deployment_status = deploy_result.status()
            # while deployment_status == "InProgress":
            #     console_helper.print_command_message("Deployment in progress..")
            #     deployment_status = deploy_result.status()
            #     time.sleep(3)

            # # print the result
            # print(f"Deployment result - {deploy_result.result()}")

        else:
            console_helper.print_error_message(f"##ERROR - {template_file} not found>!")

    # ******************************************************************************** #

    def __read_file_data(self, file_name: str) -> dict:
        """
        Opens a given parameters file and returns a JSON string
        """
        json_data: dict

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

    # ******************************************************************************** #
