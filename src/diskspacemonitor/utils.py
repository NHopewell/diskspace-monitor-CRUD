import typing as t
import datetime
import uuid

import diskspacemonitor.models as models
import diskspacemonitor.warn as monitor_warnings


def get_uuid() -> str:
    """Return a universally unique identifier"""
    return str(uuid.uuid4())


def get_timestamp() -> str:
    """Return current date and time in string format"""
    return datetime.datetime.now().strftime("%m.%d.%Y %H:%M:%S")


def register_system_component(
    component: models.SystemComponent, database: dict
) -> None:
    """Store a newly created systemc component in our db."""
    database["system_components"][component.name] = component


def register_system_event(
    component_name: str,
    component: t.Union[models.SystemComponent, models.UpdateSystemComponent],
    database: dict,
    warning: t.Optional[monitor_warnings.WarningEnum] = None,
) -> None:
    """Store a new system event in our db when a system component storage
    useage is updated. If this event triggers a resource warning (when
    storage exceeds (or comes close to exceeing) our components storage
    limit, also store this warning in our db."""

    # always register the system event to capture updates to components
    time_of_event = get_timestamp()
    event_id = get_uuid()
    system_event = models.ComponentEvent(
        event_id=event_id,
        timestamp=time_of_event,
        component_name=component.name,
        total_available_storage=component.total_available_storage,
        storage_limit=component.storage_limit,
        current_storage_useage=component.current_storage_useage,
    )
    database["system_events"][component_name].append(system_event)

    # if the system event triggered a warning, register it seperately as well
    if warning:
        warning_id = get_uuid()
        resource_warning = models.ResourceWarning(
            warning_id=warning_id, warning_type=warning, component_event_id=event_id
        )
        database["resource_warnings"][component_name].append(resource_warning)


def get_system_component(component_name: str, database: dict) -> t.Dict[str, str]:
    """Return a system component from our db."""
    return database["system_components"][component_name].dict()


def return_event_dict(
    event_id: str,
    timestamp: str,
    component_name: str,
    total_available_storage: str,
    storage_limit: str,
    current_storage_useage: str,
) -> t.Dict[str, t.Union[str, t.Dict[str, str]]]:
    """Helper to convert our SystemEvents to the JSON structure desired"""
    event_dict = {
        "event_id": event_id,
        "timestamp": timestamp,
        "component_snapshot": {
            "component_name": component_name,
            "total_available_storage": total_available_storage,
            "storage_limit": storage_limit,
            "current_storage_useage": current_storage_useage,
        },
    }

    return event_dict


def return_warning_dict(
    warning_id: str,
    warning_type: str,
    event_id: str,
    timestamp: str,
    component_name: str,
    total_available_storage: str,
    storage_limit: str,
    current_storage_useage: str,
) -> t.Dict[str, t.Union[str, t.Dict[str, t.Union[str, t.Dict[str, str]]]]]:
    """Helper to convert our ResourceWarning to the JSON structure desired"""

    warning_dict = {
        "warning_id": warning_id,
        "warning_type": warning_type,
        "component_event": {
            "event_id": event_id,
            "timestamp": timestamp,
            "component_snapshot": {
                "name": component_name,
                "total_available_storage": total_available_storage,
                "storage_limit": storage_limit,
                "current_storage_useage": current_storage_useage,
            },
        },
    }

    return warning_dict
