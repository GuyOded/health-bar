#!/usr/bin/env python3
'''
Test code for the health bar.
'''

import os
from time import sleep
from itertools import chain

from functools import wraps

from healthbar import *

def describe(bar: HealthBarBase):
    '''
    Describe a health bar, used for the ``@verbose`` decorator.

    @param bar  A health bar to describe.
    '''
    # Weird thing around ``value`` is to align it nicely
    return f'<HealthBar: length={bar.length}, max_value={bar.max_value}, value={bar.value:{len(str(float(bar.max_value)))}}>'

def verbose(print_when_set: bool = False):
    '''
    A wrapper to make debugging easier.

    @param print_when_set   If set to ``True``, print when the value is set.
                            If set to ``False``, print after drawing.
    '''
    # detect oopsies (forgetting to use parentheses)
    if not isinstance(print_when_set, bool) and issubclass(print_when_set, HealthBarBase):
        return verbose(False)(print_when_set)

    def _verbose(cls):
        assert issubclass(cls, HealthBarBase)

        if print_when_set:
            @wraps(cls, updated=())
            class VerboseHealthBar(cls):
                '''
                Verbosely print on ``draw()``.
                '''
                def set_value(self, value):
                    print(f'\033[92m{describe(self)}.set_value({value})\033[0m')
                    super().set_value(value)
        else:
            @wraps(cls, updated=())
            class VerboseHealthBar(cls):
                '''
                Verbosely print on ``draw()``.
                '''
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)

                    self.__history = []

                def set_value(self, value):
                    self.__history.append((len(self.__history), f'{describe(self)}.set_value({value})'))
                    super().set_value(value)

                def draw(self):
                    super().draw()
                    print(f'\033[92mvalue: {self.value}\033[0m')
                    # print(*self.__history[-10:], sep='\n')
                    for idx, line in self.__history[-10:]:
                        print(f'\033[33m{idx}: {line}\033[0m')
        return VerboseHealthBar
    return _verbose

def clear_occationally(cls):
    '''
    A decorator to make the health bar clear the screen occationally.
    '''
    from functools import wraps
    assert issubclass(cls, HealthBarBase)
    @wraps(cls, updated=())
    class HealthBar(cls):
        '''
        A wrapper that clears the screen every ``__INTERVAL`` seconds.
        '''
        __INTERVAL = 10
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # clear every {__INTERVAL} seconds
            self.__clear_interval = round(HealthBar.__INTERVAL / self.interval)
            self.__interval_count = 0

        def draw(self):
            self.__interval_count += 1
            if self.__interval_count == self.__clear_interval:
                print('\033[2J', end='')
                self.__interval_count = 0
            super().draw()
            # print(f'{self.__interval_count} {self.__clear_interval}')

    return HealthBar

def go(size=100):
    '''
    Quickly test a health bar class by setting the health (slowly) from 0 to max and back to 0.

    @note better to use ``make()`` and ``test()``. This was made to debug the base console healthbar.
    '''
    tsize = os.get_terminal_size()
    r = tsize.lines // 2 - 1
    c = (tsize.columns - size) // 2
    b = ConsoleHealthBar(size, fill='\033[1;31m\u2588', empty='\033[1;30m\u2588', horizontal='', corner='', left=f'\033[H\033[{r}B\033[{c}C', right='\033[0m')
    print('\033[2J', end='')
    for val in chain(range(b.max_value + 1), range(b.max_value, -1, -1)):
        b.set_value(val)
        b.draw()
        sleep(0.01)

def make(size=100, *, hbtype=ConsoleHealthBar, debug=False, **kwargs) -> HealthBarBase:
    '''
    Create a health bar for testing with ``test()``. (or manually)

    @param size     A positive integer for the size of the health bar.
    @param hbtype   The type to use for the health bar.
    @param debug    If set to true, add debug prints to the health bar.

    @note Also passes any keyword arguments to the health bar itself.

    @returns A health bar instance for use with ``test()``.
    '''
    if debug:
        hbtype = verbose(not issubclass(hbtype, ConsoleHealthBar))(hbtype)

    kwargs.setdefault('interval', 0.01)

    return hbtype(size, **kwargs)

def make_console(size: int = None, *, hbtype=ConsoleHealthBar, clear=False, **kwargs) -> HealthBarBase:
    '''
    Create a pretty consolde health bar for testing with ``test()``. (or manually)

    @param size     A positive integer (or ``None``) for the size of the health bar.
    @param hbtype   The type to use for the health bar.
    @param clear    If ``True``, clear the screen every refresh, otherwise, every few seconds.
    @param debug    If set to true, add debug prints to the health bar.
    
    @note Also passes any keyword arguments to the health bar itself.

    @returns A health bar instance for use with ``test()``.
    '''
    assert issubclass(hbtype, ConsoleHealthBar)

    tsize = os.get_terminal_size()

    if size is None:
        size = min(tsize.columns - 2, tsize.columns - (tsize.columns % 100) or 100)

    r = tsize.lines // 2 - 1
    c = (tsize.columns - size) // 2

    if clear:
        clr = '\033[2J'
    else:
        clr = ''
        hbtype = clear_occationally(hbtype)

    return make(size, hbtype=hbtype, fill='\033[1;31m\u2588', empty='\033[1;30m\u2588', horizontal='', corner='', left=f'{clr}\033[H\033[{r}B\033[{c}C', right='\033[0m', interval=0.01, **kwargs)
    # return make(size, fill='\033[1;31m\u2588\033[0m', empty='\033[1;30m\u2588\033[0m', vertical='\u2502', horizontal='\u2500', top_left='\u250c', top_right='\u2510', bottom_left='\u2514', bottom_right='\u2518')

def test(bar: HealthBarBase):
    '''
    Test a health bar by reading values for the health and setting them untill an
    empty line is entered.

    @param bar  A health bar instance created by ``make*()`` (or manually).
    '''
    def get_input():
        res = input()
        print('\033[2J', end='')
        return res

    try:
        print('starting...')
        bar.start()
        # print(bar.is_alive())
        s = get_input()
        while s:
            bar.set_value(float(s))
            s = get_input()
    finally:
        print('stopping.....')
        bar.stop()
        # print(bar.is_alive())

if __name__ == '__main__':
    import IPython
    IPython.embed()
