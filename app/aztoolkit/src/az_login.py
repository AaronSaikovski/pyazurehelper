#!/usr/bin/env python
""" Checks to see if we are logged into the Azure CLI
"""
import aztoolkit.az_subscription as az_sub
from azure.cli.core import get_default_cli
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient

import utils.console_helper as console_helper

# ******************************************************************************** #


def check_azure_login(subscription_id: str) -> None:
    """
    Checks to see if we are logged into the AzureCLI.
    Will login if we aren't logged in.

    Parameters
    ----------
    subscription_id : string

    Returns
    -------
    nothing
        Logs in if not logged on
    """
    # Check if Subscription is valid
    if az_sub.check_valid_subscription_id(subscription_id):
        # get the cli instance
        az_cli = get_default_cli()

        # Get subscription info if logged in
        account_response = az_cli.invoke(
            ["account", "show", "--subscription", subscription_id]
        )
        if account_response == 0:
            subscription_name: str = az_cli.result.result["name"]
            # pylint: disable=line-too-long
            console_helper.print_confirmation_message(
                f"Deploying: '{subscription_name}' with Id: '{subscription_id}'"
            )
        else:
            # pylint: disable=line-too-long
            console_helper.print_warning_message("Logging in to Azure CLI.")
            az_cli.invoke(["login"])
            az_cli.invoke(["account", "set", "--subscription", subscription_id])
    else:
        console_helper.print_error_message("##ERROR - Invalid SubscriptionID!")


# ******************************************************************************** #

def do_login(
    subscription_id: str, credentials: AzureCliCredential
) -> ResourceManagementClient:
    """
    Do the login

    Parameters
    ----------
    subscription_id : string
    credentials: AzureCliCredential

    Returns
    -------
    nothing
        Logs in if not logged on
    """
    # Check if SubscriptionID is valid
    if az_sub.check_valid_subscription_id(subscription_id):
        # Do login if not already
        check_azure_login(subscription_id)

        # Obtain the management object for resources.
        return ResourceManagementClient(credentials, subscription_id)
    return None
    
# ******************************************************************************** #
