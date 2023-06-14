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
from azure.mgmt.resource.resources.models import DeploymentMode


class DeploymentHelper:
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
        self.resource_client = az_login.do_login(self.subscription_id, self.credentials)

    # ******************************************************************************** #

    def __build_deployment_params(
        self, template_data: dict, parameter_data: object
    ) -> dict:
        """creates a new deployment params dict
        Parameters
        ----------
        template_data: template body
        parameter_data: template body
        """
        deployment_params: dict

        # we dont have function overloading in Py so this is the only option
        # if we have parameters passed in, add them to the dict
        if parameter_data is not None:
            deployment_params = {
                "mode": DeploymentMode.INCREMENTAL,
                "template": template_data,
                "parameters": parameter_data,
            }
        else:
            deployment_params = {
                "mode": DeploymentMode.INCREMENTAL,
                "template": template_data,
            }

        return deployment_params

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
        return self.resource_client.deployments.begin_create_or_update(
            self.resource_group_name, deployment_name, {"properties": deployment_params} # type: ignore
        )

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

        # check if the resource exists..if not create it
        self.deploy_resource_group()

        # check the file path exists
        if os.path.isfile(template_file):
            console_helper.print_command_message("**Deploying template **")

            # convert the template string to json
            template_body = self.__read_file_data(template_file)

            # Load the param file as a string
            params_body = self.__read_file_data(template_params_file)

            # Get the params from the dict using a get()
            extracted_params = params_body.get("parameters")

            # build properties
            deployment_params = self.__build_deployment_params(
                template_body, extracted_params
            )

            # do the deployment
            self.__do_resource_deployment(deployment_name, deployment_params)
            console_helper.print_command_message("**Deployment completed. **")

        else:
            console_helper.print_error_message(f"##ERROR - {template_file} not found>!")

    # ******************************************************************************** #

    def __read_file_data(self, file_name: str) -> dict:
        """
        Opens a given parameters file and returns a JSON string
        """
        if os.path.isfile(file_name):
            with open(file_name, "r") as file:
                return json.load(file)
        else:
            return None # type: ignore

    # ******************************************************************************** #

    def deploy_resource_group(self) -> None:
        """
        creates a resource group..if it doesnt exist
        """
        if not az_resourcegroup.get_resource_group(
            self.resource_client, self.resource_group_name
        ):
            az_resourcegroup.create_resource_group(
                self.resource_client, self.resource_group_name, self.location
            )

    # ******************************************************************************** #

    def destroy_resource_group(self) -> None:
        """
        Deletes a resource group if it exists
        """
        if az_resourcegroup.get_resource_group(self.resource_client, self.resource_group_name):
            az_resourcegroup.delete_resource_group(self.resource_client, self.resource_group_name)

    # ******************************************************************************** #
