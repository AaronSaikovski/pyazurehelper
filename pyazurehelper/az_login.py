#!/usr/bin/env python
""" Checks to see if we are logged into the Azure CLI
"""
from azure.cli.core import get_default_cli

import pyazurehelper.az_subscription as az_sub
import utils.console_helper as console_helper

# ******************************************************************************** #


def check_azure_login(subscription_id: str) -> None:
    """
    Checks to see if we are logged into the AzureCLI.
    Will login if we aren't logged in.

    Parameters
    ----------
    subscription_id : string
        Azure Subscription ID

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
