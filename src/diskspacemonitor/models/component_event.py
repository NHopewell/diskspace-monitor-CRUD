from typing import Dict
from typing import Union

import pydantic

JSON = Union[Dict[str, str], Dict[str, Union[str, Dict[str, str]]]]


class ComponentEvent(pydantic.BaseModel):
    """A ComponentEvent is a data point of a given SystemComponents storage
    useage one moment in time.

    note: These are automatically generated when new components are registered
    and the storage limits and useages change.
    """

    event_id: str
    timestamp: str
    component_name: str
    total_available_storage: int
    storage_limit: int
    current_storage_useage: int

    def return_custom_event_dict(self) -> JSON:
        """Convert our SystemEvents to the JSON structure desired"""
        event_dict = {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "component_snapshot": {
                "component_name": self.component_name,
                "total_available_storage": self.total_available_storage,
                "storage_limit": self.storage_limit,
                "current_storage_useage": self.current_storage_useage,
            },
        }

        return event_dict
