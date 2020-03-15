'''
Animations animations for health bars.
'''
import threading

from functools import wraps
from typing import Optional

from healthbar.base import HealthBarBase
from healthbar.console import ConsoleHealthBar

def delayed(cls):
    '''
    A decorator for health bars that cannot be reduced by more than ``max_delta`` per interval.
    '''
    assert issubclass(cls, HealthBarBase)
    @wraps(cls, updated=())
    class _DelayedHealthBar(cls, HealthBarBase):
        '''
        @param limit_per_interval   The maximal amount that ``value`` is allowed to change per interval in percents.
                                    must be in (0, 100].
        @param delay_min            The minimal amount that triggers a delay in percents. must be in [0, 100].
        '''
        def __init__(self, *args, limit_per_interval: Optional[float] = None, delay_min: float = 0, **kwargs):
            super().__init__(*args, **kwargs)

            if limit_per_interval is None:
                limit_per_interval = 1 / self.length
            if not 0 < limit_per_interval <= 100:
                raise ValueError(f'limit_per_interval must be greater than 0 and at most 100 (was {limit_per_interval}')

            if not 0 <= delay_min <= 100:
                raise ValueError(f'delay_min must be between 0 and 100 (was {delay_min}')

            self.__limit = limit_per_interval * self.max_value
            self.__delay_min = delay_min
            self.__real_value = self.value
            self.__lock = threading.Lock()

        def set_value(self, value):
            with self.__lock:
                super().set_value(value)
                if self.__delay_min >= abs(self.value - self.__real_value):
                    self.__real_value = self.value

        def draw(self):
            # Limit progression here instead of overriding ``set_value()`` because it's easier to stay within
            # [0, max_value] bounds this way.

            with self.__lock:
                # Get closer to the value
                if self.__real_value < self.value:
                    self.__real_value += min(self.__limit, self.value - self.__real_value)
                elif self.__real_value > self.value:
                    self.__real_value -= min(self.__limit, self.__real_value - self.value)

                # Draw ``__real_value`` instead of ``value``
                val = self.value
                super().set_value(self.__real_value)
                super().draw()
                super().set_value(val)

    return _DelayedHealthBar

@delayed
class DelayedConsoleBar(ConsoleHealthBar):
    '''
    A console health bar with delayed animations.
    '''
