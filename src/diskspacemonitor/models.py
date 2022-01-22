from unicodedata import category
import pydantic
import typing as t
import datetime
import warnings

import diskspacemonitor.warn as warn
from diskspacemonitor.warn import WarningEnum
import diskspacemonitor.settings as settings

warnings.simplefilter("always")


class Agent(pydantic.BaseModel):
    """
    An agent is component of the build system we would like to monitor.

    note: data validation has been captured in the data model here by
    sending custom errors to the API, signaling when to register
    AgentWarnings.

    attributes
    ----------
    name : str
        a name given to the current resource / agent. Must be unique
        to the current agent.
    total_available_storage : int
        the total storage available on the agents system (in Gigabits).
    storage_limit: optional float
        the upper limit on current storage useage (as a percentage of 100),
        above which a warning will be issued.
        Defaults to 100. Must be between 0 - 100.
    """

    name: str
    total_available_storage: int
    storage_limit: t.Optional[int] = 100
    current_storage_useage: t.Optional[int] = 0

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
        free_storage = (
            self.total_available_storage - self.current_storage_useage
        )

        return free_storage

    @pydantic.validator("storage_limit")
    @classmethod
    def storage_limit_valid(cls, value: int) -> int:
        """Validate that the storage limit set is between 0 - 100."""

        if value not in range(0, 101):
            # if the storage limit set is out of range, signal to the
            # API to respond with a failure code, do not register AgentWarning
            msg = "The storage limit must be between 0 - 100."
            raise warn.StorageLimitOutOfRangeError(value=value, message=msg)

        return value

    def set_current_storage_useage(self, value: int) -> None:
        """Validate that the current storage usage is under the
        current storage limit. Also trigger a warning when it is close
        to the storage limit as specified in settings.py"""

        storage_limit_in_gigabits = int(
            self.total_available_storage * (self.storage_limit / 100)
        )

        if value > storage_limit_in_gigabits:
            # if the current storage exceeds the storage limit, signal to
            # the API to register an AgentWarning
            msg = "The current storage useage exceeds the total storage limit."
            raise warn.OverMemoryLimitError(value=value, message=msg)
        elif (
            storage_limit_in_gigabits - value
            <= settings.CLOSE_TO_STORAGE_LIMIT_TRIGGER
        ):
            # if the current storage approached the storage limit, signal to
            # the API to register an AgentWarning
            msg = (
                f"{self.name} is approaching its storage limit. "
                f"Current storage useage: {value}G. "
                f"Total storage usage: {storage_limit_in_gigabits}G."
            )

            warnings.warn(msg, category=ResourceWarning)

        self.current_storage_useage = value


class AgentHistoricData(pydantic.BaseModel):
    """An AgentHistoridData is a data point of a given Agents storage
    useage one moment in time.

    note: These are automatically generated when new Agents are registered
    and and the storage limits and useages change.
    """

    agent_name: str
    timestamp: datetime.datetime
    storage_useage_at_timestamp: int
    total_storage_at_timestamp: int
    proportion_of_capacity_at_timestamp: float


class AgentWarning(pydantic.BaseModel):
    """An Agent warning is a warning registered when an Agent reports
    a storage useage above, or close to, its upper limit.
    """

    warning_type: WarningEnum
    agent: AgentHistoricData  # nested model including the timestamp
