"""main.py

This module contains the functions which are triggered at each endpoint
of our API. We are using a simple in-memory database to store and retrieve
data when the application is running. These data are not persisted
to disk.
"""
import typing as t
from collections import defaultdict

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Response

import diskspacemonitor.utils as api_utils
import diskspacemonitor.warn as monitor_warnings
from diskspacemonitor import models


app = FastAPI()

# DATABASE
in_memory_db = {
    "system_components": {},
    "system_events": defaultdict(list),
    "resource_warnings": defaultdict(list),
}


###################################################################
#
#                     System Component Endpoints
#                     --------------------------
#
#  POST    /v1/system_components         Create System Component
#  GET     /v1/system_components/:name   Retrieve System Component
#  PATCH   /v1/system_components/:name   Update System Component
#  DELETE  /v1/system_components/:name   Delete System Component
#  GET     /v1/system_components         List System Components
#
###################################################################


@app.post("/v1/system_components", response_model=models.SystemComponent)
def create_system_component(component: models.SystemComponent) -> None:
    """Create a new system component in our monitored system."""

    if component.name in in_memory_db["system_components"]:
        error_msg = f"{component.name} already exists in the monitored system."
        raise HTTPException(status_code=409, detail=error_msg)

    api_utils.register_system_component(component, in_memory_db)
    api_utils.register_system_event(component, in_memory_db)

    return component


@app.get(
    "/v1/system_components/{component_name}", response_model=models.SystemComponent
)
def read_system_component(component_name: str) -> t.Dict[str, str]:
    """Retrieve data regarding a single system component of our monitored system.

    Path Parameters
    ---------------
    component_name: str
        the unique name of a system component.
    """
    if component_name not in in_memory_db["system_components"]:
        error_msg = f"{component_name} does not exist in the monitored system."
        raise HTTPException(status_code=404, detail=error_msg)

    component = api_utils.get_system_component(component_name, in_memory_db)

    return component


@app.patch(
    "/v1/system_components/{component_name}", response_model=models.SystemComponent
)
def update_system_component(
    component_name: str, updated_component: models.SystemComponentUpdate
) -> None:
    """Update system component in our monitored system.

    Path Parameters
    ---------------
    component_name: str
        the unique name of a system component.

    """
    if component_name not in in_memory_db["system_components"]:
        error_msg = f"{component_name} does not exist in the monitored system."
        raise HTTPException(status_code=404, detail=error_msg)

    system_component = in_memory_db["system_components"][component_name]

    # update component total storage if in request
    if new_total := updated_component.total_available_storage:
        system_component.total_available_storage = new_total

    # update component storage limit if in request
    if new_storage_limit := updated_component.storage_limit:
        try:
            system_component.set_storage_limit(new_storage_limit)
        except monitor_warnings.StorageLimitOutOfRangeError:

            error_msg = f"{new_storage_limit} is not a valid storage limit. Must be between 0 - 100"
            raise HTTPException(status_code=400, detail=error_msg)

    # update component storage useage if in request
    warning_flag, warning_type = False, None

    if new_current_useage := updated_component.current_storage_useage:
        try:
            system_component.set_current_storage_useage(new_current_useage)

        except monitor_warnings.OverMemoryLimitError:
            warning_flag, warning_type = (
                True,
                monitor_warnings.WarningEnum.over_memory_limit,
            )

        except monitor_warnings.CloseToMemoryLimitError:
            warning_flag, warning_type = (
                True,
                monitor_warnings.WarningEnum.close_to_memory_limit,
            )

    if warning_flag:
        # register new system event along with a resource warning
        api_utils.register_system_event(system_component, in_memory_db, warning_type)
    else:
        # register new system event only
        api_utils.register_system_event(system_component, in_memory_db)

    return system_component


