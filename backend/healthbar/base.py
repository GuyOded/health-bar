#!/usr/bin/env python3
'''
Simple health bar implementation.

Implements a base for an animated health bar logic.
'''
from abc import ABCMeta, abstractmethod
from typing import Union

class HealthBarBase(metaclass=ABCMeta):
    '''
    Base class for health bar implementaions.
    '''
    def __init__(self, length:int, max_value: Union[int, float]=100, *, start_at: Union[int, float]=None):
        self.__length = length
        self.__max_value = max_value
        if start_at is None:
            self.__value = max_value
        else:
            self.__value = start_at

    @property
    def length(self):
        '''
        The amount of segments in the bar.
        For example: the amount of LEDs or the amount of characters.
        '''
        return self.__length

    @property
    def max_value(self):
        '''
        The value that represents a full bar.
        '''
        return self.__max_value

    @property
    def value(self):
        '''
        The current value for the health bar.
        '''
        return self.__value

    @value.setter
    def value(self, value):
        '''
        Set the value while keeping the value in range [0, max_value].
        '''
        self.__value = max(0, min(value, self.max_value))

    @abstractmethod
    def draw(self):
        '''
        Visually display the health bar.
        '''
        raise NotImplemented


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
        print('\033[2J\033[H', end='')
        print(f'{self.__tl}{self.__t * self.length}{self.__tr}')
        print(f'{self.__l}{self.__fill * fill_amount}{self.__empty * (self.length - fill_amount)}{self.__r}')
        print(f'{self.__bl}{self.__b * self.length}{self.__br}')
