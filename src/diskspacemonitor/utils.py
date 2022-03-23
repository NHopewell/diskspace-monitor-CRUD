"""utils.py

This module containers helpers used by main.py
"""
import datetime
import typing as t
import uuid

from diskspacemonitor import models
from diskspacemonitor import warn


def return_uuid() -> str:
    """Return a universally unique identifier"""
    return str(uuid.uuid4())


def return_timestamp() -> str:
    """Return current date and time in string format"""
    return datetime.datetime.now().strftime("%m.%d.%Y %H:%M:%S")


def register_system_component(
    component: models.SystemComponent, database: dict
) -> None:
    """Store a newly created systemc component in our db."""
    database["system_components"][component.name] = component


def register_system_event(
    component: t.Union[models.SystemComponent, models.SystemComponentUpdate],
    database: dict,
    warning: t.Optional[warn.WarningEnum] = None,
) -> None:
    """Store a new system event in our db when a system component storage
    useage is updated. If this event triggers a resource warning (when
    storage exceeds (or comes close to exceeing) our components storage
    limit, also store this warning in our db.

    Parameters
    ----------
    component: SystemComponent
        a system component object yet to be registered in the system.
    database: dict
        an dictionary serving as a database.
    warning: WarningEnum, optional
        a warning type if (only if the event triggered a warning).
    """

    # always register the system event to capture updates to components
    time_of_event = return_timestamp()
    event_id = return_uuid()
    system_event = models.ComponentEvent(
        event_id=event_id,
        timestamp=time_of_event,
        component_name=component.name,
        total_available_storage=component.total_available_storage,
        storage_limit=component.storage_limit,
        current_storage_useage=component.current_storage_useage,
    )
    database["system_events"][component.name].append(system_event)

    # if the system event triggered a warning, register it seperately as well
    if warning:
        warning_id = return_uuid()
        resource_warning = models.ResourceWarning(
            warning_id=warning_id, warning_type=warning, component_event_id=event_id
        )
        database["resource_warnings"][component.name].append(resource_warning)


def get_system_component(component_name: str, database: dict) -> t.Dict[str, str]:
    """Return a system component from our db."""
    return database["system_components"][component_name]


def get_all_warnings(
    system_components: t.List[str], database: dict
) -> t.List[models.ResourceWarning]:
    """Retrieve all resource warnings from our in memory db.

    Parameters
    ----------
    system_components: list(str)
        a list of system component names currently being monitored.
    database: dict
        an dictionary serving as a database.

    returns: a list of ResourceWarnings for each components.
    """

    all_resource_warning_objects = []

    for component in system_components:
        for warning_object in database["resource_warnings"][component]:
            all_resource_warning_objects.append(warning_object)

    return all_resource_warning_objects


def list_warning_dicts(
    warning_objects: t.List[models.ResourceWarning],
    system_components: t.List[str],
    database: dict,
) -> t.List[t.Dict[str, str]]:
    """Pair each resource warning object to the system component that
    triggered it and return as dict.

    Parameters
    ----------
    warning_objects: list(ResourceWarning)
        a list of ResourceWarnings
    system_components: list(str)
        a list of system component names currently being monitored.
    database: dict
        an dictionary serving as a database.

    returns: a list of resource warnings in dictionary format.
    """

    paired_warnings = []

    for resource_warning in warning_objects:
        warning_event_component_id = resource_warning.component_event_id
        for component in system_components:
            events_for_component = database["system_events"][component]
            for event in events_for_component:
                if warning_event_component_id == event.event_id:
                    paired_warnings.append(
                        resource_warning.return_custom_warning_dict(event)
                    )

    return paired_warnings