@app.delete("/v1/system_components/{component_name}")
def delete_system_component(component_name: str) -> None:
    """Remove a system component from our monitored system.

    Path Parameters
    ---------------
    component_name: str
        the unique name of a system component.
    """
    if component_name not in in_memory_db["system_components"]:
        error_msg = f"{component_name} does not exist in the monitored system."
        raise HTTPException(status_code=404, detail=error_msg)

    # not deleting the component from events or warnings to have backlog
    del in_memory_db["system_components"][component_name]

    return Response(status_code=204)


@app.get("/v1/system_components")
def list_system_components(
    skip: int = 0, limit: t.Optional[int] = 100
) -> t.List[t.Dict[str, str]]:
    """List all currently monitored components of our system.

    Query Parameters
    ----------------
    skip: int
        The number of system components in our result set to skip.
    limit: int
        The total number of system components to return.
    """
    all_system_components = list(in_memory_db["system_components"].values())
    filtered = all_system_components[skip : skip + limit]

    return filtered


#####################################################################################
#
#                           Component Events Endpoints
#                           --------------------------
#
#   GET   /v1/component_events/:name           Get latestest useage for a component
#   GET   /v1/component_events/:name/history   Get historic useages for a component
#   GET   /v1/component_components             Get latestest useage for all components
#
######################################################################################


@app.get("/v1/component_events/{component_name}")
def get_latest_useage(component_name: str) -> t.Dict[str, str]:
    """
    Retrieve the latest storage useage of a component in the system.

    Path Parameters
    ---------------
    component_name: str
        the unique name of a system component.
    """
    all_component_events = in_memory_db["system_events"][component_name]
    latest_event = all_component_events[len(all_component_events) - 1]

    return latest_event.return_custom_event_dict()


@app.get("/v1/component_events/{component_name}/history")
def get_useage_history(
    component_name: str, skip: int = 0, limit: t.Optional[int] = 100
) -> t.List[t.Dict[str, str]]:
    """
    List complete storage useage history for a component in the system.

    Path Parameters
    ---------------
    component_name: str
        the unique name of a system component.

    Query Parameters
    ----------------
    skip: int
        The number of component events in our result set to skip.
    limit: int
        The total number of component events to return.
    """
    all_component_events = in_memory_db["system_events"][component_name]
    event_history_response = [
        event.return_custom_event_dict() for event in all_component_events
    ]

    filtered = event_history_response[skip : skip + limit]

    return filtered


@app.get("/v1/component_events")
def get_all_latest_useages(
    skip: int = 0, limit: t.Optional[int] = 100
) -> t.List[t.Dict[str, str]]:
    """List the latest storage useage of all component in the system.

    Query Parameters
    ----------------
    skip: int
        The number of component events in our result set to skip.
    limit: int
        The total number of component events to return.
    """

    all_components = in_memory_db["system_events"].keys()

    latest_events = []
    for component in all_components:
        all_component_events = in_memory_db["system_events"][component]
        latest_events.append(all_component_events[len(all_component_events) - 1])

    latest_events_for_each_component_response = [
        event.return_custom_event_dict() for event in latest_events
    ]

    filtered = latest_events_for_each_component_response[skip : skip + limit]

    return filtered


##########################################################
#
#              Resource Warnings Endpoints
#              ---------------------------
#
#   GET   /v1/resource_warnings	 List all resource warnings
#
###########################################################


@app.get("/v1/resource_warnings")
def list_resource_warnings(
    skip: int = 0, limit: t.Optional[int] = 100
) -> t.List[t.Dict[str, str]]:
    """List all current resource warnings in our s.

    Query Parameters
    ----------------
    skip: int
        The number of system components in our result set to skip.
    limit: int
        The total number of system components to return.
    """
    # extract all resource warnings from the db and pair to the component
    # that triggered them
    system_components = in_memory_db["system_events"].keys()
    warning_objects = api_utils.get_all_warnings(system_components, in_memory_db)
    paired = api_utils.list_warning_dicts(
        warning_objects, system_components, in_memory_db
    )

    filtered = paired[skip : skip + limit]

    return filtered
