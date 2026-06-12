from typing import Any, TYPE_CHECKING

from ...script_errors import ScriptErrors
from ...consts import *


if TYPE_CHECKING:
    from ...place import Place

class TimeUnit:
    """
    Represents a time unit. 
    It can be seconds, milliseconds, minutes or hours.
    """
    SECONDS = 'seconds'
    MILLISECONDS = 'milliseconds'
    MINUTES = 'minutes'
    HOURS = 'hours'
    UNKNOWN = None

    def __init__(self, unit: str):
        self.unit = unit

    def get_second_multiplier(self) -> float | None:
        """
        Returns multiplier to convert the time to seconds.
        """
        return {
            self.SECONDS: 1.0,
            self.MILLISECONDS: 0.001,
            self.MINUTES: 60.0,
            self.HOURS: 3600.0
        }.get(self.unit, self.UNKNOWN)

    def is_unit(self, other: TimeUnit) -> bool:
        """
        Checks if this time unit is the same as the other time unit.
        """
        return self.unit == other.unit
    
def handle_time_unit(self: 'Place', block: Any, parent: Any, pos: ScriptErrors.Position) -> TimeUnit:
    """
    Handles time units. Returns a TimeUnit.
    """

    if block.secondUnit():
        return TimeUnit(TimeUnit.SECONDS)
    if block.millisUnit():
        return TimeUnit(TimeUnit.MILLISECONDS)
    if block.minuteUnit():
        return TimeUnit(TimeUnit.MINUTES)
    if block.hourUnit():
        return TimeUnit(TimeUnit.HOURS)
    
    return TimeUnit(TimeUnit.UNKNOWN)
