#!/usr/bin/env python3
'''
Simple console-based health bar implementation.

Implements a console-based health bar logic.
'''
import sys

from healthbar.base import HealthBarBase

class HideCursor:
    '''
    Hide and restore the cursor.

    Usage:
    >>> with HideCursor():
    ...     # do things now that the cursor is hidden
    '''
    def __enter__(self):
        print('\033[?25l', end='')
        sys.stdout.flush()

    def __exit__(self, *info):
        print('\033[?25h', end='')
        sys.stdout.flush()


class ConsoleHealthBar(HealthBarBase):
    '''
    A console-based health bar.
    '''
    def __init__(self, *args, fill='#', empty=' ', corner='+', vertical='|', horizontal='-',
                 top_left=None, top=None, top_right=None,
                 left=None, right=None,
                 bottom_left=None, bottom=None, bottom_right=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.__tl = top_left or corner
        self.__t = top or horizontal
        self.__tr = top_right or corner
        self.__l = left or vertical
        self.__fill = fill
        self.__empty = empty
        self.__r = right or vertical
        self.__bl = bottom_left or corner
        self.__b = bottom or horizontal
        self.__br = bottom_right or corner

    def draw(self):
        fill_amount = round(self.length * self.value / self.max_value)
        with HideCursor():
            print('\033[H', end='')
            print(f'{self.__tl}{self.__t * self.length}{self.__tr}')
            print(f'{self.__l}{self.__fill * fill_amount}{self.__empty * (self.length - fill_amount)}{self.__r}')
            print(f'{self.__bl}{self.__b * self.length}{self.__br}')
