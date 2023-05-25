#!/usr/bin/env python
""" A python script to deploy an Azure Bicep or ARM Template.
"""

import argparse

import pyazurehelper.az_deploy as az_deploy
import utils.console_helper as console_helper

# Custom modules
import utils.logging_helper as logging_helper


def main() -> None:
    """Main function.

    Returns
    -------
    None
    """

    # help message string
    # pylint: disable=line-too-long
    help_msg: str = (
        "Deploys an Azure Bicep or ARM Template"
        "to a given Subscription and Resource Group."
        " **Assumes you are logged in to the AzureCLI."
    )

    # add Args
    parser = argparse.ArgumentParser(description=help_msg)
    parser.add_argument('--SubscriptionId', '-sub', required=True, help='Subscription Id.')
    parser.add_argument('--ResourceGroup', '-rsg', required=True, help='Resource Group.')
    parser.add_argument('--Location', '-loc', required=True, help='Target Location/Region.')
    parser.add_argument('--Environment', '-env', required=False, help='Environment.')
    args = parser.parse_args()

    # set values from command line
    subscription_id = args.SubscriptionId
    resource_group_name = args.ResourceGroup
    location = args.Location
    environment = args.Environment

    # # get the environment variables from the .env file.
    # template_parameters = {
    #     'environment': {'value': environment},
    #     'location': {'value': location},
    #     'resource_group_name': {'value': resource_group_name},
    # }

    # Call the deploy class
    deploy = az_deploy.Deploy(subscription_id, resource_group_name, location)
    deploy.deploy_resource_group()
    # deploy.deploy_resource_template("main.bicep", template_parameters)
    # deploy.destroy_resource_group()

    # do the deployment
    # azdeploy.deploy_template(az_cli,
    #                 "main.bicep",
    #                 location,
    #                 template_parameters)


# Main check
if __name__ == "__main__":
    main()
