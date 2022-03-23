from typing import Dict
from typing import Union

import pydantic

from diskspacemonitor import warn
from diskspacemonitor.models.component_event import ComponentEvent

JSON = Union[Dict[str, str], Dict[str, Union[str, Dict[str, str]]]]


class ResourceWarning(pydantic.BaseModel):
    """A ResourceWarning is a warning registered when a SystemComponent
    reports a storage useage above, or close to, its upper limit.
    """

    warning_id: str
    warning_type: warn.WarningEnum
    component_event_id: str

    def return_custom_warning_dict(self, event: ComponentEvent) -> JSON:
        """Convert our ResourceWarning to the JSON structure desired"""

        warning_dict = {
            "warning_id": self.warning_id,
            "warning_type": self.warning_type,
            "component_event": {
                "event_id": self.component_event_id,
                "timestamp": event.timestamp,
                "component_snapshot": {
                    "name": event.component_name,
                    "total_available_storage": event.total_available_storage,
                    "storage_limit": event.storage_limit,
                    "current_storage_useage": event.current_storage_useage,
                },
            },
        }

        return warning_dict
