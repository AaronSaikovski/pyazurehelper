#!/usr/bin/env python3
""" A python script to deploy an Azure Bicep or ARM Template.
"""
import argparse
import sys

# import pyazuretoolkit.az_deploy as az_deploy
# import pyazuretoolkit.console_helper as console_helper


from pyazuretoolkit import *

def main() -> None:
    """Main function.

    Returns
    -------
    None
    """

    # ******************************************************************************** #

    # Check if we are running in a virtual environment
    if sys.prefix == sys.base_prefix:

        console_helper.print_error_message("** This is not a virtual environment! **")
        console_helper.print_command_message(
            "Run the following command to create a virtual environment"
        )
        console_helper.print_command_message("'make create'")
        console_helper.print_command_message(
            "This will create and activate a virtual environment using the Makefile"
        )
        sys.exit()

    # ******************************************************************************** #

    # help message string
    # pylint: disable=line-too-long
    help_msg: str = (
        "Deploys an Azure Bicep or ARM Template"
        "to a given Subscription and Resource Group."
        " **Assumes you are logged in to the AzureCLI."
    )

    # add Args
    parser = argparse.ArgumentParser(description=help_msg)
    parser.add_argument(
        "--SubscriptionId", "-sub", required=True, help="Subscription Id."
    )
    parser.add_argument(
        "--ResourceGroup", "-rsg", required=True, help="Resource Group."
    )
    parser.add_argument(
        "--Location", "-loc", required=True, help="Target Location/Region."
    )
    parser.add_argument(
        "--template", "-temp", required=True, help="Resource Template file."
    )
    parser.add_argument(
        "--params", "-params", required=False, help="Resource Template Parameters file."
    )
    args = parser.parse_args()

    # ******************************************************************************** #

    # set values from command line
    subscription_id = args.SubscriptionId
    resource_group_name = args.ResourceGroup
    location = args.Location
    template_file = args.template
    params_file = args.params

    # Call the deploy class
    deploy = az_deploy.DeploymentHelper(subscription_id, resource_group_name, location)
    deploy.deploy_resource_group()

    # deploy template
    deploy.deploy_resource_template(template_file, params_file)

    # ******************************************************************************** #


# Main check
if __name__ == "__main__":
    main()
