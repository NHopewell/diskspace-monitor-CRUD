"""warnings.py

Contains custom Errors attached to the Agent model which trigger
warnings to be registered in our system. These warnings do not
disrupt the system, but rather are storaged in memory to be queried
and logged.
"""
from enum import Enum


class WarningEnum(str, Enum):
    close_to_memory_limit = "close to memory limit"
    over_memory_limit = "over memory limit"


class OverMemoryLimitError(Exception):
    """Error that is raised when an Agents current storage useage reported
    exceeds its set storage limit.
    """

    def __init__(self, value: int, message: str) -> None:
        self.value = value
        self.message = message

        super().__init__(message)


class StorageLimitOutOfRangeError(Exception):
    """Error that is raised when an Agent sets its storage limit to a
    values outside of the range 0 - 100.
    """

    def __init__(self, value: int, message: str) -> None:
        self.value = value
        self.message = message

        super().__init__(message)
