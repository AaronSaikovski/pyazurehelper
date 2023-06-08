"""
Resource group helper
"""
from azure.mgmt.resource import ResourceManagementClient

import utils.console_helper as console_helper

# ******************************************************************************** #


def create_resource_group(
    resource_client: ResourceManagementClient, resource_group_name: str, location: str
) -> None:
    """Deploys a new Azure resource group
    Parameters
    ----------
    resource_client: ResourceManagementClient
    resource_group_name: str
    location: str

    Returns
    -------
    nothing
        Displays output status of the Resource group deployment.
    """
    console_helper.print_command_message(
        f"Creating resource group - '{resource_group_name}'."
    )
    resource_client.resource_groups.create_or_update(
        resource_group_name, {"location": location}   
    )


# ******************************************************************************** #


def delete_resource_group(
    resource_client: ResourceManagementClient, resource_group_name: str
) -> None:
    """Destroys the Azure resource group
    Parameters
    ----------
    resource_client: ResourceManagementClient
    resource_group_name: str

    Returns
    -------
    nothing
        Displays output status of the Resource group deployment.
    """
    console_helper.print_command_message(
        f"Deleting resource group - '{resource_group_name}'."
    )
    resource_client.resource_groups.begin_delete(resource_group_name)


# ******************************************************************************** #


def get_resource_group(
    resource_client: ResourceManagementClient, resource_group_name: str
) -> bool:
    """Checks if the given resource group exists
    Parameters
    ----------
    resource_client: ResourceManagementClient
    resource_group_name: str

    Returns
    -------
    bool resource group exists
    """
    return resource_client.resource_groups.check_existence(resource_group_name)


# ******************************************************************************** #
