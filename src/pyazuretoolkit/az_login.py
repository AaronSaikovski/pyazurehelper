#!/usr/bin/env python
""" Checks to see if we are logged into the Azure CLI
"""

from azure.cli.core import get_default_cli
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient

from .az_subscription import check_valid_sub_id
from .console_helper import (
    print_confirmation_message,
    print_error_message,
    print_warning_message,
)

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
    if check_valid_sub_id(subscription_id):
        # get the cli instance
        az_cli = get_default_cli()

        # Get subscription info if logged in
        account_response = az_cli.invoke(
            ["account", "show", "--subscription", subscription_id]
        )
        if account_response == 0:
            subscription_name: str = az_cli.result.result["name"]
            # pylint: disable=line-too-long
            print_confirmation_message(
                f"Deploying: '{subscription_name}' with Id: '{subscription_id}'"
            )
        else:
            # pylint: disable=line-too-long
            print_warning_message("Logging in to Azure CLI.")
            az_cli.invoke(["login"])
            az_cli.invoke(["account", "set", "--subscription", subscription_id])
    else:
        print_error_message("##ERROR - Invalid SubscriptionID!")


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
    if check_valid_sub_id(subscription_id):
        # Do login if not already
        check_azure_login(subscription_id)

        # Obtain the management object for resources.
        return ResourceManagementClient(credentials, subscription_id)
    return None
    
# ******************************************************************************** #
