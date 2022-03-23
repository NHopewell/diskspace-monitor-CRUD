import typing as t

import pydantic

from diskspacemonitor import settings
from diskspacemonitor import warn


class SystemComponent(pydantic.BaseModel):
    """
    a SystemComponent represents a component of the build system we would
    like to monitor.

    note: data validation has been captured in the data model here by
    sending custom errors to the API, signaling when to register
    ResourceWarnings.

    attributes
    ----------
    name: str, required
        a name given to the current resource / component. Must be unique
        to the current agent.
    total_available_storage: int, required
        the total storage available on the system component (in Gigabits).
    storage_limit: int
        the upper limit on current storage useage (as a percentage of 100),
        above which a warning will be issued.
        Defaults to 100. Must be between 0 - 100.
    current_storage_useage: int
        the amount of storage the agent is currently using.
        Defaults to 0. Must be between 0 - total_available_storage.
    """

    name: str
    total_available_storage: int
    storage_limit: int = 100
    current_storage_useage: int = 0

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name}, total_storage={self.total_available_storage}G)"

    @property
    def proportion_of_total_storage_used(self) -> float:
        """Returns the amount of total storage in use as a proportion of 100%"""
        proportion_used = (
            self.current_storage_useage / self.total_available_storage
        ) * 100

        return proportion_used

    @property
    def free_storage(self) -> float:
        """Returns currently unused storage in Gigabits"""
        free_storage = self.total_available_storage - self.current_storage_useage

        return free_storage

    def set_storage_limit(self, value: int) -> None:
        if value not in range(0, 101):
            msg = "The storage limit must be between 0 - 100."
            raise warn.StorageLimitOutOfRangeError(value=value, message=msg)

        self.storage_limit = value

    def set_current_storage_useage(self, value: int) -> None:
        """Validate that the current storage usage is under the
        current storage limit. Also trigger a warning when it is close
        to the storage limit as specified in settings.py"""

        storage_limit_in_gigabits = int(
            self.total_available_storage * (self.storage_limit / 100)
        )

        # set new value always, optionally trigger a warning
        self.current_storage_useage = value

        if value > storage_limit_in_gigabits:
            msg = "The current storage useage exceeds the total storage limit."
            raise warn.OverMemoryLimitError(value=value, message=msg)
        elif (
            storage_limit_in_gigabits - value <= settings.CLOSE_TO_STORAGE_LIMIT_TRIGGER
        ):
            msg = (
                f"{self.name} is approaching its storage limit. "
                f"Current storage useage: {value}G. "
                f"Total storage usage: {storage_limit_in_gigabits}G."
            )

            raise warn.CloseToMemoryLimitError(value=value, message=msg)


class UpdateSystemComponent(SystemComponent):
    """An UpdateSystemComponent is a SystemComponent with all optional
    attributes which is created when an agent issues an update via the API"""

    name: t.Optional[str] = None
    total_available_storage: t.Optional[int] = None
    storage_limit: t.Optional[int] = None
    current_storage_useage: t.Optional[int] = None


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


class ResourceWarning(pydantic.BaseModel):
    """A ResourceWarning is a warning registered when a SystemComponent
    reports a storage useage above, or close to, its upper limit.
    """

    warning_id: str
    warning_type: warn.WarningEnum
    component_event_id: str
